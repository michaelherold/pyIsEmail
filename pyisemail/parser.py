from pyparsing import Forward, Literal, OneOrMore, Optional
from pyparsing import ParserElement, Regex, ZeroOrMore


class Parser:
    _rfc2822 = None
    _rfc5322 = None

    def __init__(self):
        self.__init_rfc2822()
        self.__init_rfc5322()

    def __init_rfc2822(self):
        """Initialize the RFC2822 parsing grammar.

        For more information, see the RFC:
            * http://tools.ietf.org/html/rfc2822
        """

        if self._rfc2822 is None:
            ParserElement.setDefaultWhitespaceChars("")

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
            self._rfc2822 = addr_spec

    def __init_rfc5322(self):
        """Initialize the RFC5322 parsing grammar.

        For more information, see the RFC:
            * http://tools.ietf.org/html/rfc5322
        """

        if self._rfc5322 is None:
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
            comment = ("(" + ZeroOrMore(Optional(FWS) + ccontent) +
                       Optional(FWS) + ")")
            CFWS = (OneOrMore(Optional(FWS) + comment) + Optional(FWS)) | FWS

            # 3.2.3 Atom
            atext = Regex("[a-zA-Z0-9!#$%&'*+\-/=\?^_`{|}~]")
            atom = Optional(CFWS) + OneOrMore(atext) + Optional(CFWS)
            dot_atom_text = (OneOrMore(atext) +
                             OneOrMore("." + OneOrMore(atext)))
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
            self._rfc5322 = addr_spec

    def parse(self, address):
        try:
            parsed = self._rfc5322.parseString(address)
            return parsed is not None
        except:
            return False
