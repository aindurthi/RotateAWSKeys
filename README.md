# RotateAWSKeys
This is a python script that is used to automatically rotate the IAM keys of the multiple users using a cron scheduler.
# Prerequisites
1. Python 2.7.5
2. Boto3
3. pexpect

# Adding Crontab
1. crontab -e
2. * 4 * * *	/usr/bin/python	/opt/aws/aws_configure.py # you need to add the respective directory where the script is present
3. crontab -l

