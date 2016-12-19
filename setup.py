#!/usr/bin/python
# coding: utf8

from setuptools.command.test import test as TestCommand
import sys
import os
import logging
import re
from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

# parse version
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       "simple_hdlc.py")) as fdp:
    pattern = re.compile(r".*__version__ = '(.*?)'", re.S)
    VERSION = pattern.match(fdp.read()).group(1)

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=False)

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

test_requirements = [
    "pytest"
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
    author="Matthias Wutte",
    author_email='matthias.wutte@gmail.com',
    url='https://github.com/wuttem/simple-hdlc',
    packages=[
        'simple_hdlc',
    ],
    package_dir={'simple_hdlc': '.'},
    include_package_data=True,
    install_requires=reqs,
    zip_safe=False,
    keywords='simple-hdlc',
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)
