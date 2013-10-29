pyIsEmail
=========

|Build Status| |Coverage Status|

pyIsEmail is a simple egg that provides robust checking for email formatting,
based on the work of Dominic Sayers at http://isemail.info.

.. |Build Status| image::https://travis-ci.org/michaelherold/pyIsEmail.png?branch=develop
   :target: http://travis-ci.org/michaelherold/pyIsEmail
.. |Coverage Status| image:: https://coveralls.io/repos/michaelherold/pyIsEmail/badge.png?branch=develop
   :target: https://coveralls.io/r/michaelherold/pyIsEmail

Installation
------------

Install from PyPI using `pip`_, a package manager for Python.

::
    $ pip install pyIsEmail

Don't have pip installed? Try installing it, by running this from the command
line:

::
    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

Or, you can `download the source code (zip)`_ for ``pyIsEmail``, and then run:

::
    $ python setup.py install

You may need to run the above commands with ``sudo``.
.. _pip: http://www.pip-installer.org/en/latest/
.. _download the source code (zip): https://github.com/michaelherold/pyIsEmail/zipball/develop

Usage
-----

For the simplest usage, import and use the ``is_email`` function:

.. code::python

    from pyisemail import is_email

    address = "test@example.com"
    bool_result = is_email(address)
    detailed_result = is_email(address, diagnose=True)

You can also check whether the domain used in the email is a valid domain and
whether or not it has a valid MX record:

.. code::python

    from pyisemail import is_email

    address = "test@example.com"
    bool_result_with_dns = is_email(address, check_dns=True)
    detailed_result_with_dns = is_email(address, check_dns=True, diagnose=True)

These are primary indicators of whether an email address can even be issued at
that domain. However, a valid response here *is not a guarantee that the email
exists*, merely that is *can* exist.

In addition to the base ``is_email`` functionality, you can also use the
validators by themselves. Check the validator source code to see how this works.

Acknowledgments
---------------

The base ``ParserValidator`` is based off of `Dominic Sayers' is_email script`_.
I wanted the functionality in Python, so I ported it from PHP.

.. _Dominic Sayers' is_email script: https://github.com/dominicsayers/isemail

Contributing
------------

1. Fork it
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push to the branch (``git push origin my-new-feature``)
5. Create new Pull Request

Versioning
----------

This library aims to adhere to `Semantic Versioning 2.0.0`_. Violations of this
scheme should be reported as bugs.

:: _Semantic Versioning 2.0.0: http://semver.org/

Copyright
---------

Copyright (c) 2013 Michael Herold. See LICENSE for details.