from pyisemail.diagnosis import GTLDDiagnosis, ValidDiagnosis


class GTLDValidator(object):
    def is_valid(self, domain, diagnose=False):

        """Check whether a domain is a gTLD.

        Keyword arguments:
        domain   --- the domain to check
        diagnose --- flag to report a diagnosis or a boolean (default False)

        """

        if "." in domain:
            d = ValidDiagnosis()
        else:
            d = GTLDDiagnosis("GTLD")

        return d
