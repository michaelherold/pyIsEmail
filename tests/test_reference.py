import pytest

from pyisemail import Reference


def test_reference_repr():
    r = Reference("local-part")

    result = repr(r)
    expected = "%s (%r)" % (r.__class__, r.__dict__)

    assert result == expected


def test_reference_str():
    r = Reference("local-part")

    result = str(r)
    expected = "%s <%s>" % (r.citation, r.link)

    assert result == expected
