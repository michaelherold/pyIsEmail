__author__ = "Michael Herold"
__copyright__ = "Copyright (c) 2013 Michael Herold"
__license__ = "MIT"

import os
import sys
from setuptools import setup

kwargs = {}

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    try:
        with open('README.md', 'r') as f:
            long_description = f.read()
    except IOError:  # For tox
        long_description = ""

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

setup(
    name="pyIsEmail",
    version=get_version(),
    description="Simple, robust email validation",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
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
    setup_requires=["pypandoc >= 0.7.0"],
    tests_require=["testtools >= 0.9.21", "testscenarios >= 0.3"],
    test_suite="tests",
    **kwargs
)
