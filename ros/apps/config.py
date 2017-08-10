# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

import NewConfigParser
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

ACCESS_KEY_ID = None
ACCESS_KEY_SECRET = None
REGION_ID = None
client = None
JSON_FORM = False
JSON_INDENT = 2
ROS_DEBUG = False


def current_conf():
    """
    Print current client configuration
    :return: None
    """
    global ACCESS_KEY_ID
    global ACCESS_KEY_SECRET
    global REGION_ID

    print(
        "Current Config:\nACCESS_KEY_ID: %s\nACCESS_KEY_SECRET: %s\nREGION_ID: %s\n" %
        (ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID))


def set_client(cfg_file, region_id, top_dir=None):
    """
    Configure client
    :param cfg_file: specify the configuration file
    :param region_id: specify region id
    :param top_dir: working path
    :return: None
    """
    global ACCESS_KEY_ID
    global ACCESS_KEY_SECRET
    global REGION_ID
    global client
    global JSON_INDENT
    global ROS_DEBUG

    if top_dir is None:
        default_file = 'ros/ros.conf'
    else:
        default_file = os.path.normpath(top_dir + '/ros/ros.conf')

    cf = NewConfigParser.NewConfigParser()
    if cfg_file is None:
        if ROS_DEBUG:
            print("Use default config file: %s\n" % default_file)
        cfg_file = default_file

    if os.path.isfile(cfg_file):
        pass
    else:
        if os.path.isdir(top_dir + '/ros'):
            pass
        else:
            os.mkdir(top_dir + '/ros')
            
        print('Please set Aliyun access info first.')
        access_key_id = raw_input('Enter your access key id:')
        access_key_secret = raw_input('Enter your access key secret:')
        default_region_id = raw_input('Enter default region id:')

        cf.add_section('ACCESS')
        cf.set('ACCESS', 'ACCESS_KEY_ID', access_key_id)
        cf.set('ACCESS', 'ACCESS_KEY_SECRET', access_key_secret)
        cf.set('ACCESS', 'REGION_ID', default_region_id)

        cf.add_section('JSON')
        cf.set('JSON', 'JSON_INDENT', 2)

        with open(cfg_file, 'w') as configfile:
            cf.write(configfile)

    try:
        cf.read(cfg_file)
    except BaseException:
        print("""Config file (%s) error, please write it like:

        [ACCESS]
        ACCESS_KEY_ID = YOUR_KEY_ID
        ACCESS_KEY_SECRET = YOUR_KEY_SECRET
        REGION_ID = cn-beijing

        [JSON]
        JSON_INDENT = 2
        """ % cfg_file)
        sys.exit(1)

    ACCESS_KEY_ID = cf.get("ACCESS", "ACCESS_KEY_ID")
    ACCESS_KEY_SECRET = cf.get("ACCESS", "ACCESS_KEY_SECRET")
    if region_id is None:
        REGION_ID = cf.get("ACCESS", "REGION_ID")
    else:
        REGION_ID = region_id

    JSON_INDENT = int(cf.get("JSON", "JSON_INDENT"))

    client = AcsClient(
        ACCESS_KEY_ID,
        ACCESS_KEY_SECRET,
        REGION_ID
    )

    if ROS_DEBUG:
        current_conf()
