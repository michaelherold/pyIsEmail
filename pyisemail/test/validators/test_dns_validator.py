from testscenarios import TestWithScenarios
from pyisemail.diagnosis import ValidDiagnosis
from pyisemail.test.validators import create_diagnosis, get_scenarios
from pyisemail.validators.dns_validator import DNSValidator


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
