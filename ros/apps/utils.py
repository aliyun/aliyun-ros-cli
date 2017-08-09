# coding=utf-8
#
# Copyright (c) 2017 Aliyun.com All right reserved. This software is the
# confidential and proprietary information of Aliyun.com ("Confidential
# Information"). You shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license agreement you entered
# into with Aliyun.com .
#
# created by quming on 07/18/2017

from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception import error_code, error_msg
import ros.apps.config as connect
import sys
import json
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')

def print_error(data):
    """
    Output error response from aliyun server
    :param data: response body in json
    :return: None
    """

    for (k, v) in data.items():
        print('%-20s:  %s' % (k, v))


def read_template(template_url):
    """
    Get template content, support local file and online url
    :param template_url: the url of the template
    :return: template content
    """
    if template_url.startswith('http'):
        try:
            response = urllib2.urlopen(template_url)
            return response.read()
        except Exception as e:
            print('Something wrong:\n%s' % str(e))
            sys.exit(1)
    else:
        try:
            with open(template_url, 'r') as file_object:
                file_context = file_object.read()
            return file_context
        except Exception as e:
            print('Something wrong:\n%s' % str(e))
            sys.exit(1)


def alignment(s, space, align='left'):
    """
    In python 2.x, make Chinese characters keep align
    :param str: input str
    :param space: width of the str
    :param align: left\right\center
    :return: aligned str
    """
    length = len(s.encode('gb2312'))
    space = space - length if space >= length else 0
    if align == 'left':
        s = s + ' ' * space
    elif align == 'right':
        s = ' ' * space + s
    elif align == 'center':
        s = ' ' * (space // 2) + s + ' ' * (space - space // 2)
    return s


def send_req(req):
    """
    Send ros request
    :param req: request
    :return: None
    """
    try:
        status, headers, body = get_raw_resp(req)
    except Exception, e:
        print('Something wrong:\n%s' % str(e))
        sys.exit(1)

    return status, headers, body


def deal_resp(status, headers, body, print_response):
    """
    Output response
    :param status: status code
    :param headers: response header
    :param body: response body
    :param print_response: print function
    :return: None
    """
    try:
        data = json.loads(body)
        if 200 <= status < 300:
            print("[Succeed]")
            print_response(data)
        else:
            print("[Failed]")
            print_error(data)
    except Exception, e:
        print("[Error]")
        print('Something wrong:\n%s' % str(e))
        sys.exit(1)


def get_raw_resp(request):
    """
    Get RAW response of aliyunsdk
    :param client: aliyunsdk client
    :param request: request to send
    :return: None
    """

    client = connect.client

    endpoint = client._resolve_endpoint(request)
    http_response = client._make_http_response(endpoint, request)
    if client._url_test_flag:
        raise ClientException("URLTestFlagIsSet", http_response.get_url())

    # Do the actual network thing
    try:
        status, headers, body = http_response.get_response_object()
        return status, headers, body
    except IOError as e:
        raise ClientException(
            error_code.SDK_SERVER_UNREACHABLE,
            error_msg.get_msg('SDK_SERVER_UNREACHABLE') + ': ' + str(e))
    except AttributeError:
        raise ClientException(
            error_code.SDK_INVALID_REQUEST,
            error_msg.get_msg('SDK_INVALID_REQUEST'))


def recursively_print(data, flag=True, indent=0):
    """
    Print dict\list recursively
    :param data: data to print
    :param flag: whether need to use indentation
    :param indent: passed father level's indent
    :return: None
    """
    if isinstance(data, list):
        for item in data:
            print('')
            recursively_print(item, False, indent + 1)

    elif isinstance(data, dict):
        for (k, v) in data.items():
            if indent == 0:
                print '\n\n===================================================\n',
            elif indent == 1:
                print '\n\n    -----------------------------------------------\n',
            print('')
            recursively_print(k, False, indent)
            print':  ',
            recursively_print(v, True, indent + 1)

    else:
        data_out = str(data)
        pre = ''
        if not flag:
            pre = '    '
        for i in range(0, indent):
            data_out = pre + data_out
        print data_out,


if __name__ == '__main__':
    resp = read_template('http://ros-template.cn-hangzhou.oss.aliyun-inc.com/ecs_vpc_instance.json')
    print(resp)