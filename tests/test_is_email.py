from testscenarios import TestWithScenarios
from pyisemail import is_email
from pyisemail.diagnosis import BaseDiagnosis
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
