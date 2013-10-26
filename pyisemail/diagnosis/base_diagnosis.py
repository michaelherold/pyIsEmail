from pyisemail.reference import Reference


class BaseDiagnosis(object):

    DESCRIPTION = ""
    MESSAGES = {}
    REFERENCES = {}

    def __init__(self, diagnosis_type):
        self.diagnosis_type = str(diagnosis_type)
        self.description = self.DESCRIPTION
        self.message = self.MESSAGES.get(diagnosis_type, "")
        self.references = self.get_references(diagnosis_type)

    def get_references(self, diagnosis_type):
        refs = self.REFERENCES.get(diagnosis_type, [])
        return [Reference(ref) for ref in refs]

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.diagnosis_type)

    def __eq__(self, other):
        return repr(self) == repr(other)
