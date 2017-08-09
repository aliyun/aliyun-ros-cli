# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

from aliyunsdkros.request.v20150901 import DescribeEventsRequest

import ros.apps.config as connect
import ros.apps.utils as utils
import json
import sys
import math

reload(sys)
sys.setdefaultencoding('utf-8')


def setup(subparsers):
    parser = subparsers.add_parser('list-events', help='Returns all stack related events for a specified stack in reverse chronological order')
    parser.add_argument('--stack-name', help='The name that is associated with the stack', required=True)
    parser.add_argument('--stack-id', help='The id that is associated with the stack', required=True)
    parser.add_argument('--resource-status', help='status of resources: COMPLETE\FAILED\IN_PROGRESS', choices=['COMPLETE', 'FAILED', 'IN_PROGRESS'])
    parser.add_argument('--resource-name', help='The name of resources')
    parser.add_argument('--resource-type', help='The type of resources')
    parser.add_argument('--page-number', help='The page number of stack lists, start from 1, default 1', type=int, default=1)
    parser.add_argument('--page-size', help='Lines each page, max 100, default 10', type=int, default=10)
    
    parser.set_defaults(func=list_events)


def list_events(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeEventsRequest.DescribeEventsRequest()
    req.set_StackName(args.stack_name)
    req.set_StackId(args.stack_id)

    if args.resource_status is not None:
        req.set_ResourceStatus(args.resource_status)

    if args.resource_name is not None:
        req.set_ResourceName(args.resource_name)

    if args.resource_type is not None:
        req.set_ResourceType(args.resource_type)

    req.set_PageNumber(args.page_number)
    req.set_PageSize(args.page_size)

    return req


def print_response(data):
    if connect.JSON_FORM:
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print(jsonDumpsIndentStr)
    else:
        print('\nTotal Records: %d     Page: %d/%d' % (data.get('TotalCount'), data.get('PageNumber'),
            math.ceil(float(data.get('TotalCount'))/data.get('PageSize'))))

        for item in data.get('Events'):
            print('\n%-20s:  %s' % ('Time', item.get('Time')))
            print('%-20s:  %s' % ('ResourceName', item.get('ResourceName')))
            print('%-20s:  %s' % ('ResourceType', item.get('ResourceType')))
            print('%-20s:  %s' % ('Type', item.get('Type')))
            print('%-20s:  %s' % ('Status', item.get('Status')))
            print('%-20s:  %s\n' % ('StatusReason', item.get('StatusReason')))
