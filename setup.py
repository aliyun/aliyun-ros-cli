# coding=utf-8

from setuptools import setup, find_packages

setup (
    name = 'aliyun-ros-cli',
    version = 'dev-0.0.3',
    keywords = ('aliyun', 'ros', 'template', 'orchestration'),
    install_requires = ['aliyun-python-sdk-ros'],

    author = 'shenggong.wang, quming.ly',
    author_email = 'shenggong.wang@alibaba-inc.com',
    scripts=['bin/ros'],
    packages = find_packages(),
    include_package_data=True,
    exclude_package_date={'':['.gitignore']},
    platforms = 'any'
)
