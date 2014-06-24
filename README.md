# pyIsEmail

[![Version](https://pypip.in/v/pyIsEmail/badge.png)][pypi]
[![Travis](https://travis-ci.org/michaelherold/pyIsEmail.png?branch=master)][travis]
[![Coverage](https://coveralls.io/repos/michaelherold/pyIsEmail/badge.png?branch=master)][coveralls]
[![Downloads](https://pypip.in/d/pyIsEmail/badge.png)][pypi]

[bitdeli]: https://bitdeli.com/free
[coveralls]: https://coveralls.io/r/michaelherold/pyIsEmail
[pypi]: https://pypi.python.org/pypi/pyIsEmail/
[travis]: http://travis-ci.org/michaelherold/pyIsEmail

## Getting Started

pyIsEmail is a no-nonsense approach for checking whether that user-supplied
email address could be real. Sick of not being able to use
[email address tagging][tagging] to sort through your [Bacn][bacn]? We can fix
that.

Regular expressions are cheap to write, but often require maintenance when new
top-level domains come out or don't conform to email addressing features that
come back into vogue. pyIsEmail allows you to validate an email address -- and
even check the domain, if you wish -- with one simple call, making your code
more readable and faster to write. When you want to know why an email address
doesn't validate, we even provide you with a diagnosis.

[tagging]: http://en.wikipedia.org/wiki/Email_address#Address_tags
[bacn]: http://en.wikipedia.org/wiki/Bacn

## Install

Install from PyPI using [pip], a package manager for Python.

    $ pip install pyIsEmail

Don't have pip installed? Try installing it, by running this from the command
line:

    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

Or, you can [download the source code (zip)][zipball] for ``pyIsEmail``, and
then run:

    $ python setup.py install

You may need to run the above commands with ``sudo``.

[pip]: http://www.pip-installer.org/en/latest/
[zipball]: https://github.com/michaelherold/pyIsEmail/zipball/develop

## Usage

For the simplest usage, import and use the ``is_email`` function:

```python

from pyisemail import is_email

address = "test@example.com"
bool_result = is_email(address)
detailed_result = is_email(address, diagnose=True)
```

You can also check whether the domain used in the email is a valid domain and
whether or not it has a valid MX record:

```python

from pyisemail import is_email

address = "test@example.com"
bool_result_with_dns = is_email(address, check_dns=True)
detailed_result_with_dns = is_email(address, check_dns=True, diagnose=True)
```

These are primary indicators of whether an email address can even be issued at
that domain. However, a valid response here *is not a guarantee that the email
exists*, merely that is *can* exist.

In addition to the base ``is_email`` functionality, you can also use the
validators by themselves. Check the validator source code to see how this works.

## Uninstall

Want to get rid of pyIsEmail? Did you install with pip? Here you go:

    $ pip uninstall pyIsEmail

## Acknowledgments

The base ``ParserValidator`` is based off of [Dominic Sayers][dominic]'
[is_email script][is_email]. I wanted the functionality in Python, so I ported
it from the original PHP.

[dominic]: https://github.com/dominicsayers
[is_email]: https://github.com/dominicsayers/isemail

## Contributing

1. Fork it
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push to the branch (``git push origin my-new-feature``)
5. Create new Pull Request

## Versioning

This library aims to adhere to [Semantic Versioning 2.0.0][semver]. Violations
of this scheme should be reported as bugs.

[semver]: http://semver.org/

## Copyright

Copyright (c) 2013 Michael Herold. Open sourced under the terms of the
[MIT license][license].

[license]: http://opensource.org/licenses/MIT
