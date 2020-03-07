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
    name="nlpcda",
    version="1.0",
    keywords=("pip", "nlptool", "nlpcda", "nlp"),
    description="NLP Chinese Data Augmentation，一键中文数据增强工具",
    long_description="一键中文数据增强工具，支持：随机实体替换，近义词、近义近音字替换，随机字删除。在不改变原文的情况下生成指定数量的训练语料文本",
    license="MIT Licence",

    url="https://github.com/425776024/nlpcda",
    author="Jiang.XinFa",
    author_email="425776024@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['jieba']
)
