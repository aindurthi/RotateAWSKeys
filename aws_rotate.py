import boto3
import datetime
from botocore.exceptions import ClientError

usernames = []
dates = []
dayscount = []
users = []
accesskeyids = []
useraccessids = []
newaccesskey = []
iam_client = boto3.client('iam')
users = iam_client.list_users()
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
	users = [usernames[day] for day in range(len(dayscount)) if dayscount[day].days >= 0]
	useraccessids = [accesskeyids[day][0] for day in range(len(dayscount)) if dayscount[day].days >= 0]

for user in range(len(users)):
	update_key_status = iam_client.update_access_key(AccessKeyId=useraccessids[user],Status='Inactive',UserName=users[user])
	create_key = iam_client.create_access_key(UserName=users[user])
	newaccesskey.append(create_key['AccessKey'])


for newkey in range(len(newaccesskey)):
	if users[newkey] == newaccesskey[newkey]['UserName']:
		file = open("/opt/."+newaccesskey[newkey]['UserName']+".txt", "w")
		file.write("Access Key : {}\n".format(newaccesskey[newkey]['AccessKeyId']))
        file.write("Secret Key : {}".format(newaccesskey[newkey]['SecretAccessKey']))
        file.close()
