import re
import os
import logging
from zipfile import ZipFile
from io import BytesIO
from time import gmtime, strftime

import boto3
import cfnresponse

from aws_org_manager.ou import getParentOUs, isOUExists, createOrg, getOIDByName
from aws_org_manager.accnt import isAccntExists, createAccnt, waitForCreateAccnt, isAccntMoved, moveAccnt
from aws_org_manager.scp import isPolicyExist, createPolicy, updatePolicy, attachPolicy

log = logging.getLogger()
org = boto3.client('organizations')
iam = boto3.client('iam')
s3 = boto3.client('s3')


def run(event, context):
    log.info('Event => %s', event)
    orgID = org.describe_organization()['Organization']['Id']
    parentID = event['ResourceProperties']['ParentId']
    accntName = event['ResourceProperties']['AccountName']
    ouName = event['ResourceProperties']['OUName']
    emailAddress = event['ResourceProperties']['Email']
    s3Bucket = event['ResourceProperties']['S3Bucket']
    policyZipFile = event['ResourceProperties']['PolicyZipFile']

    r = s3.get_object(
        Bucket=s3Bucket,
        Key=policyZipFile
    )['Body']
    zipfile = ZipFile(BytesIO(r.read()))
    unzippedPath = '/tmp/' + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    scpPath = unzippedPath + '/acl/scp'
    zipfile.extractall(unzippedPath)

    if event['RequestType'] in ['Create', 'Update']:
        OUID = isOUExists(org, parentID, ouName)
        if not OUID:
            OUID = createOrg(org, parentID, ouName)
            if not OUID:
                cfnresponse.send(event, context, cfnresponse.FAILED, {'Message': 'Failed Organization creation'})
                return 1

        newAccountId = isAccntExists(org, emailAddress)
        if not newAccountId:
            accntStatusID = createAccnt(org, emailAddress, accntName)
            if not accntStatusID:
                cfnresponse.send(event, context, cfnresponse.FAILED, {'Message': 'Failed Account creation'})
                return 1

            newAccountId = waitForCreateAccnt(org, accntStatusID, accntName)
            if not newAccountId:
                cfnresponse.send(event, context, cfnresponse.FAILED, {'Message': 'Something went wrong while waiting for account creation event'})
                return 1

        if not isAccntMoved(org, OUID, newAccountId):
            if isAccntMoved(org, org.list_roots()['Roots'][0]['Id'], newAccountId):
                sourceParentId = org.list_roots()['Roots'][0]['Id']
            else:
                sourceParentId = parentID
            if not moveAccnt(org, OUID, sourceParentId, newAccountId):
                cfnresponse.send(event, context, cfnresponse.FAILED, {'Message': 'Account move failed'})
                return 1

        for i in os.listdir(scpPath):  # Service Control policy
            if re.match(r'[^@]+@[^@]+\.[^@]+', i):
                name = i.split('.json')[0]
                id = isAccntExists(
                    org,
                    name
                )
            else:
                name = i.split('.')[0]
                id = getOIDByName(
                    org,
                    getParentOUs(org, org.list_roots()['Roots'][0]['Id']),
                    name
                )
            if not id:
                log.info('Id not found for %s', i)
                continue
            policy = open(scpPath + '/' + i, 'r').read()
            log.info('Adding SCP for ID %s => %s', id, name)
            try:
                policyId = isPolicyExist(org, name)
                if policyId:
                    policyId = updatePolicy(org, policyId, policy)
                else:
                    policyId = createPolicy(org, name, policy, id)
                    attachPolicy(org, policyId, id)
            except Exception as e:
                log.exception(e)
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {'Message': 'Success', 'OrganizationId': orgID})
    else:
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {'Message': 'Skipping, Request Type is Delete', 'OrganizationId': orgID})
    return 0
