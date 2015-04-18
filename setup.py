__author__ = "Michael Herold"
__copyright__ = "Copyright (c) 2015 Michael Herold"
__license__ = "MIT"

import os
import sys
from setuptools import setup

kwargs = {}

if sys.version_info[0] == 2:
    dnspython = "dnspython"
elif sys.version_info[0] == 3:
    dnspython = "dnspython3"


def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'pyisemail/version.py')) as f:
        locals = {}
        exec(f.read(), locals)
        return locals['VERSION']
    raise RuntimeError('No version information found.')


def tests_require():
    requirements = [
        "coverage",
        "testtools >= 0.9.21",
        "testscenarios >= 0.3"
    ]

    if sys.version_info[0] < 3:
        requirements.append("mock >= 1.0.1")

    return requirements

setup(
    name="pyIsEmail",
    version=get_version(),
    description="Simple, robust email validation",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=['email', 'validation'],
    author="Michael Herold",
    author_email="michael.j.herold@gmail.com",
    url="https://github.com/michaelherold/pyIsEmail",
    license="MIT",
    packages=["pyisemail", "pyisemail.diagnosis", "pyisemail.validators"],
    include_package_data=True,
    exclude_package_data={
        '': ['.gitignore']
    },
    zip_safe=False,
    install_requires=[
        "%s >= 1.10.0" % dnspython,
    ],
    tests_require=tests_require(),
    test_suite="tests",
    **kwargs
)
