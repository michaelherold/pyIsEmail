import pytest
from pyisemail import EmailValidator


def test_abstract_is_email():
    v = EmailValidator()

    with pytest.raises(NotImplementedError):
        v.is_email("test@example.com")
