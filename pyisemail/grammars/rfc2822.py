from pyparsing import Forward, Literal, OneOrMore, Optional
from pyparsing import Regex, ZeroOrMore
from pyisemail import Grammar


class RFC2822(Grammar):

    def __init__(self):
        parts = self.__create_parts()
        self.local_part = parts['local_part']
        self.domain = parts['domain']
        self.addr_spec = parts['addr_spec']

    def __create_parts(self):

        CRLF = Literal("\r\n")
        LOWASCII = Regex("[\x00-\x7f]")
        WSP = Regex("[\x20\x09]")

        # 3.2.1 Primitive Tokens
        NO_WS_CTL = Regex("[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]")
        text = Regex("[\x01-\x09\x0b\x0c\x0e-\x7f]")

        # 3.2.2 Quoted characters
        obs_qp = r"\\" + LOWASCII
        quoted_pair = (r"\\" + text) | obs_qp

        # 3.2.3 Folding white space and comments
        obs_FWS = OneOrMore(WSP) + ZeroOrMore(CRLF + OneOrMore(WSP))
        comment = Forward()
        FWS = (Optional(ZeroOrMore(WSP) + CRLF) + OneOrMore(WSP)) | obs_FWS
        ctext = NO_WS_CTL | Regex("[\x21-\x27\x2a-\x5b\x5d-\x7e]")
        ccontent = ctext | quoted_pair | comment
        comment << ("(" +
                    ZeroOrMore(Optional(FWS) + ccontent) +
                    Optional(FWS) +
                    ")")
        CFWS = (ZeroOrMore(Optional(FWS) + comment) +
                ((Optional(FWS) + comment) | FWS))

        # 3.2.4 Atom
        atext = Regex("[a-zA-Z0-9!#$%&'*+\-/=\?^_`{|}~]")
        atom = Optional(CFWS) + OneOrMore(atext) + Optional(CFWS)
        dot_atom_text = (OneOrMore(atext) +
                         ZeroOrMore("." + OneOrMore(atext)))
        dot_atom = Optional(CFWS) + dot_atom_text + Optional(CFWS)

        # 3.2.5 Quoted strings
        qtext = NO_WS_CTL | Regex("[\x21\x23-\x5b\x5d-\x7e]")
        qcontent = qtext | quoted_pair
        quoted_string = (Optional(CFWS) + '"' +
                         ZeroOrMore(Optional(FWS) + qcontent) +
                         Optional(FWS) + '"' + Optional(CFWS))

        # 3.2.6 Miscellaneous tokens
        word = atom | quoted_string
        obs_local_part = word + ZeroOrMore("." + word)

        # 3.4.1 Addr-spec specification
        dtext = NO_WS_CTL | Regex("[\x21-\x5a\x5e-\x7e]")
        local_part = dot_atom | quoted_string | obs_local_part

        dcontent = dtext | quoted_pair
        domain_literal = (Optional(CFWS) + "[" +
                          ZeroOrMore(Optional(FWS) + dcontent) +
                          Optional(FWS) + "]" + Optional(CFWS))

        obs_domain = atom + ZeroOrMore("." + atom)

        domain = dot_atom | domain_literal | obs_domain

        addr_spec = local_part + "@" + domain

        return {
            'local_part': local_part,
            'domain': domain,
            'addr_spec': addr_spec
        }
