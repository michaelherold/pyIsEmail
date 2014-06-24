import os
import sys
import xml.etree.ElementTree as ET
from pyisemail.diagnosis import CFWSDiagnosis, DeprecatedDiagnosis
from pyisemail.diagnosis import DNSDiagnosis, InvalidDiagnosis
from pyisemail.diagnosis import RFC5321Diagnosis, RFC5322Diagnosis
from pyisemail.diagnosis import ValidDiagnosis

__all__ = ["create_diagnosis", "get_scenarios"]

if sys.version_info[0] == 3:
    _unicode = str
elif sys.version_info[0] == 2:
    _unicode = unicode


def create_diagnosis(tag):

    """Create a Diagnosis for a given tag.

    Keyword arguments:
    tag --- the tag string to create a Diagnosis for

    """

    split_tag = tag.split("_")
    d_class = _get_diagnosis_class(split_tag[1])
    diagnosis_type = "_".join(split_tag[2:])
    if diagnosis_type == "" and d_class == ValidDiagnosis:
        diagnosis_type = "VALID"

    return d_class(diagnosis_type)


def get_scenarios(filename, flaky=False):

    """Parse the given test file and return the scenarios list.

    Keyword arguments:
    filename --- the name of the test XML file to parse
    flaky    --- flag to include or exclude only flaky tests

    """

    document = ET.parse("%s/../data/%s" % (
        os.path.dirname(__file__), filename))
    root = document.getroot()

    scenarios = []

    for test in root.iter('test'):
        id = str(test.attrib['id'])

        attrs = {}
        attrs['id'] = str(test.attrib['id'])
        attrs['address'] = _get_node_text(test.find('address').text)
        attrs['diagnosis'] = _get_node_text(test.find('diagnosis').text)
        try:
            attrs['flaky'] = _get_node_text(test.find('flaky').text) == "True"
        except AttributeError:
            attrs['flaky'] = False

        if attrs['flaky'] is flaky:
            scenario = (id, attrs)
            scenarios.append(scenario)

    return scenarios


def _get_node_text(text):

    """Cast text to a unicode string to handle unicode characters.

    Keyword arguments:
    text --- the string to cast to unicode

    """

    if text:
        return _unicode(text)
    else:
        return ''


def _get_diagnosis_class(tag):

    """Get class of the Diagnosis to use for a given tag.

    Keyword arguments:
    tag --- the tag string to look up

    """

    if tag == "ERR":
        d_class = InvalidDiagnosis
    elif tag == "DNSWARN":
        d_class = DNSDiagnosis
    elif tag == "VALID":
        d_class = ValidDiagnosis
    elif tag == "RFC5321":
        d_class = RFC5321Diagnosis
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
