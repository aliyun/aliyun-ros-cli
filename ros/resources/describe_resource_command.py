# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

from aliyunsdkros.request.v20150901 import DescribeResourceDetailRequest

import ros.apps.config as connect
import ros.apps.utils as utils
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def setup(subparsers):
    parser = subparsers.add_parser('describe-resource', help='Returns a description of the specified resource in the specified stack')
    parser.add_argument('--stack-name', help='The name of stack', required=True)
    parser.add_argument('--stack-id', help='The id of stack', required=True)
    parser.add_argument('--resource-name', help='The name of resource', required=True)

    parser.set_defaults(func=describe_resource)


def describe_resource(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeResourceDetailRequest.DescribeResourceDetailRequest()
    req.set_StackName(args.stack_name)
    req.set_StackId(args.stack_id)
    req.set_ResourceName(args.resource_name)

    if args.region_id is not None:
        req.set_headers({'x-acs-region-id': args.region_id})
    else:
        req.set_headers({'x-acs-region-id': connect.REGION_ID})

    return req


def print_response(data):
    if connect.JSON_FORM:
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print(jsonDumpsIndentStr)
    else:
        print('\n%-20s:  %s' % ('Id', data.get('Id')))
        print('%-20s:  %s' % ('Name', data.get('Name')))
        print('%-20s:  %s' % ('Type', data.get('Type')))
        print('%-20s:  %s' % ('Status', data.get('Status')))
        print('%-20s:  %s' % ('StatusReason', data.get('StatusReason')))
        print('%-20s:  %s' % ('ResourceData', data.get('ResourceData')))
        print('%-20s:  %s' % ('PhysicalId', data.get('PhysicalId')))
        print('%-20s:  %s' % ('Created', data.get('Created')))
        print('%-20s:  %s' % ('Updated', data.get('Updated')))
        print('%-20s:  %s\n' % ('Deleted', data.get('Deleted')))

