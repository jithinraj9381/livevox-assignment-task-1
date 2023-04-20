from Utilities.Baseclass import Baseclass
from datetime import datetime, timedelta
import sys

class TestCase1(Baseclass):
    def __init__(self,auto_scaling_group_name):
        self.asg_response = None
        self.instances = None
        self.desiredcapacity = None
        self.instance_ids = None
        self.ec2_response = None
        self.auto_scaling_group_name = auto_scaling_group_name

    def get_asg_instances(self):
        try:
            self.asg_response = self.ASGconnection().describe_auto_scaling_groups(AutoScalingGroupNames=[self.auto_scaling_group_name], MaxRecords=1)
            if not self.asg_response['AutoScalingGroups']:
                print('Error: No Auto Scaling Group found with the given name, Exiting TestCaseA')
                exit(1)
        except Exception as e:
            print("\nError occured while login or ASG is invalid")
            sys.exit()

        self.instances = self.asg_response['AutoScalingGroups'][0]['Instances']
        self.desiredcapacity = self.asg_response['AutoScalingGroups'][0]['DesiredCapacity']

    def get_ec2_instances(self):
        # Fetch Instances id created by ASG
        self.get_asg_instances()
        self.instance_ids = [instance['InstanceId'] for instance in self.instances]
        self.ec2_response = self.EC2Connection().describe_instances(InstanceIds=self.instance_ids)

    def validate_desired_running_count(self):
        self.get_asg_instances()
        print(f"\nDesired Capacity is {self.desiredcapacity} and Running Instances are {len(self.instances)}")
        assert self.desiredcapacity == len(self.instances), 'Desired and running count mismatch'
        print('Pass: Desired and running count match!')

    def validate_az(self):
        self.get_asg_instances()
        # Get AZs
        AZs = []

        for instance in self.instances:
            # Get the availability zone of each instance
            az = instance['AvailabilityZone']
            AZs.append(az)

        # Verify AZs of instances
        if len(AZs) > 1:
            # Check if all the instances have same AZs

            if all(x == AZs[0] for x in AZs):
                print(f"\nFail : Instances are not distributed across multiple AZs, All the instances have the same AZ {AZs}")
            else:
                print(f"\nPass : Instances are distributed across multiple AZ {AZs}")
        else:
            print(f"\nAuto Scaling group has only one instance running and AZ is {AZs}")

    def compare_image_id_sg_id_vpc_id(self):
        self.get_ec2_instances()

        # Loop through the instances and compare their image ID and security group ID and VPC ID
        if len(self.instance_ids) < 2:
            print("\nASG has Launched only 1 Instance, hence cannot compare image ID , security group ID and VPC ID")
        else:
            image_ids = []
            sg_ids = []
            vpc_ids = []

            for reservation in self.ec2_response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']

                    # Fetch Image IDs
                    image_id = instance['ImageId']
                    image_ids.append(image_id)
                    print(f"\nInstance {instance_id} has image ID {image_id}")

                    # Check if all the image IDs in the list are the same
                    if all(x == image_ids[0] for x in image_ids):
                        print(f"All instances have the same image ID")
                    else:
                        print(f"Not all instances have the same image ID")

                    # Fetch Security Group IDs
                    sg_id = [sg['GroupId'] for sg in instance['SecurityGroups']]
                    sg_ids.append(sg_id)
                    print(f"\nInstance {instance_id} has Security Group ID {sg_ids}")

                    # Check if all the Security Group id in the list are the same
                    if all(x == sg_ids[0] for x in sg_ids):
                        print(f"All instances have the same sg ID")
                    else:
                        print(f"Not all instances have the same sg ID")

                    # Fetch VPC ID
                    vpc_id = instance['VpcId']
                    vpc_ids.append(vpc_id)

                    # Print the instance ID and image ID
                    print(f"\nInstance {instance_id} has vpc ID {vpc_id}")

                    # Check if all the VPC ID in the list are the same
                    if all(x == vpc_ids[0] for x in vpc_ids):
                        print(f"All instances have the same vpc ID")
                    else:
                        print(f"Not all instances have the same vpc ID")

    def uptime_of_instances(self):
        self.get_asg_instances()
        self.get_ec2_instances()

        instances_data = []
        for reservation in self.ec2_response['Reservations']:
            for instance in reservation['Instances']:
                _instance_id = instance['InstanceId']
                _launch_time = instance['LaunchTime']
                instances_data.append({'InstanceId': _instance_id, 'Launchtime': _launch_time})

        max_uptime_instance = {'InstanceId': None, 'Uptime': timedelta(0)}

        for instance in instances_data:
            launch_time = instance['Launchtime'].replace(tzinfo=None)
            current_time = datetime.utcnow()
            uptime = current_time - launch_time

            if uptime > max_uptime_instance['Uptime']:
                max_uptime_instance['InstanceId'] = instance['InstanceId']
                max_uptime_instance['Uptime'] = uptime

        print(
            f"\nInstance with maximum uptime: {max_uptime_instance['InstanceId']}, Uptime: {max_uptime_instance['Uptime']}")


