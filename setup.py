__author__ = "Michael Herold"
__copyright__ = "Copyright (c) 2013 Michael Herold"
__license__ = "MIT"

import sys
from setuptools import setup
from pyisemail import __version__

kwargs = {}

with open('README.md') as f:
    long_description = f.read()

if sys.version_info[0] == 2:
    dnspython = "dnspython"
elif sys.version_info[0] == 3:
    dnspython = "dnspython3"

setup(
    name="pyIsEmail",
    version=__version__,
    description="Email format checker based on http://isemail.info",
    long_description=long_description,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent"
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="",
    author="Michael Herold",
    author_email="michael.j.herold@gmail.com",
    url="https://github.com/michaelherold/pyIsEmail",
    license="MIT",
    packages=["pyisemail", "pyisemail.diagnosis", "pyisemail.test"],
    include_package_data=True,
    exclude_package_data={
        '': ['.gitignore']
    },
    zip_safe=False,
    install_requires=[
        "%s >= 1.10.0" % dnspython,
    ],
    tests_require=["testtools >= 0.9.21", "testscenarios >= 0.3"],
    test_suite="pyisemail.test",
    **kwargs
)
