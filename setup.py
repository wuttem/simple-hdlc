#!/usr/bin/python
# coding: utf8

from setuptools.command.test import test as TestCommand
import sys
import os
import logging
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

# parse version
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       "simple_hdlc", "__init__.py")) as fdp:
    pattern = re.compile(r".*__version__ = '(.*?)'", re.S)
    VERSION = pattern.match(fdp.read()).group(1)

test_requirements = [
    "pytest"
]

reqs = [
    "pyserial",
    "pythoncrc",
    "six"
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        logging.basicConfig(level=logging.INFO)
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='simple-hdlc',
    version=VERSION,
    description="Simple HDLC Protocol",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Matthias Wutte",
    author_email='matthias.wutte@gmail.com',
    url='https://github.com/wuttem/simple-hdlc',
    packages=[
        'simple_hdlc',
    ],
    include_package_data=True,
    install_requires=reqs,
    zip_safe=False,
    keywords='simple-hdlc',
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)
