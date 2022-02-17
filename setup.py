# Notes on setup: https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

from setuptools import setup

setup(
    name='pyhop_anytime',
    version='0.3.6',
    description='pyHOP planner modified to be an anytime planner',
    url='https://github.com/gjf2a/pyhop_anytime',
    author='Gabriel Ferrer',
    author_email='ferrer@hendrix.edu',
    license='Apache 2.0',
    packages=['pyhop_anytime']
)