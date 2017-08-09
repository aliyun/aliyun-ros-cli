# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

import sys
import os
import ros.apps.NewConfigParser as NewConfigParser
import ros.apps.config

reload(sys)
sys.setdefaultencoding('utf-8')

POSSIBLE_TOPDIR = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), os.pardir, os.pardir))


def setup(subparsers):
    parser = subparsers.add_parser('set-userdata', help='Set default Aliyun access info')
    parser.add_argument('--key-id', help='The default Aliyun access key id', required=True)
    parser.add_argument('--key-secret', help='The default Aliyun access key region', required=True)
    parser.add_argument('--region-id', help='The default region', required=True)
    parser.add_argument('--json-ident', help='The default json indent when output in json format', default=2)

    parser.set_defaults(func=set_userdata)


def set_userdata(args):

    default_file = os.path.normpath(POSSIBLE_TOPDIR + '/ros/ros.conf')

    cf = NewConfigParser.NewConfigParser()
    cf.add_section('ACCESS')
    cf.set('ACCESS', 'ACCESS_KEY_ID', args.key_id)
    cf.set('ACCESS', 'ACCESS_KEY_SECRET', args.key_secret)
    cf.set('ACCESS', 'REGION_ID', args.region_id)

    cf.add_section('JSON')
    cf.set('JSON', 'JSON_INDENT', args.json_ident)

    try:
        with open(default_file, 'wb') as configfile:
            cf.write(configfile)
        print('Write : %s' % default_file)
    except Exception, e:
        print('Something wrong:\n%s' % str(e))
        sys.exit(1)
