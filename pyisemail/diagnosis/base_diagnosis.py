from pyisemail.reference import Reference


class BaseDiagnosis(object):

    """Super class for an error diagnosis.

    You should rarely, i.e. only in testing, instantiate a BaseDiagnosis, as
    it does not provide any pertinent information. Always use one of its
    subclasses.

    """

    CATEGORIES = {
        'VALID': 1,
        'DNSWARN': 7,
        'RFC5321': 15,
        'THRESHOLD': 16,
        'CFWS': 31,
        'DEPREC': 63,
        'RFC5322': 127,
        'ERR': 255,
    }
    DESCRIPTION = ""
    ERROR_CODES = {}
    MESSAGES = {}
    REFERENCES = {}

    def __init__(self, diagnosis_type):
        self.diagnosis_type = str(diagnosis_type)
        self.description = self.DESCRIPTION
        self.message = self.MESSAGES.get(diagnosis_type, "")
        self.references = self.get_references(diagnosis_type)
        self.code = self.ERROR_CODES.get(diagnosis_type, -1)

    def get_references(self, diagnosis_type):
        refs = self.REFERENCES.get(diagnosis_type, [])
        return [Reference(ref) for ref in refs]

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.diagnosis_type)

    def __hash__(self):
        return hash((self.__class__.__name__, self.diagnosis_type))

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __lt__(self, other):
        if isinstance(other, BaseDiagnosis):
            return self.code < other.code
        else:
            return self.code < other

    def __gt__(self, other):
        if isinstance(other, BaseDiagnosis):
            return self.code > other.code
        else:
            return self.code > other