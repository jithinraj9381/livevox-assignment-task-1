from Utilities.Baseclass import Baseclass
from datetime import datetime, timezone


class TestCase2(Baseclass):
    def __init__(self,auto_scaling_group_name):
        self.auto_scaling_group_name = auto_scaling_group_name


    def get_ec2_instances(self):
        self.asg_activity_response = self.ASGconnection().describe_scaling_activities(AutoScalingGroupName=self.auto_scaling_group_name, MaxRecords=100)['Activities']

        current_date = datetime.now(timezone.utc).date()

        # Filter EC2 Instances Launched/Terminated by ASG
        self.instance_data = []
        for instance in self.asg_activity_response:
            if instance['EndTime'].date() == current_date and ("Terminating EC2 instance" in instance['Description'] or "Launching a new EC2 instance" in instance['Description']):
                instance_description = instance['Description']
                instance_id = instance['Description'].split()[-1]
                start_time = instance['StartTime']
                end_time = instance['EndTime']
                self.instance_data.append(
                    {'Description': instance_description, 'InstanceId': instance_id, 'StartTime': start_time, 'EndTime': end_time})

    def terminated_instances(self):
        self.get_ec2_instances()

        print("\nList of instances terminated today and corresponding start and end times:")
        terminated_count = 0
        for instance in self.instance_data:
            if "Terminating EC2 instance" in instance['Description']:
                print(f"InstanceId: {instance['InstanceId']}, Start time: {instance['StartTime']}, End time: {instance['EndTime']}")
                terminated_count += 1
        print(f"Number of Instances Terminated Today is: {terminated_count}")

    def launched_instances(self):
        self.get_ec2_instances()

        print("\nList of instances started today and corresponding start and end times:")
        launched_inst_count = 0
        for instance in self.instance_data:
            if "Launching a new EC2 instance" in instance['Description']:
                print(f"InstanceId: {instance['InstanceId']}, Start time: {instance['StartTime']}, End time: {instance['EndTime']}")
                launched_inst_count += 1
        print(f"Number of Instances Launched Today is: {launched_inst_count}")

    def get_scheduled_action(self):
        self.asg_schedule_response = self.ASGconnection().describe_scheduled_actions(AutoScalingGroupName=self.auto_scaling_group_name)

        scheduled_actions = self.asg_schedule_response['ScheduledUpdateGroupActions']

        # Find the next scheduled action
        next_action = min(scheduled_actions, key=lambda x: x['StartTime']) if scheduled_actions else None

        # If there is a next scheduled action, calculate the time until it runs
        if next_action:
            scheduled_time = next_action['StartTime']
            now = datetime.now(timezone.utc)
            time_until_action = scheduled_time - now

            # Convert the time until the action to hh:mm:ss format
            seconds = int(time_until_action.total_seconds())
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            time_until_action_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            print(f"\nThe next scheduled action for Auto Scaling group {self.auto_scaling_group_name} is '{next_action['ScheduledActionName']}' and it is scheduled to run in {time_until_action_str}.")
        else:
            print(f"\nThere are no scheduled actions for Auto Scaling group {self.auto_scaling_group_name}.")
