from pyisemail.diagnosis import BaseDiagnosis


class GTLDDiagnosis(BaseDiagnosis):

    """A diagnosis indicating that a domain is a disallowed gTLD."""

    DESCRIPTION = "Address uses a gTLD as its domain."

    ERROR_CODES = {"GTLD": 2}

    MESSAGES = {
        "GTLD": (
            "Address has a gTLD as its domain and you "
            "have disallowed those in your check."
        )
    }
