#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Jiang.XinFa
# Mail: 425776024@qq.com
# Created Time:  2019-12-29 12:38:34
#############################################

from setuptools import setup, find_packages

setup(
    name="nlpts",
    version="0.0.1",
    keywords=("pip", "nlptool", "nlpts", "nlp"),
    description="A Text Summarization tool",
    long_description="A (Chinese) NLP Text Summarization toll",
    license="MIT Licence",

    url="https://github.com/425776024/nlpTS",
    author="Jiang.XinFa",
    author_email="425776024@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['jieba']
)
