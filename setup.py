__author__ = "Michael Herold"
__copyright__ = "Copyright (c) 2012 Michael Herold"
__license__ = "BSD"

from setuptools import setup, find_packages
from pyisemail.common.version import version

setup(
    name = "pyIsEmail",
    version = version,
    description = "Email format checker based on http://isemail.info",
    long_description = open("README.rst").read(),
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Operating System :: OS Independent"
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Libraries",
    ],
    keywords = "",
    author = "Michael Herold",
    author_email = "michael.j.herold@gmail.com",
    url = "https://github.com/michaelherold/pyIsEmail",
    license = "BSD",
    packages = find_packages(
        exclude = ["*.test", "*.test.*", "test.*", "test"]
    ),
    include_package_data = True,
    exclude_package_data = {
        '': ['.gitignore', '.venv']
    },
    zip_safe = False,
    install_requires = [
        "dnspython >= 1.10.0"
    ],
    setup_requires = ["setuptools-git >= 0.4.2"],
    tests_require = ["testtools >= 0.9.21", "testscenarios >= 0.3"],
    test_suite = "pyisemail.test",
    entry_points = """
    # -*- Entry points: -*-
    """
)
