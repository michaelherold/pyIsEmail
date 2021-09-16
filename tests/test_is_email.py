import pytest

import dns.resolver
from pyisemail import is_email
from pyisemail.diagnosis import (
    BaseDiagnosis,
    DNSDiagnosis,
    GTLDDiagnosis,
    ValidDiagnosis,
)
from tests.validators import create_diagnosis, get_scenarios

scenarios = get_scenarios("tests.xml")
threshold = BaseDiagnosis.CATEGORIES["THRESHOLD"]


def side_effect(*_):
    raise dns.resolver.NoAnswer


@pytest.mark.parametrize("test_id,address,diagnosis", scenarios)
def test_without_diagnosis(test_id, address, diagnosis):
    result = is_email(address)
    expected = create_diagnosis(diagnosis) < threshold

    assert result == expected, "%s (%s): Got %s, but expected %s." % (
        test_id,
        address,
        result,
        expected,
    )


@pytest.mark.parametrize("test_id,address,diagnosis", scenarios)
def test_with_diagnosis(test_id, address, diagnosis):
    result = is_email(address, diagnose=True)
    expected = create_diagnosis(diagnosis)

    assert result == expected, "%s (%s): Got %s, but expected %s." % (
        test_id,
        address,
        result,
        expected,
    )


def test_dns_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", side_effect)

    result = is_email("test@example.com", check_dns=True)
    expected = False

    assert result == expected


def test_dns_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", side_effect)

    result = is_email("test@example.com", check_dns=True, diagnose=True)
    expected = DNSDiagnosis("NO_RECORD")

    assert result == expected


def test_gtld_with_diagnosis():
    assert is_email("a@b") == True
    assert is_email("a@b", allow_gtld=False) == False


def test_gtld_without_diagnosis():
    assert is_email("a@b", diagnose=True) == ValidDiagnosis()
    assert is_email("a@b", allow_gtld=False, diagnose=True) == GTLDDiagnosis("GTLD")
