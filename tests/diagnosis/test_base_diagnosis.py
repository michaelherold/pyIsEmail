import pytest

from pyisemail.diagnosis import BaseDiagnosis


def test_diagnosis_less_than():
    d1 = BaseDiagnosis("test")
    d1.code = 1
    d2 = BaseDiagnosis("test")
    d2.code = 2

    assert d1 < d2
    assert d1 < 3


def test_diagnosis_greater_than():
    d1 = BaseDiagnosis("test")
    d1.code = 1
    d2 = BaseDiagnosis("test")
    d2.code = 2

    assert d2 > d1
    assert 3 > d1


def test_diagnosis_equal_to():
    d1 = BaseDiagnosis("test")
    d1.code = 1
    d2 = BaseDiagnosis("test")
    d2.code = 1

    assert d1 == d2


def test_diagnosis_hash():
    d1 = BaseDiagnosis("test")
    d2 = BaseDiagnosis("test")

    assert hash(d1) == hash(d2)
