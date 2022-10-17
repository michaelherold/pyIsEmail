import pytest

from pyisemail.diagnosis import BaseDiagnosis
from pyisemail.validators import ParserValidator
from tests.validators import create_diagnosis, get_scenarios

scenarios = get_scenarios("tests.xml")
threshold = BaseDiagnosis.CATEGORIES["THRESHOLD"]


@pytest.mark.parametrize("test_id,address,diagnosis", scenarios)
def test_without_diagnosis(test_id, address, diagnosis):

    v = ParserValidator()

    result = v.is_email(address)
    expected = create_diagnosis(diagnosis) < threshold

    assert result == expected, "%s (%s): Got %s, but expected %s." % (
        test_id,
        address,
        result,
        expected,
    )


@pytest.mark.parametrize("test_id,address,diagnosis", scenarios)
def test_with_diagnosis(test_id, address, diagnosis):

    v = ParserValidator()

    result = v.is_email(address, True)
    expected = create_diagnosis(diagnosis)

    assert result == expected, "%s (%s): Got %s, but expected %s." % (
        test_id,
        address,
        result,
        expected,
    )
