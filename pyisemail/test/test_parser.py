__author__ = "Michael Herold"
__copyright__ = "Copyright (c) 2013 Michael Herold"
__license__ = "MIT"

import xml.etree.ElementTree as ET
from pyisemail.parser import Parser
from testscenarios import TestWithScenarios


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
        attrs['valid'] = get_node_text(test.find('valid').text) == "True"

        scenario = (id, attrs)

        scenarios.append(scenario)

    return scenarios


def get_node_text(text):

    """Ensures that we have a string from the XML document."""

    if text:
        return unicode(text)
    else:
        return ''


class ParseTestCase(TestWithScenarios):

    scenarios = get_scenarios()

    def test_parser(self):

        p = Parser()

        result = p.parse(self.address)
        expected = self.valid

        self.assertEqual(
            result,
            expected,
            ("%s (%s): Got %s, but expected %s. (%s)"
             % (self.id, self.address, result, expected, str(p)))
        )
