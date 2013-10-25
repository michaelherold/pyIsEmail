from pyparsing import ParserElement, ParseException


class Grammar(object):

    def __init__(self, local_part, domain, addr_spec=None):
        ParserElement.setDefaultWhitespaceChars("")
        self.local_part = local_part
        self.domain = domain
        if addr_spec is not None:
            self.addr_spec = addr_spec
        else:
            self.addr_spec = local_part + "@" + domain

    def parse(self, address):
        try:
            parsed = self.addr_spec.parseString(address)
            return parsed is not None
        except ParseException:
            return False
