from pyparsing import Forward, Literal, OneOrMore, Optional
from pyparsing import Regex, ZeroOrMore
from pyisemail import Grammar


class RFC5322(Grammar):

    def __init__(self):
        parts = self.__create_parts()
        self.local_part = parts["local_part"]
        self.domain = parts["domain"]
        self.addr_spec = parts["addr_spec"]

    def __create_parts(self):
        # Character classes from core rules
        CRLF = Literal('\r\n')
        DQUOTE = Literal('"')
        HTAB = Literal('\x09')
        SP = Literal(' ')
        WSP = SP | HTAB
        VCHAR = Regex("[\x21-\x7e]")

        # 3.2.1 Quoted characters
        quoted_pair = ("\\" + (VCHAR | WSP))

        # 3.2.2 Folding white space and comments
        FWS = (Optional(ZeroOrMore(WSP) + CRLF) + OneOrMore(WSP))
        ctext = Regex("[\x21-\x27\x2a-\x5b\x5d-\x7e]")
        comment = Forward()
        ccontent = ctext | quoted_pair | comment
        comment << ("(" + ZeroOrMore(Optional(FWS) + ccontent) +
                    Optional(FWS) + ")")
        CFWS = (OneOrMore(Optional(FWS) + comment) + Optional(FWS)) | FWS

        # 3.2.3 Atom
        atext = Regex("[a-zA-Z0-9!#$%&'*+\-/=\?^_`{|}~]")
        dot_atom_text = (OneOrMore(atext) +
                         OneOrMore("." + OneOrMore(atext)))
        dot_atom = Optional(CFWS) + dot_atom_text + Optional(CFWS)

        # 3.2.4 Quoted Strings
        qtext = Regex("[\x21\x23-\x5b\x5d-\x7e]")
        qcontent = qtext | quoted_pair
        quoted_string = (Optional(CFWS) + DQUOTE +
                         ZeroOrMore(Optional(FWS) + qcontent) +
                         Optional(FWS) + DQUOTE + Optional(CFWS))

        # 3.4.1 Addr-spec Specification
        local_part = dot_atom | quoted_string

        dtext = Regex("[\x21-\x5a\x5e-\x7e]")
        domain_literal = (Optional(CFWS) + "[" +
                          ZeroOrMore(Optional(FWS) + dtext) +
                          Optional(FWS) + "]" + Optional(CFWS))
        domain = dot_atom | domain_literal

        addr_spec = local_part + "@" + domain

        return {
            "local_part": local_part,
            "domain": domain,
            "addr_spec": addr_spec
        }