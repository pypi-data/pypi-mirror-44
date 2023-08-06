#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'splunk_log_handler', '__version__.py'), 'r') as f:
    exec(f.read(), about)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov=splunk_log_handler']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


install_requirements = [
    'requests',
]

test_requirements = [
    "pytest",
    "pytest-cov",
]

setup(
    name="splunk-log-handler",
    version=about['__VERSION__'],
    keywords=("splunk", "log handler"),
    description="A log handler to send logs to a given splunk",
    long_description="A log handler to send logs to a given splunk",
    license="MIT",
    url="https://github.com/cuyu/splunk-log-handler",
    author="Curtis Yu",
    author_email="icyarm@icloud.com",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
    platforms="any",
    install_requires=install_requirements,
    cmdclass={
        'test': PyTest,
    },
    extras_require={
        'test': test_requirements,
    }
)
