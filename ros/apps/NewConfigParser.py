# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

import ConfigParser


class NewConfigParser(ConfigParser.ConfigParser):
    '''
    Make options keep upper case
    '''
    def __init__(self,defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr
