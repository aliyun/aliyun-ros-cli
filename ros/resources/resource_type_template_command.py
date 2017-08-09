# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

from aliyunsdkros.request.v20150901 import DescribeResourceTypeTemplateRequest

import ros.apps.config as connect
import ros.apps.utils as utils
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def setup(subparsers):
    parser = subparsers.add_parser('resource-type-template', help='Returns template of the specific resource type')
    parser.add_argument('--name', help='The name of resource', required=True)

    parser.set_defaults(func=resource_type_template)


def resource_type_template(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeResourceTypeTemplateRequest.DescribeResourceTypeTemplateRequest()
    req.set_TypeName(args.name)

    return req


def print_response(data):
    # if connect.JSON_FORM:
    jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
    print(jsonDumpsIndentStr)
    # else:
    #      utils.recursivePrint(list)

