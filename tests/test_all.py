#!/usr/bin/env python
# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017
#
# Run this bash to test all situations of ros-cli. The test will create a new stack, use it in the 
# following unittests and delete it finally. Use default config 'ros/ros.conf'.
#
# Steps:
# 0 list-regions
#   preview-stack with name 'test_ros_cli', region-id 'cn-beijing', template './template.json'
# 1 create-stack with requirements above
# 2 update-stack with requirements above and stack-id of the newly created stack
# 3 list-stacks
#   describe-stack
# 4 list-resources
#   describe-resource
# 5 resource-type
#   resource-type-detail
#   resource-type-template
# 6 get-template
#   validate-template
# 7 list-events
# 8 abandon-stack
# 9 delete-stack
#
# The test choose a simple template, and set 3 seconds as waiting-time before update-stack\delete-stack\
# list-events so that resources for those procedures are available.
#
# The total time is around 11 seconds. (Including 9 seconds waiting)
#

import os
import sys
import unittest
import argparse
import json
import time
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

POSSIBLE_TOPDIR = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), os.pardir, os.pardir))

if os.path.exists(os.path.join(POSSIBLE_TOPDIR, 'ros', '__init__.py')):
    sys.path.insert(0, POSSIBLE_TOPDIR)

from ros.stacks import create_stack_command
from ros.stacks import delete_stack_command
from ros.stacks import update_stack_command
from ros.stacks import preview_stack_command
from ros.stacks import abandon_stack_command
from ros.stacks import describe_stack_command
from ros.stacks import list_stacks_command
from ros.resources import list_resources_command
from ros.resources import describe_resource_command
from ros.resources import resource_type_command
from ros.resources import resource_type_detail_command
from ros.resources import resource_type_template_command
from ros.templates import validate_template_command
from ros.templates import get_template_command
from ros.others import list_regions_command
from ros.others import list_events_command
from ros.apps import config
from ros.apps import utils

