#coding:utf-8
import sys
from distutils.core import setup

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests/']
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='fantasy_data',
    version='1.1.3',
    description='FantasyData Python',
    author='Fantasy Football Calculator',
    author_email='support@fantasyfootballcalculator.com',
    url='https://fantasyfootballcalculator.com/fantasydata-python',
    packages=['fantasy_data'],
    keywords=['fantasy', 'sports', 'football', 'nba'],
    install_requires=[
        "requests",
        "six",
    ],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    download_url='https://github.com/ffcalculator/fantasydata-python/archive/v1.1.3.tar.gz'
)
