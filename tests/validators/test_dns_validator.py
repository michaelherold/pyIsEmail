import pytest
import dns.name
import dns.resolver
from pyisemail.diagnosis import DNSDiagnosis, RFC5321Diagnosis, ValidDiagnosis
from pyisemail.validators import DNSValidator


is_valid = DNSValidator().is_valid


def no_side_effect(*_):
    return True


def nx_domain_side_effect(*_):
    raise dns.resolver.NXDOMAIN


def too_long_side_effect(*_):
    raise dns.name.NameTooLong


def no_record_side_effect(*_):
    raise dns.resolver.NoAnswer


def no_ns_side_effect(*_):
    raise dns.resolver.NoNameservers


def timeout_side_effect(*_):
    raise dns.resolver.Timeout


def test_working_mx_record_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", no_side_effect)

    assert is_valid("example.com")


def test_working_mx_record_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", no_side_effect)

    assert is_valid("example.com", diagnose=True) == ValidDiagnosis()


def test_non_existant_mx_record_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", nx_domain_side_effect)

    assert not is_valid("example.com")


def test_non_existant_mx_record_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", nx_domain_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("NO_RECORD")


def test_domain_too_long_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", too_long_side_effect)

    assert not is_valid("example.com")


def test_domain_too_long_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", too_long_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("NO_RECORD")


def test_no_record_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", too_long_side_effect)

    assert not is_valid("example.com")


def test_no_record_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", too_long_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("NO_RECORD")


def test_no_mx_on_tld_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", nx_domain_side_effect)

    assert not is_valid("com")


def test_no_mx_on_tld_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", nx_domain_side_effect)

    assert is_valid("com", diagnose=True) == DNSDiagnosis("NO_RECORD")


def test_no_records_on_tld_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", no_record_side_effect)

    assert not is_valid("com")


def test_no_records_on_tld_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", no_record_side_effect)

    assert is_valid("com", diagnose=True) == RFC5321Diagnosis("TLD")


def test_no_records_on_numeric_tld_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", no_record_side_effect)

    assert not is_valid("iana.123")


def test_no_records_on_numeric_tld_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", no_record_side_effect)

    assert is_valid("iana.123", diagnose=True) == RFC5321Diagnosis("TLDNUMERIC")


def test_no_nameservers_respond_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", no_ns_side_effect)

    assert not is_valid("example.com")


def test_no_nameservers_respond_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", no_ns_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("NO_NAMESERVERS")


def test_dns_timeout_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", timeout_side_effect)

    assert not is_valid("example.com")


def test_dns_timeout_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "query", timeout_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("DNS_TIMEDOUT")