class TestROS(unittest.TestCase):

    stack_name = 'test_ros_cli'
    stack_id = ''
    region_id = 'cn-beijing'
    template_path = './template.json'
    show_output = False

    # Limit to try to delete/update a stack for the stack may be not under state COMPLETE
    max_try = 1
    wait_time = 3

    def setUp(self):
        config.ROS_TEST = True
        self.parser = argparse.ArgumentParser(prog='test_all')
        self.subparsers = self.parser.add_subparsers(title='commands', metavar='', help=None)
        self.parser.add_argument('--config', metavar='CONFIG_FILE', help='Location of config file', default=None)
        self.parser.add_argument('--json', action='store_true', help="Print results as JSON format", default=False)
        self.parser.add_argument('--region-id', help="Region ID, if not set, use config file's field", default=None)

        print('setUp...')

    def tearDown(self):
        print('tearDown...')

    def run_test(self, commands, ros_func, save_stack_id=False):
        self.args = self.parser.parse_args(commands)
        config.set_client(self.args.config, self.args.region_id)
        req = ros_func.prepare_request(self.args)
        status, headers, body = utils.send_req(req)

        if self.show_output:
            utils.deal_resp(status, headers, body, ros_func.print_response)
        elif status >= 300 or status < 200:
            print(body)

        self.assertGreaterEqual(status, 200)
        self.assertLess(status, 300)

        if save_stack_id:
            self.save_stack_id(json.loads(body)['Id'])

    def save_stack_id(self, stack_id):
        # Save stack_id in the file so that other tests can use it.
        cf = ConfigParser.ConfigParser()
        cf.add_section('Stack')
        cf.set('Stack', 'StackId', stack_id)

        with open('test.cfg', 'wb') as configfile:
            cf.write(configfile)

    def read_stack_id(self):
        # Read stack_id from the file
        cf = ConfigParser.ConfigParser()
        cf.read('test.cfg')
        self.stack_id = cf.get("Stack", "StackId")
        print('StackId: ', self.stack_id)
    
    def test_p0_list_regions(self):
        print('##### Test list-regions command #####')

        list_regions_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf','list-regions']
        self.run_test(commands, list_regions_command)

    def test_p0_preview_stack(self):
        print('##### Test preview-stack command #####')

        preview_stack_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'preview-stack', '--region-id',
            self.region_id, '--stack-name', self.stack_name, '--template-url', self.template_path,
            '--parameters', 'VpcName=testVPC']
        self.run_test(commands, preview_stack_command)

    def test_p1_create_stack(self):
        print('##### Test create-stack command #####')

        create_stack_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'create-stack', '--region-id',
            self.region_id, '--stack-name', self.stack_name, '--template-url', self.template_path,
            '--parameters', 'VpcName=testVPC']
        self.run_test(commands, create_stack_command, True)

    def test_p2_update_stack(self):
        print('##### Test update-stack command #####')

        self.read_stack_id()
        update_stack_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'update-stack', '--region-id',
            self.region_id, '--stack-name', self.stack_name, '--template-url', self.template_path,
            '--parameters', 'VpcName=testVPC', '--stack-id', self.stack_id]

        count = 0
        time.sleep(self.wait_time)
        while count < self.max_try and self.run_test(commands, update_stack_command) is False:
            # Wait a while   
            time.sleep(self.wait_time)
            count = count + 1

    def test_p3_list_stacks(self):
        print('##### Test list-stacks command #####')

        list_stacks_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'list-stacks', '--page-number', '2',
            '--page-size', '3']
        self.run_test(commands, list_stacks_command)

    def test_p3_describe_stack(self):
        print('##### Test describe-stack command #####')

        self.read_stack_id()
        describe_stack_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'describe-stack', '--stack-name', self.stack_name,
            '--stack-id', self.stack_id]
        self.run_test(commands, describe_stack_command)

    def test_p4_list_resources(self):
        print('##### Test list-resources command #####')

        self.read_stack_id()
        list_resources_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'list-resources', '--stack-name', self.stack_name,
            '--stack-id', self.stack_id]
        self.run_test(commands, list_resources_command)

    def test_p4_describe_resource(self):
        print('##### Test describe-resource command #####')

        self.read_stack_id()
        describe_resource_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'describe-resource', '--stack-name', self.stack_name,
            '--stack-id', self.stack_id, '--resource-name', 'Vpc']
        self.run_test(commands, describe_resource_command)

    def test_p5_resource_type(self):
        print('##### Test resource-type command #####')

        resource_type_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'resource-type']
        self.run_test(commands, resource_type_command)

    def test_p5_resource_type_detail(self):
        print('##### Test resource-type-detail command #####')

        resource_type_detail_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'resource-type-detail', '--name', 'ALIYUN::ECS::VPC']
        self.run_test(commands, resource_type_detail_command)

    def test_p5_resource_type_template(self):
        print('##### Test resource-type-template command #####')

        resource_type_template_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'resource-type-template', '--name', 'ALIYUN::ECS::VPC']
        self.run_test(commands, resource_type_template_command)

    def test_p6_get_template(self):
        print('##### Test get-template command #####')

        self.read_stack_id()
        get_template_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'get-template', '--stack-name', self.stack_name,
            '--stack-id', self.stack_id]
        self.run_test(commands, get_template_command)

    def test_p6_validate_template(self):
        print('##### Test validate-template command #####')

        self.read_stack_id()
        validate_template_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'validate-template', '--template-url', self.template_path]
        self.run_test(commands, validate_template_command)

    def test_p7_list_events(self):
        print('##### Test list-events command #####')

        self.read_stack_id()
        list_events_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'list-events', '--stack-name', self.stack_name,
            '--stack-id', self.stack_id, '--page-number', '1', '--page-size', '3', '--resource-status',
            'COMPLETE']
        time.sleep(3)
        self.run_test(commands, list_events_command)

    def test_p8_abandon_stack(self):
        print('##### Test abandon-stack command #####')

        self.read_stack_id()
        abandon_stack_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'abandon-stack', '--region-id',
            self.region_id, '--stack-name', self.stack_name, '--stack-id', self.stack_id]
        self.run_test(commands, abandon_stack_command)

    # Name p9 to make it run last
    def test_p9_delete_stack(self): 
        print('##### Test delete-stack command #####')

        self.read_stack_id()
        delete_stack_command.setup(self.subparsers)
        commands = ['--config', '../ros/ros.conf', 'delete-stack', '--region-id',
            self.region_id, '--stack-name', self.stack_name, '--stack-id', self.stack_id]

        count = 0
        time.sleep(self.wait_time)
        while count < self.max_try and self.run_test(commands, delete_stack_command) is False:
            # Wait a while
            time.sleep(self.wait_time)
            count = count + 1
            

if __name__ == '__main__':
    unittest.main()
