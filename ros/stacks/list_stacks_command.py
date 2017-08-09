# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

from aliyunsdkros.request.v20150901 import DescribeStacksRequest

import ros.apps.config as connect
import ros.apps.utils as utils
import json
import sys
import math

reload(sys)
sys.setdefaultencoding('utf-8')


def setup(subparsers):
    parser = subparsers.add_parser('list-stacks', help='Returns the summary information for stacks whose status matches the specified StackStatusFilter')
    parser.add_argument('--stack-name', help='The name that is associated with the stack', default=None)
    parser.add_argument('--stack-id', help='The id that is associated with the stack', default=None)
    parser.add_argument('--status', help='status of stacks', choices=['CREATE_COMPLETE', 'CREATE_FAILED', 'CREATE_IN_PROGRESS',\
     'DELETE_COMPLETE', 'DELETE_FAILED', 'DELETE_IN_PROGRESS', 'ROLLBACK_COMPLETE', 'ROLLBACK_FAILED', 'ROLLBACK_IN_PROGRESS'], default=None)
    parser.add_argument('--region-id', help='The region of stacks')
    parser.add_argument('--page-number', help='The page number of stack lists, start from 1, default 1', type=int, default=1)
    parser.add_argument('--page-size', help='Lines each page, max 100, default 10', type=int, default=10)

    parser.set_defaults(func=list_stacks)


def list_stacks(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeStacksRequest.DescribeStacksRequest()
    # No function in DescribeStacksRequest to set region-id

    if args.region_id is not None:
        req.set_headers({'x-acs-region-id': args.region_id})
    else:
        req.set_headers({'x-acs-region-id': connect.REGION_ID})

    if args.stack_name is not None:
        req.set_Name(args.stack_name)

    if args.stack_id is not None:
        req.set_StackId(args.stack_id)

    if args.status is not None:
        req.set_Status(args.stack_status)

    req.set_PageNumber(args.page_number)
    req.set_PageSize(args.page_size)

    return req


def print_response(data):

    print('\nTotal Records: %d     Page: %d/%d' % (data.get('TotalCount'), data.get('PageNumber'),
            math.ceil(float(data.get('TotalCount'))/data.get('PageSize'))))

    if connect.JSON_FORM:
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print(jsonDumpsIndentStr)
    else:
        for item in data.get('Stacks'):
            print('\n%-20s:  %s' % ('Id', item.get('Id')))
            print('%-20s:  %s' % ('Name', item.get('Name')))
            print('%-20s:  %s' % ('Description', item.get('Description')))
            print('%-20s:  %s' % ('Region', item.get('Region')))
            print('%-20s:  %s' % ('Status', item.get('Status')))
            print('%-20s:  %s' % ('StatusReason', item.get('StatusReason')))
            print('%-20s:  %s' % ('TimeoutMins', item.get('TimeoutMins')))
            print('%-20s:  %s' % ('DisableRollback', item.get('DisableRollback')))
            print('%-20s:  %s' % ('Created', item.get('Created')))
            print('%-20s:  %s\n' % ('Updated', item.get('Updated')))
