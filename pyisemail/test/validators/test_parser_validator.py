import os
import xml.etree.ElementTree as ET
from testscenarios import TestWithScenarios
from pyisemail.diagnosis import CFWSDiagnosis, DeprecatedDiagnosis, BaseDiagnosis
from pyisemail.diagnosis import InvalidDiagnosis, RFC5321Diagnosis
from pyisemail.diagnosis import RFC5322Diagnosis, ValidDiagnosis
from pyisemail.validators import ParserValidator


def get_scenarios():
    """Parses the tests.xml file and returns the scenarios list."""

    document = ET.parse("%s/../data/tests.xml" % os.path.dirname(__file__))
    root = document.getroot()

    scenarios = []

    for test in root.iter('test'):
        id = str(test.attrib['id'])

        attrs = {}
        attrs['id'] = str(test.attrib['id'])
        attrs['address'] = get_node_text(test.find('address').text)
        attrs['diagnosis'] = get_node_text(test.find('diagnosis').text)

        scenario = (id, attrs)

        scenarios.append(scenario)

    return scenarios


def get_node_text(text):

    """Ensures that we have a string from the XML document."""

    if text:
        return unicode(text)
    else:
        return ''


def get_diagnosis_class(tag):

    if tag == "ERR":
        d_class = InvalidDiagnosis
    elif tag == "VALID":
        d_class = ValidDiagnosis
    elif tag == "RFC5321":
        d_class = RFC5321Diagnosis
    elif tag == "RFC5322":
        d_class = RFC5322Diagnosis
    elif tag == "CFWS":
        d_class = CFWSDiagnosis
    elif tag == "DEPREC":
        d_class = DeprecatedDiagnosis
    else:
        d_class = ""

    return d_class


def create_diagnosis(tag):

    split_tag = tag.split("_")
    d_class = get_diagnosis_class(split_tag[1])
    diagnosis_type = "_".join(split_tag[2:])
    if diagnosis_type == "" and d_class == ValidDiagnosis:
        diagnosis_type = "VALID"

    return d_class(diagnosis_type)


class ParserValidatorTest(TestWithScenarios):

    scenarios = get_scenarios()
    threshold = BaseDiagnosis.CATEGORIES['THRESHOLD']

    def test_without_diagnosis(self):

        v = ParserValidator()

        result = v.is_email(self.address)
        expected = create_diagnosis(self.diagnosis) < self.threshold

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, self.address, result, expected))
        )

    def test_with_diagnosis(self):

        v = ParserValidator()

        result = v.is_email(self.address, True)
        expected = create_diagnosis(self.diagnosis)

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, self.address, result, expected))
        )
