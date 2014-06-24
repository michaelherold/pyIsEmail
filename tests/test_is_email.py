from unittest import expectedFailure
from testscenarios import TestWithScenarios
from pyisemail import is_email
from pyisemail.diagnosis import BaseDiagnosis
from tests.validators import create_diagnosis, get_scenarios


class IsEmailTest(TestWithScenarios):

    scenarios = get_scenarios("tests.xml") + get_scenarios("dns-tests.xml")
    threshold = BaseDiagnosis.CATEGORIES['THRESHOLD']

    def test_without_diagnosis(self):
        result = is_email(self.address, check_dns=True)
        expected = create_diagnosis(self.diagnosis) < self.threshold

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, self.address, result, expected))
        )

    def test_with_diagnosis(self):
        result = is_email(self.address, check_dns=True, diagnose=True)
        expected = create_diagnosis(self.diagnosis)

        try:
            self.assertEqual(
                result,
                expected,
                ("%s (%s): Got %s, but expected %s."
                 % (self.id, self.address, result, expected))
            )
        except AssertionError as err:
            if self.flaky is True:
                pass
            else:
                raise err


class IsEmailFlakyTest(TestWithScenarios):

    """Test suite for flaky is_email tests.

    Due to different DNS servers handling missing domains differently, these
    tests are marked as flaky. A flaky test might succeed in one environment
    and fail in another, purely due to DNS issues. An ideal fix for this
    behavior would be to mock the DNS check to alleviate this problem, but for
    now this will have to do.

    """

    scenarios = (get_scenarios("tests.xml", flaky=True) +
                 get_scenarios("dns-tests.xml", flaky=True))
    threshold = BaseDiagnosis.CATEGORIES['THRESHOLD']

    def test_without_diagnosis(self):
        result = is_email(self.address, check_dns=True)
        expected = create_diagnosis(self.diagnosis) < self.threshold

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, self.address, result, expected))
        )

    @expectedFailure
    def test_with_diagnosis(self):
        result = is_email(self.address, check_dns=True, diagnose=True)
        expected = create_diagnosis(self.diagnosis)

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, self.address, result, expected))
        )
