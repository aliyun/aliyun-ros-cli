# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

from aliyunsdkros.request.v20150901 import DescribeStackDetailRequest

import ros.apps.config as connect
import ros.apps.utils as utils
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def setup(subparsers):
    parser = subparsers.add_parser('describe-stack', help='Returns the description for the specified stack')
    parser.add_argument('--stack-name', help='The name that is associated with the stack', required=True)
    parser.add_argument('--stack-id', help='The id that is associated with the stack', required=True)

    parser.set_defaults(func=describe_stack)


def describe_stack(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeStackDetailRequest.DescribeStackDetailRequest()
    req.set_headers({'x-acs-region-id': connect.REGION_ID})
    req.set_StackName(args.stack_name)
    req.set_StackId(args.stack_id)

    return req


def print_response(data):
    if(connect.JSON_FORM):
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print(jsonDumpsIndentStr)
    else:
        print("%-20s:  %s" % ('Name', data.get("Name")))
        print("%-20s:  %s" % ('Id', data.get("Id")))
        print("%-20s:  %s" % ('Description', data.get("Description")))
        print("%-20s:  %s" % ('Region', data.get("Region")))
        print("%-20s:  %s" % ('Status', data.get("Status")))
        print("%-20s:  %s" % ('StatusReason', data.get("StatusReason")))
        print("%-20s:  %s" % ('DisableRollback', data.get("DisableRollback")))
        print("%-20s:  %s" % ('TimeoutMins', data.get("TimeoutMins")))
        print("%-20s:  %s" % ('Created', data.get("Created")))
        print("%-20s:  %s" % ('Updated', data.get("Updated")))
        print("%-20s:  %s" % ('Webhook', data.get("Webhook")))

        print("\nParameters:")
        if data.get("Parameters") is not None:
            for (k,v) in data.get("Parameters").items():
                print("    %-20s: %s" % (k,v))

        print("\nOutputs:")
        if data.get("Outputs") is not None:
            for out in data.get("Outputs"):
                print("    %-20s: %s --- %s" % (out["OutputKey"], out["OutputValue"], out["Description"]))
    