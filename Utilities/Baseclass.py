import boto3
import os


aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key']
region = 'ap-south-1'


class Baseclass:

    def ASGconnection(self):
            asg_client = boto3.client('autoscaling',region_name=region,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
            return asg_client


    def EC2Connection(self):
            ec2_client = boto3.client('ec2',region_name=region,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
            return ec2_client