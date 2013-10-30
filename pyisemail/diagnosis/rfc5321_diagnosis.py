from pyisemail.diagnosis import BaseDiagnosis


class RFC5321Diagnosis(BaseDiagnosis):

    """A diagnosis indicating the address is only valid for SMTP.

    """

    DESCRIPTION = "Address is valid for SMTP but has unusual elements."

    ERROR_CODES = {
        'TLD': 9,
        'TLDNUMERIC': 10,
        'QUOTEDSTRING': 11,
        'ADDRESSLITERAL': 12,
        'IPV6DEPRECATED': 13,
    }

    MESSAGES = {
        'TLD': "Address is valid but at a Top Level Domain.",
        'TLDNUMERIC': ("Address is valid but the Top Level Domain "
                       "begins with a number."),
        'QUOTEDSTRING': "Address is valid but contains a quoted string.",
        'ADDRESSLITERAL': ("Address is valid but at a literal address, "
                           "not a domain."),
        'IPV6DEPRECATED': ("Address is valid but contains a :: that "
                           "only elides one zero group."),
    }

    REFERENCES = {
        'TLD': ['TLD'],
        'TLDNUMERIC': ['TLD-format'],
        'QUOTEDSTRING': ['quoted-string'],
        'ADDRESSLITERAL': ['address-literal', 'address-literal-IPv4'],
        'IPV6DEPRECATED': ['address-literal-IPv6'],
    }
