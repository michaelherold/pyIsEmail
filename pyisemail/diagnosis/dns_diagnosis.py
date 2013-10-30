from pyisemail.diagnosis import BaseDiagnosis


class DNSDiagnosis(BaseDiagnosis):

    """A diagnosis indicating a lack of a DNS record for a domain.

    """

    DESCRIPTION = "Address is valid but a DNS check was not successful."

    ERROR_CODES = {
        'NO_MX_RECORD': 5,
        'NO_RECORD': 6,
    }

    MESSAGES = {
        'NO_MX_RECORD': ("Couldn't find an MX record for this domain "
                         "but an A record does exist."),
        'NO_RECORD': "Couldn't find an MX record or A record for this domain.",
    }
