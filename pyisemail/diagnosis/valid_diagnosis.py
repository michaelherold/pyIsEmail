from pyisemail.diagnosis import BaseDiagnosis


class ValidDiagnosis(BaseDiagnosis):

    """A diagnosis indicating the address is valid for use.

    """

    DESCRIPTION = "Address is valid."

    MESSAGE = ("Address is valid. Please note that this does not mean "
               "the address actually exists, nor even that the domain "
               "actually exists. This address could be issued by the "
               "domain owner without breaking the rules of any RFCs.")

    def __init__(self, diagnosis_type='VALID'):
        self.diagnosis_type = diagnosis_type
        self.description = self.DESCRIPTION
        self.message = self.MESSAGE
        self.references = None
        self.code = 0
