# RotateAWSKeys
This is a python script that is used to automatically rotate the IAM keys of the multiple users using a cron scheduler.And add the respective user's profile in the credentials file.
# Prerequisites
1. Python 2.7.5
2. Boto3
3. pexpect

# Adding Crontab
1. crontab -e
2. ``` * 4 * * *	/usr/bin/python	/opt/aws/aws_configure.py # you need to add the respective directory where the script is present```
3. crontab -l

# Number of Days
To automatically rotate the access & secret keys and delete the previous keys based on days ex: 15,20,30...etc then change the "days" value in the "aws_configure.py" script.

