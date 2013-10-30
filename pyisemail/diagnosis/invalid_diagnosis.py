from pyisemail.diagnosis import BaseDiagnosis


class InvalidDiagnosis(BaseDiagnosis):

    """A diagnosis indicating the presence of an invalid address component.

    """

    DESCRIPTION = "Address is invalid for any purpose"

    ERROR_CODES = {
        'EXPECTING_DTEXT': 129,
        'NOLOCALPART': 130,
        'NODOMAIN': 131,
        'CONSECUTIVEDOTS': 132,
        'ATEXT_AFTER_CFWS': 133,
        'ATEXT_AFTER_QS': 134,
        'ATEXT_AFTER_DOMLIT': 135,
        'EXPECTING_QPAIR': 136,
        'EXPECTING_ATEXT': 137,
        'EXPECTING_QTEXT': 138,
        'EXPECTING_CTEXT': 139,
        'BACKSLASHEND': 140,
        'DOT_START': 141,
        'DOT_END': 142,
        'DOMAINHYPHENSTART': 143,
        'DOMAINHYPHENEND': 144,
        'UNCLOSEDQUOTEDSTR': 145,
        'UNCLOSEDCOMMENT': 146,
        'UNCLOSEDDOMLIT': 147,
        'FWS_CRLF_X2': 148,
        'FWS_CRLF_END': 149,
        'CR_NO_LF': 150,
        'BAD_PARSE': 151,
    }

    MESSAGES = {
        'EXPECTING_DTEXT': ("Address contains a character that is "
                            "not allowed in a domain literal."),
        'NOLOCALPART': "Address has no local part.",
        'NODOMAIN': "Address has no domain part.",
        'CONSECUTIVEDOTS': "Address contains consecutive dots.",
        'ATEXT_AFTER_CFWS': ("Address contains text after a comment "
                             "or Folding White Space."),
        'ATEXT_AFTER_QS': "Address contains text after a quoted string.",
        'ATEXT_AFTER_DOMLIT': ("Address contains extra characters "
                               "after the domain literal."),
        'EXPECTING_QPAIR': ("Address contains a character that is "
                            "not allowed in a quoted pair."),
        'EXPECTING_ATEXT': "Address contains a character that is not allowed.",
        'EXPECTING_QTEXT': ("Address contains a character that is "
                            "not allowed in a quoted string."),
        'EXPECTING_CTEXT': ("Address contains a character that is "
                            "not allowed in a comment."),
        'BACKSLASHEND': "Address ends in a backslash.",
        'DOT_START': ("Address has a local part or domain "
                      "that begins with a dot."),
        'DOT_END': ("Address has a local part or domain "
                    "that ends with a dot."),
        'DOMAINHYPHENSTART': ("Address has a local part or domain "
                              "that begins with a hyphen."),
        'DOMAINHYPHENEND': ("Address has a local part or domain "
                            "that ends with a hyphen."),
        'UNCLOSEDQUOTEDSTR': "Address contains an unclosed quoted string.",
        'UNCLOSEDCOMMENT': "Address contains an unclosed comment.",
        'UNCLOSEDDOMLIT': ("Address contains a domain literal "
                           "that is missing its closing bracket."),
        'FWS_CRLF_X2': ("Address contains a Folding White Space "
                        "that has consecutive CRLF sequences."),
        'FWS_CRLF_END': ("Address contains a Folding White Space "
                         "that ends with a CRLF sequence."),
        'CR_NO_LF': ("Address contains a carriage return "
                     "that is not followed by a line return."),
        'BAD_PARSE': "Address is malformed.",
    }

    REFERENCES = {
        'EXPECTING_DTEXT': ['dtext'],
        'NOLOCALPART': ['local-part'],
        'NODOMAIN': ['addr-spec', 'mailbox'],
        'CONSECUTIVEDOTS': ['local-part', 'domain-RFC5322', 'domain-RFC5321'],
        'ATEXT_AFTER_CFWS': ['local-part', 'domain-RFC5322'],
        'ATEXT_AFTER_QS': ['local-part'],
        'ATEXT_AFTER_DOMLIT': ['domain-RFC5322'],
        'EXPECTING_QPAIR': ['quoted-pair'],
        'EXPECTING_ATEXT': ['atext'],
        'EXPECTING_QTEXT': ['qtext'],
        'EXPECTING_CTEXT': ['ctext'],
        'BACKSLASHEND': ['domain-RFC5322', 'domain-RFC5321', 'quoted-pair'],
        'DOT_START': ['local-part', 'domain-RFC5322', 'domain-RFC5321'],
        'DOT_END': ['local-part', 'domain-RFC5322', 'domain-RFC5321'],
        'DOMAINHYPHENSTART': ['sub-domain'],
        'DOMAINHYPHENEND': ['sub-domain'],
        'UNCLOSEDQUOTEDSTR': ['quoted-string'],
        'UNCLOSEDCOMMENT': ['CFWS'],
        'UNCLOSEDDOMLIT': ['domain-literal'],
        'FWS_CRLF_X2': ['CFWS'],
        'FWS_CRLF_END': ['CFWS'],
        'CR_NO_LF': ['CFWS', 'CRLF'],
        'BAD_PARSE': [],
    }
