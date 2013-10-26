from pyisemail.diagnosis import BaseDiagnosis


class DNSDiagnosis(BaseDiagnosis):

    DESCRIPTION = "Address is valid but a DNS check was not successful."

    MESSAGES = {
        'NO_MX_RECORD': ("Couldn't find an MX record for this domain "
                         "but an A record does exist."),
        'NO_RECORD': "Couldn't find an MX record or A record for this domain.",
    }
