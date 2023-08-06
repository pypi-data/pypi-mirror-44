import os
import logging
from zipfile import ZipFile
from io import BytesIO
from time import gmtime, strftime

import boto3
import cfnresponse

from aws_member_accnt_manager.role import isRoleExist, createRole, updateRole, attachPermission

log = logging.getLogger()
org = boto3.client('organizations')
sts = boto3.client('sts')
s3 = boto3.client('s3')

orgAccnts = {}
paginator = org.get_paginator('list_accounts')
pages = paginator.paginate().build_full_result()
for page in pages['Accounts']:
    orgAccnts[page['Email']] = page['Id']
log.info('List of accounts in organization %s', orgAccnts)


def run(event, context):
    log.info('Event => %s', event)
    s3Bucket = event['ResourceProperties']['S3Bucket']
    policyZipFile = event['ResourceProperties']['PolicyZipFile']

    r = s3.get_object(
        Bucket=s3Bucket,
        Key=policyZipFile
    )['Body']
    zipfile = ZipFile(BytesIO(r.read()))
    unzippedPath = '/tmp/' + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    iamRolesPath = unzippedPath + '/acl/roles'
    zipfile.extractall(unzippedPath)

    if event['RequestType'] in ['Create', 'Update']:
        for i in os.listdir(iamRolesPath):
            if i in orgAccnts.keys():
                accntId = orgAccnts[i]
                log.info('Assuming IAM roles for Account %s under ID %s', i, accntId)
                assumdRole = sts.assume_role(
                    RoleArn='arn:aws:iam::' + accntId + ':role/OrganizationAccountAccessRole',
                    RoleSessionName=accntId
                )
                creds = assumdRole['Credentials']
                iam = boto3.resource(
                    'iam',
                    aws_access_key_id=creds['AccessKeyId'],
                    aws_secret_access_key=creds['SecretAccessKey'],
                    aws_session_token=creds['SessionToken'],
                )
                log.info('Applying IAM roles for Account %s under ID %s', i, accntId)
                x = iamRolesPath + '/' + i
                for j in os.listdir(x + '/trusts'):
                    trustJSON = open(x + '/trusts/' + j, 'r').read()
                    policyJSON = open(x + '/policies/' + j, 'r').read()
                    name = accntId + '_' + j.split('.')[0]

                    log.info('Adding IAM Role for %s', name)

                    if isRoleExist(iam, name):
                        updateRole(iam, name, trustJSON)
                    else:
                        createRole(iam, name, trustJSON)
                    attachPermission(iam, name, name, policyJSON)
            else:
                log.info('Account %s not found', i)
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {'Message': 'Success'})
    else:
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {'Message': 'Skipping, Request Type is Delete'})

    return 0
