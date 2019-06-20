#!/usr/bin/python
import os
import boto3
import pexpect
import datetime
import subprocess
import logging
from botocore.exceptions import ClientError

logfilename = "/var/log/awsrotate.log"
logging.basicConfig(filename=logfilename,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

days = 2
usernames = []
dates = []
dayscount = []
users = []
accesskeyids = []
useraccessids = []
newaccesskey = []
inactive = []

iam_client = boto3.client('iam')
users = iam_client.list_users()
def create_update_keys(users):
	for index in range(len(users['Users'])):
		usernames.append(users['Users'][index]['UserName'])

	paginator = iam_client.get_paginator('list_access_keys')
	for username in usernames:
		for response in paginator.paginate(UserName=username):
			dates.append(list(response['AccessKeyMetadata'][key]['CreateDate'] for key in range(len(response['AccessKeyMetadata'])) if response['AccessKeyMetadata'][key]['Status'] == 'Active'))
			accesskeyids.append(list(response['AccessKeyMetadata'][keyid]['AccessKeyId'] for keyid in range(len(response['AccessKeyMetadata'])) if response['AccessKeyMetadata'][keyid]['Status'] == 'Active'))

	today = datetime.datetime.now()

	for date in range(len(dates)):
		dayscount.append(today - dates[date][0].replace(tzinfo=None))
		users = [usernames[day] for day in range(len(dayscount)) if dayscount[day].days >= int(days)]
		useraccessids = [accesskeyids[day][0] for day in range(len(dayscount)) if dayscount[day].days >= int(days)]

	for user in range(len(users)):
		update_key_status = iam_client.update_access_key(AccessKeyId=useraccessids[user],Status='Inactive',UserName=users[user])
		create_key = iam_client.create_access_key(UserName=users[user])
		newaccesskey.append(create_key['AccessKey'])

	for newkey in range(len(newaccesskey)):
		if users[newkey] == newaccesskey[newkey]['UserName']:
			child = pexpect.spawn('aws configure --profile {}'.format(newaccesskey[newkey]['UserName']))
			child.expect('.*Access Key.*')
			child.sendline('{}'.format(newaccesskey[newkey]['AccessKeyId']))
			child.expect('.*Secret Access Key.*')
			child.sendline('{}'.format(newaccesskey[newkey]['SecretAccessKey']))
			child.expect('.*region name.*')
			child.sendline('us-east-1')
			child.expect('.*output format.*')
			child.sendline('json')
	if len(users) > 0:
		export_output = os.system("export AWS_DEFAULT_PROFILE="+users[0])
		logging.info("User keys updated successfully")
	else:
		logging.info("There are no users profiles exists within the respective time period : %d" % (int(days)))

create_update_keys(users)

def delete_keys(Accesskey,Username):
	
	iam_client.delete_access_key(AccessKeyId=Accesskey,UserName=Username)

paginator = iam_client.get_paginator('list_access_keys')
for username in usernames:
    for response in paginator.paginate(UserName=username):
        inactive.append([response['AccessKeyMetadata'][key] for key in range(len(response['AccessKeyMetadata'])) if response['AccessKeyMetadata'][key]['Status'] == 'Inactive'])

for inact in range(len(inactive)):
	if len(inactive[inact]) > 0:
		delete_keys(inactive[inact][0]['AccessKeyId'],inactive[inact][0]['UserName'])
		logging.info("User keys deleted successfully for %s" %(inactive[inact][0]['UserName']))
	else:
		logging.info("There are no user keys exists within the time period: %d" %(days))

def readfile(filename):
    logfile = open(filename,"r")
    logfile_lines = logfile.readlines()
    for line in logfile_lines:
        if "botocore.credentials" in line:
            logfile_lines.remove(line)
    updatefile = open(filename, "w")
    for appendline in logfile_lines:
        updatefile.write(appendline)

readfile(logfilename)
