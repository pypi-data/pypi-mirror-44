#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pali",
    version="0.0.1",
    author="Vipin Sharma",
    author_email="sh.vipin@gmail.com",
    description="A simple ThreadPool library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitvipin/hemis/tree/master/projects/pali",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
