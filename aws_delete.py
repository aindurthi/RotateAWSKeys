import boto3

iam_client = boto3.client('iam')

usernames = []
inactive = []
users = iam_client.list_users()
for index in range(len(users['Users'])):
    usernames.append(users['Users'][index]['UserName'])

paginator = iam_client.get_paginator('list_access_keys')
for username in usernames:
    for response in paginator.paginate(UserName=username):
		inactive.append([response['AccessKeyMetadata'][key] for key in range(len(response['AccessKeyMetadata'])) if response['AccessKeyMetadata'][key]['Status'] == 'Inactive'])

for inact in range(len(inactive)):
	iam_client.delete_access_key(AccessKeyId=inactive[inact][0]['AccessKeyId'],UserName=inactive[inact][0]['UserName'])

