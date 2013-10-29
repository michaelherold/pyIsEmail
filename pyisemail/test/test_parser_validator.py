__author__ = "Michael Herold"
__copyright__ = "Copyright (c) 2013 Michael Herold"
__license__ = "MIT"

import xml.etree.ElementTree as ET
from testscenarios import TestWithScenarios
from pyisemail.validators import ParserValidator
from pyisemail.diagnosis import CFWSDiagnosis, DeprecatedDiagnosis
from pyisemail.diagnosis import InvalidDiagnosis, RFC5321Diagnosis
from pyisemail.diagnosis import RFC5322Diagnosis, ValidDiagnosis
from pyisemail.diagnosis import DNSDiagnosis


def get_scenarios():
    """Parses the tests.xml file and returns the scenarios list."""

    document = ET.parse('pyisemail/test/data/tests.xml')
    root = document.getroot()

    scenarios = []

    for test in root.iter('test'):
        id = str(test.attrib['id'])

        attrs = {}
        attrs['id'] = str(test.attrib['id'])
        attrs['address'] = get_node_text(test.find('address').text)
        attrs['diagnosis'] = get_node_text(test.find('diagnosis').text)
        validity = get_node_text(test.find('valid').text)
        if validity == 'True':
            attrs['valid'] = True
        else:
            attrs['valid'] = False

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
    elif tag == "DNSWARN":
        d_class = DNSDiagnosis
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


def get_expected_diagnosis(tag):

    split_tag = tag.split("_")
    d_class = get_diagnosis_class(split_tag[1])
    diagnosis_type = "_".join(split_tag[2:])
    if diagnosis_type == "" and d_class == ValidDiagnosis:
        diagnosis_type = "VALID"

    return d_class(diagnosis_type)


class ParserValidatorTest(TestWithScenarios):

    scenarios = get_scenarios()

    def test_without_diagnosis(self):

        v = ParserValidator()

        result = v.is_email(self.address)
        expected = self.valid

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, self.address, result, expected))
        )

    def test_with_diagnosis(self):

        v = ParserValidator()

        result = v.is_email(self.address, True)
        result = (result == ValidDiagnosis(), result)
        expected = (self.valid, get_expected_diagnosis(self.diagnosis))

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s."
             % (self.id, self.address, result, expected))
        )
