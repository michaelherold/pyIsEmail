__author__ = "Michael Herold"
__copyright__ = "Copyright (c) 2015 Michael Herold"
__license__ = "MIT"

import os
import sys
from setuptools import setup

kwargs = {}


def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "pyisemail/version.py")) as f:
        locals = {}
        exec(f.read(), locals)
        return locals["VERSION"]
    raise RuntimeError("No version information found.")


setup(
    name="pyIsEmail",
    version=get_version(),
    description="Simple, robust email validation",
    long_description=open("README.rst").read(),
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
    keywords=["email", "validation"],
    author="Michael Herold",
    author_email="opensource@michaeljherold.com",
    url="https://github.com/michaelherold/pyIsEmail",
    license="MIT",
    packages=["pyisemail", "pyisemail.diagnosis", "pyisemail.validators"],
    include_package_data=True,
    exclude_package_data={"": [".gitignore"]},
    zip_safe=False,
    install_requires=[
        "dnspython >= 2.0.0",
    ],
    tests_require=["coverage", "pytest"],
    test_suite="tests",
    **kwargs
)
