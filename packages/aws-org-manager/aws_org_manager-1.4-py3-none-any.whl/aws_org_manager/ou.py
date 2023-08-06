import logging

log = logging.getLogger()


def getParentOUs(client, parentID):
    paginator = client.get_paginator('list_organizational_units_for_parent')
    pages = paginator.paginate(ParentId=parentID).build_full_result()
    log.info('list_organizational_units_for_parent => %s, %s', parentID, pages)
    return pages['OrganizationalUnits']


def isOUExists(client, parentID, ouName):
    paginator = client.get_paginator('list_organizational_units_for_parent')
    pages = paginator.paginate(ParentId=parentID).build_full_result()
    for page in pages['OrganizationalUnits']:
        log.info('list_organizational_units_for_parent => %s', page)
        if page['Name'] == ouName:
            log.info('OU %s exists for parentID %s', ouName, parentID)
            return page['Id']

    return False


def createOrg(client, parentID, ouName):
    log.info('Creating OU %s for parentID %s', ouName, parentID)
    try:
        r = client.create_organizational_unit(
             ParentId=parentID,
             Name=ouName
        )['OrganizationalUnit']
        log.info('create_organizational_unit => %s', r)
        return r['Id']
    except Exception as e:
        log.exception(e)
        return None


def getOIDByName(client, metas, match):
    for meta in metas:
        log.info('Checking %s with %s', meta['Name'], match)
        if meta['Name'] == match:
            log.info('OU %s found at parentID %s', match, meta['Id'])
            return meta['Id']
        else:
            x = getOIDByName(
                client,
                getParentOUs(client, meta['Id']),
                match
            )
            if x is not None:
                return x
