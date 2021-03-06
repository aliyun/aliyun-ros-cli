# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

from aliyunsdkros.request.v20150901 import CreateStacksRequest

import ros.apps.config as connect
import ros.apps.utils as utils
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def setup(subparsers):
    # create a parser for the 'create-stack' command
    parser = subparsers.add_parser('create-stack', help='Creates a stack as specified in the template')
    parser.add_argument('--region-id', help='The region that is associated with the stack')
    parser.add_argument('--stack-name', help='The name that is associated with the stack', required=True)
    parser.add_argument('--template-url', help='Location of file containing the template body', required=True)
    parser.add_argument('--parameters', help='A list of Parameter structures that specify input parameters for the stack. Synatax: key=value,key=value')
    parser.add_argument('--disable-rollback', help='Set to true to disable rollback of the stack if stack creation failed', default=True, type=bool)
    parser.add_argument('--timeout-in-minutes', help='The amount of time that can pass before the stack status becomes CREATE_FAILED', default=60, type=int)

    parser.set_defaults(func=create_stack)


def create_stack(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = CreateStacksRequest.CreateStacksRequest()
    
    if args.region_id is not None:
        req.set_headers({'x-acs-region-id': args.region_id})
    else:
        req.set_headers({'x-acs-region-id': connect.REGION_ID})

    content = {}
    content['Name'] = args.stack_name

    file_context = utils.read_template(args.template_url)
    content['Template'] = file_context

    content['DisableRollback'] = args.disable_rollback
    content['TimeoutMins'] = args.timeout_in_minutes

    ps = {}
    if args.parameters is not None:
        s = args.parameters.split(',')
        for item in s:
            pair = item.split('=')
            ps[pair[0]] = pair[1]

    content['Parameters'] = ps

    jsonDumpsIndentStr = json.dumps(content, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
    # print(jsonDumpsIndentStr)
    req.set_content(jsonDumpsIndentStr)

    return req


def print_response(data):
    if connect.JSON_FORM:
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print(jsonDumpsIndentStr)
    else:
        for (k, v) in data.items():
            print('%-20s:  %s' % (k, v))

