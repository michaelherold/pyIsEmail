from pyisemail.diagnosis import BaseDiagnosis


class RFC5322Diagnosis(BaseDiagnosis):

    DESCRIPTION = ("Address is only valid according to the "
                   "broad definition of RFC5322. It is otherwise invalid.")

    MESSAGES = {
        'DOMAIN': ("Address is RFC5322 compliant but contains domain "
                   "characters that are not allowed by DNS."),
        'TOOLONG': "Address is too long.",
        'LOCAL_TOOLONG': "Address contains a local part that is too long.",
        'DOMAIN_TOOLONG': "Address contains a domain that is too long.",
        'LABEL_TOOLONG': ("Address contains a domain part with an element "
                          "that is too long."),
        'DOMAINLITERAL': ("Address contains a domain literal that is "
                          "not a valid RFC5321 address literal."),
        'DOMLIT_OBSDTEXT': ("Address contains a domain literal that is "
                            "not a valid RFC5321 address literal and "
                            "contains obsolete characters."),
        'IPV6_GRPCOUNT': ("Address contains an IPv6 literal address with "
                          "the wrong number of groups."),
        'IPV6_2X2XCOLON': ("Address contains an IPv6 literal address with "
                           "too many :: sequences."),
        'IPV6_BADCHAR': ("Address contains an IPv6 literal address with "
                         "an illegal group of characters."),
        'IPV6_MAXGRPS': ("Address contains an IPv6 literal address with "
                         "too many groups."),
        'IPV6_COLONSTRT': ("Address contains an IPv6 literal address that "
                           "starts with a single colon."),
        'IPV6_COLONEND': ("Address contains an IPv6 literal address that "
                          "ends with a single colon."),
    }

    REFERENCES = {
        'DOMAIN': ['domain-RFC5322'],
        'TOOLONG': ['mailbox-maximum'],
        'LOCAL_TOOLONG': ['local-part-maximum'],
        'DOMAIN_TOOLONG': ['domain-maximum'],
        'LABEL_TOOLONG': ['label'],
        'DOMAINLITERAL': ['domain-literal'],
        'DOMLIT_OBSDTEXT': ['obs-dtext'],
        'IPV6_GRPCOUNT': ['address-literal-IPv6'],
        'IPV6_2X2XCOLON': ['address-literal-IPv6'],
        'IPV6_BADCHAR': ['address-literal-IPv6'],
        'IPV6_MAXGRPS': ['address-literal-IPv6'],
        'IPV6_COLONSTRT': ['address-literal-IPv6'],
        'IPV6_COLONEND': ['address-literal-IPv6'],
    }
