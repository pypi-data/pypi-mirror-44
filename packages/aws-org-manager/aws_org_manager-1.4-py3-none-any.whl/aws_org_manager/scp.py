import logging

log = logging.getLogger()


def isPolicyExist(client, policyName):
    paginator = client.get_paginator('list_policies')
    pages = paginator.paginate(Filter='SERVICE_CONTROL_POLICY').build_full_result()
    for page in pages['Policies']:
        log.info('list_policies => %s', page)
        if page['Name'] == policyName:
            log.info('Policy %s exists', policyName)
            return page['Id']

    return False


def createPolicy(client, policyName, content, description):
    r = client.create_policy(
         Content=content,
         Description=policyName + ' ' + description,
         Name=policyName,
         Type='SERVICE_CONTROL_POLICY'
    )
    log.info('create_policy => %s', r)
    return r['Policy']['PolicySummary']['Id']


def updatePolicy(client, policyId, content):
    r = client.update_policy(
         Content=content,
         PolicyId=policyId
    )
    log.info('update_policy => %s', r)
    return r['Policy']['PolicySummary']['Id']


def attachPolicy(client, policyId, targetId):
    client.attach_policy(
         PolicyId=policyId,
         TargetId=targetId
    )
    return 0
