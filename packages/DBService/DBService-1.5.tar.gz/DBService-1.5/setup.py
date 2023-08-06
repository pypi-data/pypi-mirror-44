# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Email:  hhczy1003@163.com
# @Date:   2017-08-01 20:37:27
# @Last Modified by:   hang.zhang
# @Last Modified time: 2019-04-12 17:28:46

from setuptools import setup

setup(
    name="DBService",
    version="1.5",
    author="yiTian.zhang",
    author_email="hhczy1003@163.com",
    packages=["DBService"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "scrapy",
        "scrapy-redis",
        "pymongo",
        "apscheduler",
        "selenium",
    ],
)
