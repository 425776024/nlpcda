#!/usr/bin/env python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name="nlpcda",
    version="2.5.3",
    keywords=("pip", "nlptool", "nlpcda", "nlp", '数据增强'),
    description="NLP Chinese Data Augmentation.一键中文数据增强.NLP数据增强",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://github.com/425776024/nlpcda",
    author="Jiang.XinFa",
    author_email="425776024@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['jieba', 'requests', 'bert4keras==0.7.7']
)
