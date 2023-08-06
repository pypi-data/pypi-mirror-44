#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='tudejian_test_pypi',
    version='0.0.1',
    author='tudejian',
    author_email='tudejian@gmail.com',
    description=u'Test pipy upload by tudejian',
    packages=['tudejian_test_pypi'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'testFoo1=tudejian_test_pypi:testFoo1',
            'testFoo2=tudejian_test_pypi:testFoo2'
        ]
    }
)
