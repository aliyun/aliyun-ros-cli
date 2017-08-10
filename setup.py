# coding=utf-8

from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup (
    name = 'aliyun-ros-cli',
    version = '1.0.0',
    keywords = ('aliyun', 'ros', 'template', 'orchestration'),
    install_requires = ['aliyun-python-sdk-ros'],
    python_requires='>=2.6, <3',
    author = 'shenggong.wang, quming.ly',
    author_email = 'shenggong.wang@alibaba-inc.com',
    scripts=['bin/ros'],
    packages = find_packages(),
    include_package_data=True,
    exclude_package_date={'':['.gitignore']},
    platforms = 'any',
    description = 'Aliyun ros command line tools.',
    long_description=readme()
)
