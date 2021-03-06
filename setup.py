import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="lit-script",
    version="0.1.0",
    url="https://github.com/MaciejWas/lit-script",
    license="MIT",
    author="Maciej Wasilewski",
    author_email="wasilewski.maciej20@gmail.com",
    description="Compiler for my cool & useless language",
    long_description=read("README.md"),
    packages=find_packages(exclude=("tests",)),
    install_requires=["lark"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ],
)
