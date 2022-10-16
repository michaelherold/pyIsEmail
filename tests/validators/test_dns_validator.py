import time
import dns.name
import dns.resolver
import pytest
from pyisemail.diagnosis import DNSDiagnosis, RFC5321Diagnosis, ValidDiagnosis
from pyisemail.validators import DNSValidator

is_valid = DNSValidator().is_valid

message_text_null_mx = """id 1234
opcode QUERY
rcode NOERROR
flags QR AA RD
;QUESTION
example.com. IN MX
;ANSWER
example.com. 86400   IN  MX  0 .
;AUTHORITY
;ADDITIONAL
"""

message_text_zero_preference = """id 1234
opcode QUERY
rcode NOERROR
flags QR AA RD
;QUESTION
example.com. IN MX
;ANSWER
example.com. 86400   IN  MX  0 mail.example.com.
;AUTHORITY
;ADDITIONAL
"""


class FakeAnswer(object):
    def __init__(self, expiration):
        self.expiration = expiration

    def __len__(self):
        return 2


def null_mx_record(*_):
    message = dns.message.from_text(message_text_null_mx)
    name = dns.name.from_text("example.com.")

    return dns.resolver.Answer(name, dns.rdatatype.MX, dns.rdataclass.IN, message)


def zero_preference_mx_record(*_):
    message = dns.message.from_text(message_text_zero_preference)
    name = dns.name.from_text("example.com.")

    return dns.resolver.Answer(name, dns.rdatatype.MX, dns.rdataclass.IN, message)


def no_side_effect(*_):
    return FakeAnswer(time.time() + 1)


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
    monkeypatch.setattr(dns.resolver, "resolve", no_side_effect)

    assert is_valid("example.com")


def test_working_mx_record_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", no_side_effect)

    assert is_valid("example.com", diagnose=True) == ValidDiagnosis()


def test_non_existant_mx_record_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", nx_domain_side_effect)

    assert not is_valid("example.com")


def test_non_existant_mx_record_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", nx_domain_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("NO_RECORD")


def test_domain_too_long_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", too_long_side_effect)

    assert not is_valid("example.com")


def test_domain_too_long_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", too_long_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("NO_RECORD")


def test_no_record_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", too_long_side_effect)

    assert not is_valid("example.com")


def test_no_record_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", too_long_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("NO_RECORD")


def test_no_mx_on_tld_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", nx_domain_side_effect)

    assert not is_valid("com")


def test_no_mx_on_tld_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", nx_domain_side_effect)

    assert is_valid("com", diagnose=True) == DNSDiagnosis("NO_RECORD")


def test_no_records_on_tld_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", no_record_side_effect)

    assert not is_valid("com")


def test_no_records_on_tld_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", no_record_side_effect)

    assert is_valid("com", diagnose=True) == RFC5321Diagnosis("TLD")


def test_no_records_on_numeric_tld_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", no_record_side_effect)

    assert not is_valid("iana.123")


def test_no_records_on_numeric_tld_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", no_record_side_effect)

    assert is_valid("iana.123", diagnose=True) == RFC5321Diagnosis("TLDNUMERIC")


def test_no_nameservers_respond_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", no_ns_side_effect)

    assert not is_valid("example.com")


def test_no_nameservers_respond_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", no_ns_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("NO_NAMESERVERS")


def test_dns_timeout_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", timeout_side_effect)

    assert not is_valid("example.com")


def test_dns_timeout_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", timeout_side_effect)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("DNS_TIMEDOUT")


def test_null_mx_record_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", null_mx_record)

    assert not is_valid("example.com")


def test_null_mx_record_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", null_mx_record)

    assert is_valid("example.com", diagnose=True) == DNSDiagnosis("NULL_MX_RECORD")


def test_zero_preference_mx_record_without_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", zero_preference_mx_record)

    assert is_valid("example.com")


def test_zero_preference_mx_record_with_diagnosis(monkeypatch):
    monkeypatch.setattr(dns.resolver, "resolve", zero_preference_mx_record)

    assert is_valid("example.com", diagnose=True) == ValidDiagnosis()
