from testscenarios import TestWithScenarios
from unittest import TestCase
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
import dns.resolver
from pyisemail import is_email
from pyisemail.diagnosis import BaseDiagnosis, DNSDiagnosis
from tests.validators import create_diagnosis, get_scenarios


class IsEmailTest(TestWithScenarios):

    scenarios = get_scenarios("tests.xml")
    threshold = BaseDiagnosis.CATEGORIES['THRESHOLD']

    def test_without_diagnosis(self):
        result = is_email(self.address)
        expected = create_diagnosis(self.diagnosis) < self.threshold

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, self.address, result, expected))
        )

    def test_with_diagnosis(self):
        result = is_email(self.address, diagnose=True)
        expected = create_diagnosis(self.diagnosis)

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
                % (self.id, self.address, result, expected))
        )


@patch('dns.resolver.query', side_effect=dns.resolver.NoAnswer)
class CheckDNSFailureTestCase(TestCase):

    def test_without_diagnosis(self, mocked_method):
        result = is_email('test@example.com', check_dns=True)
        expected = False
        self.assertEqual(result, expected)

    def test_with_diagnosis(self, mocked_method):
        result = is_email('test@example.com', check_dns=True, diagnose=True)
        expected = DNSDiagnosis('NO_RECORD')
        self.assertEqual(result, expected)
