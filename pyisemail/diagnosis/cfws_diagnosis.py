from pyisemail.diagnosis import BaseDiagnosis


class CFWSDiagnosis(BaseDiagnosis):

    """A diagnosis indicating a problem with white space in the address.

    """

    DESCRIPTION = ("Address is valid within the message "
                   "but cannot be used unmodified for the envelope.")

    ERROR_CODES = {
        'COMMENT': 17,
        'FWS': 18,
    }

    MESSAGES = {
        'COMMENT': "Address contains messages",
        'FWS': "Address contains Folding White Space",
    }

    REFERENCES = {
        'COMMENT': ['dot-atom'],
        'FWS': ['local-part'],
    }
