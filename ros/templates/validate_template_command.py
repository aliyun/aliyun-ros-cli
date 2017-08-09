# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

from aliyunsdkros.request.v20150901 import ValidateTemplateRequest

import ros.apps.config as connect
import ros.apps.utils as utils
import json
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def setup(subparsers):
    parser = subparsers.add_parser('validate-template', help='Validates a specified template')
    parser.add_argument('--template-url', help='Location of file containing the template body', required=True)

    parser.set_defaults(func=validate_template)


def validate_template(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = ValidateTemplateRequest.ValidateTemplateRequest()

    file_context =  utils.read_template(args.template_url)
    req.set_content('{"Template":' + file_context + "}")

    return req


def print_response(data):
    print('The template is ok:\n')

    # if connect.JSON_FORM:
    jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
    print(jsonDumpsIndentStr)
    # else:
    #      utils.recursivePrint(list)

