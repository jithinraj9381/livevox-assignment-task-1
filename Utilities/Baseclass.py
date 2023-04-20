import boto3

access_key = ''
secret_key = ''
region = 'ap-south-1'

class Baseclass:

    def ASGconnection(self):
        asg_client = boto3.client('autoscaling',region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
        return asg_client

    def EC2Connection(self):
        ec2_client = boto3.client('ec2',region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
        return ec2_client