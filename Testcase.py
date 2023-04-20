from Methods.Testcase1Methods import TestCase1
from Methods.Testcase2Methods import TestCase2

class TestCase:

    def testcaseA(self, auto_scaling_group_name):

        testscenarios = TestCase1(auto_scaling_group_name)

        # Test 1: Check if the desired and running count are the same
        testscenarios.validate_desired_running_count()

        # Test 2: Check if the instances are distributed across multiple availability zones
        testscenarios.validate_az()

        # Test 3: Check if Security Group, ImageID and VPC ID are same on ASG running instances
        testscenarios.compare_image_id_sg_id_vpc_id()

        # Test 4: Find out uptime of ASG running instances and get the longest running instance.
        testscenarios.uptime_of_instances()

    def testcaseB(self, auto_scaling_group_name):
        testscenarios = TestCase2(auto_scaling_group_name)

        # Test 1 : Find the Scheduled actions of given ASG which is going to run next and calculate elapsed in
        # hh:mm:ss from current time.
        testscenarios.get_scheduled_action()

        # Test 2 : Calculate total number instances lunched and terminated on current day for the given ASG.
        testscenarios.terminated_instances()
        testscenarios.launched_instances()


TestExecution = TestCase()
TestExecution.testcaseA('lv-test-cpu')
TestExecution.testcaseB('lv-test-cpu')