import logging

log = logging.getLogger()


def isAccntExists(client, emailAddress):
    paginator = client.get_paginator('list_accounts')
    pages = paginator.paginate().build_full_result()
    for page in pages['Accounts']:
        log.info('list_accounts => %s', page)
        if page['Email'] == emailAddress:
            log.info('Account exists with email %s', emailAddress)
            return page['Id']

    return False


def createAccnt(client, emailAddress, accntName):
    log.info('Creating account %s with email %s', accntName, emailAddress)
    try:
        r = client.create_account(
            Email=emailAddress,
            AccountName=accntName
        )['CreateAccountStatus']
        log.info('create_account => %s', r)
        return r['Id']
    except Exception as e:
        log.exception(e)
        return None


def waitForCreateAccnt(client, accntStatusID, accntName):
    while True:
        r = client.describe_create_account_status(
            CreateAccountRequestId=accntStatusID
        )
        log.info('describe_create_account_status => %s', r)
        status = r['CreateAccountStatus']['State']

        if status == 'FAILED':
            log.error('Account creation %s FAILED', accntName)
            return None
        if status == 'SUCCEEDED':
            return r['CreateAccountStatus']['AccountId']


def isAccntMoved(client, OUID, newAccountId):
    paginator = client.get_paginator('list_accounts_for_parent')
    pages = paginator.paginate(ParentId=OUID).build_full_result()
    for page in pages['Accounts']:
        log.info('list_accounts_for_parent => %s', page)
        if page['Id'] == newAccountId:
            log.info('AccountID %s exists at parentID %s', newAccountId, OUID)
            return True
    return False


def moveAccnt(client, OUID, parentID, newAccountId):
    try:
        log.info('Moving %s from %s to %s', newAccountId, parentID, OUID)
        r = client.move_account(
            AccountId=newAccountId,
            SourceParentId=parentID,
            DestinationParentId=OUID
        )
        log.info('move_account => %s', r)
        return True
    except Exception as e:
        log.exception(e)
        return False
