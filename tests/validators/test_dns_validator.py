from unittest import expectedFailure
from testscenarios import TestWithScenarios
from pyisemail.diagnosis import ValidDiagnosis
from pyisemail.validators import DNSValidator
from tests.validators import create_diagnosis, get_scenarios


class DNSValidatorTest(TestWithScenarios):

    scenarios = get_scenarios("dns-tests.xml")

    def test_without_diagnosis(self):

        v = DNSValidator()

        domain = self.address.split("@")[1]
        result = v.is_valid(domain)
        expected = create_diagnosis(self.diagnosis) == ValidDiagnosis()

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, domain, result, expected))
        )

    def test_with_diagnosis(self):

        v = DNSValidator()

        domain = self.address.split("@")[1]
        result = v.is_valid(domain, True)
        expected = create_diagnosis(self.diagnosis)

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, domain, result, expected))
        )


class DNSValidatorFlakyTest(TestWithScenarios):

    """Test suite for flaky DNSValidator tests.

    Due to different DNS servers handling missing domains differently, these
    tests are marked as flaky. A flaky tests might succeed in one environment
    and fail in another, purely due to DNS issues. An ideal fix for this
    behavior would be to mock the DNS check to alleviate this problem, but for
    now this will have to do.

    """

    scenarios = get_scenarios("dns-tests.xml", flaky=True)

    @expectedFailure
    def test_without_diagnosis(self):

        v = DNSValidator()

        domain = self.address.split("@")[1]
        result = v.is_valid(domain)
        expected = create_diagnosis(self.diagnosis) == ValidDiagnosis()

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, domain, result, expected))
        )

    @expectedFailure
    def test_with_diagnosis(self):

        v = DNSValidator()

        domain = self.address.split("@")[1]
        result = v.is_valid(domain, True)
        expected = create_diagnosis(self.diagnosis)

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, domain, result, expected))
        )
