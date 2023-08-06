import logging

log = logging.getLogger()


def isRoleExist(client, roleName):
    log.info('Filtering roles for => %s', roleName)
    for i in client.roles.all():
        if i.name == roleName:
            log.info('Role %s exists', roleName)
            return True

    return False


def createRole(client, roleName, content):
    r = client.create_role(
         RoleName=roleName,
         AssumeRolePolicyDocument=content
    )
    log.info('create_role => %s', r)
    return r


def updateRole(client, roleName, content):
    log.info('update_assume_role_policy => %s', roleName)
    o = client.AssumeRolePolicy(roleName)
    o.update(PolicyDocument=content)
    return None


def attachPermission(client, roleName, policyName, content):
    log.info('put_role_policy => %s', roleName)
    o = client.RolePolicy(roleName, policyName)
    o.put(PolicyDocument=content)
    return None
