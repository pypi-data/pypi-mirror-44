# -*- coding:utf-8 -*-


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="havedocker",
    version="0.0.2",
    author="haitanghuadeng",
    author_email="491609917@qq.com",
    description="This is Python-docker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haitanghuadeng",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
