from pyparsing import ParserElement, ParseException
from pyisemail.diagnosis import InvalidDiagnosis, ValidDiagnosis


class Grammar(object):

    def __init__(self, local_part, domain, addr_spec=None):
        ParserElement.setDefaultWhitespaceChars("")
        self.local_part = local_part
        self.domain = domain
        if addr_spec is not None:
            self.addr_spec = addr_spec
        else:
            self.addr_spec = local_part + "@" + domain

    def parse(self, address, diagnose=False):
        try:
            parsed = self.addr_spec.parseString(address)
            if diagnose:
                return (parsed is not None, ValidDiagnosis())
            else:
                return parsed is not None
        except ParseException as err:
            if diagnose:
                if err.parserElement == "@" or "@" not in err.pstr:
                    diagnosis = InvalidDiagnosis('NODOMAIN')
                else:
                    diagnosis = None
                return (False, diagnosis)
            else:
                return False
