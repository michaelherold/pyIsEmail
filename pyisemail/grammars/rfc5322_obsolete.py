from pyparsing import Forward, Literal, OneOrMore, Optional
from pyparsing import Regex, ZeroOrMore
from pyisemail import Grammar


class RFC5322Obsolete(Grammar):

    def __init__(self):
        parts = self.__create_parts()
        self.local_part = parts["local_part"]
        self.domain = parts["domain"]
        self.addr_spec = parts["addr_spec"]

    def __create_parts(self):
        # Character classes from core rules
        CR = Literal('\r')
        LF = Literal('\n')
        CRLF = Literal('\r\n')
        DQUOTE = Literal('"')
        HTAB = Literal('\x09')
        SP = Literal(' ')
        WSP = SP | HTAB
        VCHAR = Regex("[\x21-\x7e]")

        # 4.1 Miscellaneous Obsolete Tokens
        obs_NO_WS_CTL = Regex("[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]")
        obs_ctext = obs_NO_WS_CTL
        obs_qtext = obs_NO_WS_CTL
        obs_qp = "\\" + ("\x00" | obs_NO_WS_CTL | LF | CR)
        obs_FWS = OneOrMore(WSP) + ZeroOrMore(CRLF + OneOrMore(WSP))

        # 3.2.1 Quoted characters
        quoted_pair = ("\\" + (VCHAR | WSP)) | obs_qp

        # 3.2.2 Folding white space and comments
        FWS = (Optional(ZeroOrMore(WSP) + CRLF) + OneOrMore(WSP)) | obs_FWS
        ctext = Regex("[\x21-\x27\x2a-\x5b\x5d-\x7e]") | obs_ctext
        comment = Forward()
        ccontent = ctext | quoted_pair | comment
        comment << ("(" + ZeroOrMore(Optional(FWS) + ccontent) +
                    Optional(FWS) + ")")
        CFWS = (OneOrMore(Optional(FWS) + comment) + Optional(FWS)) | FWS

        # 3.2.3 Atom
        atext = Regex("[a-zA-Z0-9!#$%&'*+\-/=\?^_`{|}~]")
        atom = Optional(CFWS) + OneOrMore(atext) + Optional(CFWS)
        dot_atom_text = (OneOrMore(atext) + OneOrMore("." + OneOrMore(atext)))
        dot_atom = Optional(CFWS) + dot_atom_text + Optional(CFWS)

        # 3.2.4 Quoted Strings
        qtext = Regex("[\x21\x23-\x5b\x5d-\x7e]") | obs_qtext
        qcontent = qtext | quoted_pair
        quoted_string = (Optional(CFWS) + DQUOTE +
                         ZeroOrMore(Optional(FWS) + qcontent) +
                         Optional(FWS) + DQUOTE + Optional(CFWS))

        # 3.2.5 Miscellaneous Tokens
        word = atom | quoted_string

        # 4.4 Obsolete Addressing
        obs_local_part = word + ZeroOrMore("." + word)
        obs_domain = atom + ZeroOrMore("." + atom)
        obs_dtext = obs_NO_WS_CTL | quoted_pair

        # 3.4.1 Addr-spec Specification
        local_part = dot_atom | quoted_string | obs_local_part

        dtext = Regex("[\x21-\x5a\x5e-\x7e]") | obs_dtext
        domain_literal = (Optional(CFWS) + "[" +
                          ZeroOrMore(Optional(FWS) + dtext) +
                          Optional(FWS) + "]" + Optional(CFWS))
        domain = dot_atom | domain_literal | obs_domain

        addr_spec = local_part + "@" + domain

        return {
            "local_part": local_part,
            "domain": domain,
            "addr_spec": addr_spec
        }