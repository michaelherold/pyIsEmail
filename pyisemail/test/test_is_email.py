__author__ = "Michael Herold"
__copyright__ = "Copyright (c) 2013 Michael Herold"
__license__ = "MIT"

import xml.etree.ElementTree as ET
from pyisemail.is_email import is_email
from testscenarios import TestWithScenarios

# Categories
ISEMAIL_VALID_CATEGORY = 1
ISEMAIL_DNSWARN = 7
ISEMAIL_RFC5321 = 15
ISEMAIL_CFWS = 31
ISEMAIL_DEPREC = 63
ISEMAIL_RFC5322 = 127
ISEMAIL_ERR = 255

# Diagnoses
# Address is valid
ISEMAIL_VALID = 0
# Address is valid but a DNS check was not successful
ISEMAIL_DNSWARN_NO_MX_RECORD = 5
ISEMAIL_DNSWARN_NO_RECORD = 6
# Address is valid for SMTP but has unusual elements
ISEMAIL_RFC5321_TLD = 9
ISEMAIL_RFC5321_TLDNUMERIC = 10
ISEMAIL_RFC5321_QUOTEDSTRING = 11
ISEMAIL_RFC5321_ADDRESSLITERAL = 12
ISEMAIL_RFC5321_IPV6DEPRECATED = 13
# Address is valid within the message but cannot be used unmodified for the
# envelope
ISEMAIL_CFWS_COMMENT = 17
ISEMAIL_CFWS_FWS = 18
# Address contains deprecated elements but may still be valid in restricted
# contexts
ISEMAIL_DEPREC_LOCALPART = 33
ISEMAIL_DEPREC_FWS = 34
ISEMAIL_DEPREC_QTEXT = 35
ISEMAIL_DEPREC_QP = 36
ISEMAIL_DEPREC_COMMENT = 37
ISEMAIL_DEPREC_CTEXT = 38
ISEMAIL_DEPREC_CFWS_NEAR_AT = 49
# The address is only valid according to the broad definition of RFC 5322.
# It is otherwise invalid.
ISEMAIL_RFC5322_DOMAIN = 65
ISEMAIL_RFC5322_TOOLONG = 66
ISEMAIL_RFC5322_LOCAL_TOOLONG = 67
ISEMAIL_RFC5322_DOMAIN_TOOLONG = 68
ISEMAIL_RFC5322_LABEL_TOOLONG = 69
ISEMAIL_RFC5322_DOMAINLITERAL = 70
ISEMAIL_RFC5322_DOMLIT_OBSDTEXT = 71
ISEMAIL_RFC5322_IPV6_GRPCOUNT = 72
ISEMAIL_RFC5322_IPV6_2X2XCOLON = 73
ISEMAIL_RFC5322_IPV6_BADCHAR = 74
ISEMAIL_RFC5322_IPV6_MAXGRPS = 75
ISEMAIL_RFC5322_IPV6_COLONSTRT = 76
ISEMAIL_RFC5322_IPV6_COLONEND = 77
# Address is invalid for any purpose
ISEMAIL_ERR_EXPECTING_DTEXT = 129
ISEMAIL_ERR_NOLOCALPART = 130
ISEMAIL_ERR_NODOMAIN = 131
ISEMAIL_ERR_CONSECUTIVEDOTS = 132
ISEMAIL_ERR_ATEXT_AFTER_CFWS = 133
ISEMAIL_ERR_ATEXT_AFTER_QS = 134
ISEMAIL_ERR_ATEXT_AFTER_DOMLIT = 135
ISEMAIL_ERR_EXPECTING_QPAIR = 136
ISEMAIL_ERR_EXPECTING_ATEXT = 137
ISEMAIL_ERR_EXPECTING_QTEXT = 138
ISEMAIL_ERR_EXPECTING_CTEXT = 139
ISEMAIL_ERR_BACKSLASHEND = 140
ISEMAIL_ERR_DOT_START = 141
ISEMAIL_ERR_DOT_END = 142
ISEMAIL_ERR_DOMAINHYPHENSTART = 143
ISEMAIL_ERR_DOMAINHYPHENEND = 144
ISEMAIL_ERR_UNCLOSEDQUOTEDSTR = 145
ISEMAIL_ERR_UNCLOSEDCOMMENT = 146
ISEMAIL_ERR_UNCLOSEDDOMLIT = 147
ISEMAIL_ERR_FWS_CRLF_X2 = 148
ISEMAIL_ERR_FWS_CRLF_END = 149
ISEMAIL_ERR_CR_NO_LF = 150

# function control
ISEMAIL_THRESHOLD = 16

# Email parts
ISEMAIL_COMPONENT_LOCALPART = 0
ISEMAIL_COMPONENT_DOMAIN = 1
ISEMAIL_COMPONENT_LITERAL = 2
ISEMAIL_CONTEXT_COMMENT = 3
ISEMAIL_CONTEXT_FWS = 4
ISEMAIL_CONTEXT_QUOTEDSTRING = 5
ISEMAIL_CONTEXT_QUOTEDPAIR = 6

# Miscellaneous string constants
ISEMAIL_STRING_AT = '@'
ISEMAIL_STRING_BACKSLASH = '\\'
ISEMAIL_STRING_DOT = '.'
ISEMAIL_STRING_DQUOTE = '"'
ISEMAIL_STRING_OPENPARENTHESIS = '('
ISEMAIL_STRING_CLOSEPARENTHESIS = ')'
ISEMAIL_STRING_OPENSQBRACKET = '['
ISEMAIL_STRING_CLOSESQBRACKET = ']'
ISEMAIL_STRING_HYPHEN = '-'
ISEMAIL_STRING_COLON = ':'
ISEMAIL_STRING_DOUBLECOLON = '::'
ISEMAIL_STRING_SP = ' '
ISEMAIL_STRING_HTAB = "\t"
ISEMAIL_STRING_CR = "\r"
ISEMAIL_STRING_LF = "\n"
ISEMAIL_STRING_IPV6TAG = 'IPv6:'
# US-ASCII visible characters not valid for atext
# (http:#tools.ietf.org/html/rfc5322#section-3.2.3)
ISEMAIL_STRING_SPECIALS = '()<>[]:;@\\,."'


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
        attrs['category'] = get_node_text(test.find('category').text)
        attrs['diagnosis'] = get_node_text(test.find('diagnosis').text)
        attrs['source'] = get_node_text(test.find('source').text)
        attrs['source_link'] = get_node_text(test.find('sourcelink').text)

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

    def test_is_email(self):

        p = {}

        result = is_email(self.address, True, True, p)
        diagnosis = eval(self.diagnosis)

        self.assertEqual(
            result,
            diagnosis,
            ("%s (%s): Got %s, but expected %s. (%s)"
             % (self.id, self.address, result, diagnosis, str(p)))
        )
