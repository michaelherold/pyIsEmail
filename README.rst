pyIsEmail
=========

|pypi| |travis| |coveralls| |downloads|

Getting Started
---------------

pyIsEmail is a no-nonsense approach for checking whether that
user-supplied email address could be real. Sick of not being able to use
`email address tagging`_ to sort through your `Bacn`_? We can fix that.

Regular expressions are cheap to write, but often require maintenance when
new top-level domains come out or don't conform to email addressing
features that come back into vogue. pyIsEmail allows you to validate an
email address -- and even check the domain, if you wish -- with one simple
call, making your code more readable and faster to write. When you want to
know why an email address doesn't validate, we even provide you with
a diagnosis.

.. _email address tagging: http://en.wikipedia.org/wiki/Email_address#Address_tags
.. _Bacn: http://en.wikipedia.org/wiki/Bacn

Install
-------

Install from PyPI using `pip`_, a package manager for Python.

.. code-block:: bash

    $ pip install pyIsEmail

Don't have pip installed? Try installingit by running this from the
command line:

.. code-block:: bash

    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

Or you can `download the source code (zip)`_ for ``pyIsEmail`` and then
run:

.. code-block:: bash

    $ python setup.py install

You may need to run the above commands with ``sudo``.

.. _pip: http://www.pip-installer.org/en/latest/
.. _download the source code (zip): https://github.com/michaelherold/pyIsEmail/zipball/master

Usage
-----

For the simplest usage, import and use the ``is_email`` function:

.. code-block:: python

    from pyisemail import is_email

    address = "test@example.com"
    bool_result = is_email(address)
    detailed_result = is_email(address, diagnose=True)

You can also check whether the domain used in the email is a valid domain
and whether or not it has a valid MX record:

.. code-block:: python

    from pyisemail import is_email

    address = "test@example.com"
    bool_result_with_dns = is_email(address, check_dns=True)
    detailed_result_with_dns = is_email(address, check_dns=True, diagnose=True)

These are primary indicators of whether an email address can even be
issued at that domain. However, a valid response here *is not a guarantee
that the email exists*, merely that is *can* exist.

In addition to the base ``is_email`` functionality, you can also use the
validators by themselves. Check the validator source doe to see how this
works.

Uninstall
---------

Want to get rid of pyIsEmail? Did you install with pip? Here you go:

.. code-block:: bash

    $ pip uninstall pyIsEmail

Acknowledgements
----------------

The base ``ParserValidator`` is based off of `Dominic Sayers`_' `is_email
script`_. I wanted the functionality in Python, so I ported it from the
original PHP.

.. _Dominic Sayers: https://github.com/dominicsayers
.. _is_email script: https://github.com/dominicsayers/isemail

Contributing
------------

1. Fork it
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push to the branch (``git push origin my-new-feature``)
5. Create a new Pull Request

Versioning
----------

This library aims to adhere to `Semantic Versioning 2.0.0`_. Violations of
this scheme should be reported as bugs.

.. _Semantic Versioning 2.0.0: http://semver.org/

Copyright
---------

Copyright (c) 2015 Michael Herold. Open sourced under the terms of the
`MIT license`_.

.. _MIT license: http://opensource.org/licenses/MIT


.. |pypi| image:: https://img.shields.io/pypi/v/pyIsEmail.svg?style=flat-square
   :target: https://pypi.python.org/pypi/pyIsEmail
   :alt: Latest version released on PyPI
.. |travis| image:: https://img.shields.io/travis/michaelherold/pyIsEmail/master.svg?style=flat-square
   :target: http://travis-ci.org/michaelherold/pyIsEmail
.. |coveralls| image:: https://img.shields.io/coveralls/michaelherold/pyIsEmail/master.svg?style=flat-square
   :target: https://coveralls.io/r/michaelherold/pyIsEmail?branch=master
   :alt: Test coverage
.. |downloads| image:: https://img.shields.io/pypi/dm/pyIsEmail.svg?style=flat-square
   :target: https://pypi.python.org/pypi/pyIsEmail/
