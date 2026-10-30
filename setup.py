#!/usr/bin/env python
# -*- coding:utf-8 -*-


from pathlib import Path

from setuptools import find_packages, setup

version = {}
exec((Path(__file__).parent / "nlpcda" / "_version.py").read_text(encoding="utf-8"), version)

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setup(
    name="nlpcda",
    version=version["__version__"],
    keywords=["pip", "nlptool", "nlpcda", "nlp", "数据增强"],
    description="NLP Chinese Data Augmentation.一键中文数据增强.NLP数据增强",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://github.com/425776024/nlpcda",
    author="Jiang.XinFa",
    author_email="425776024@qq.com",
    packages=find_packages(include=["nlpcda", "nlpcda.*"]),
    include_package_data=False,
    package_data={"nlpcda": ["data/*.txt"]},
    platforms="any",
    python_requires=">=3.10",
    project_urls={
        "Source": "https://github.com/425776024/nlpcda",
        "Issues": "https://github.com/425776024/nlpcda/issues",
    },
    install_requires=["jieba>=0.42.1", "requests>=2.33.0"],
)
