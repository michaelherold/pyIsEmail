import re
import sys
from pyisemail import EmailValidator
from pyisemail.diagnosis import BaseDiagnosis, CFWSDiagnosis
from pyisemail.diagnosis import DeprecatedDiagnosis
from pyisemail.diagnosis import InvalidDiagnosis, RFC5321Diagnosis
from pyisemail.diagnosis import RFC5322Diagnosis, ValidDiagnosis
from pyisemail.utils import enum

__all__ = ["ParserValidator"]

Char = enum(AT='@',
            BACKSLASH='\\',
            DOT='.',
            DQUOTE='"',
            OPENPARENTHESIS='(',
            CLOSEPARENTHESIS=')',
            OPENSQBRACKET='[',
            CLOSESQBRACKET=']',
            HYPHEN='-',
            COLON=':',
            DOUBLECOLON='::',
            SP=' ',
            HTAB="\t",
            CR="\r",
            LF="\n",
            IPV6TAG='IPv6:',
            # US-ASCII visible characters not valid for atext
            # (http:#tools.ietf.org/html/rfc5322#section-3.2.3)
            SPECIALS='()<>[]:;@\\,."')

Context = enum(LOCALPART=0,
               DOMAIN=1,
               LITERAL=2,
               COMMENT=3,
               FWS=4,
               QUOTEDSTRING=5,
               QUOTEDPAIR=6)

if sys.version_info[0] == 3:
    _unichr = chr
    _range = range
elif sys.version_info[0] == 2:
    _unichr = unichr
    _range = xrange


def to_char(token):
    """Transforms the ASCII control character symbols to their real char.

    Note: If the token is not an ASCII control character symbol, just
    return the token.

    Keyword arguments:
    token -- the token to transform

    """
    if ord(token) in _range(9216, 9229 + 1):
        token = _unichr(ord(token) - 9216)

    return token


class ParserValidator(EmailValidator):
    def is_email(self, address, diagnose=False):
        """Check that an address address conforms to RFCs 5321, 5322 and others.

        More specifically, see the follow RFCs:
            * http://tools.ietf.org/html/rfc5321
            * http://tools.ietf.org/html/rfc5322
            * http://tools.ietf.org/html/rfc4291#section-2.2
            * http://tools.ietf.org/html/rfc1123#section-2.1
            * http://tools.ietf.org/html/rfc3696) (guidance only)

        Keyword arguments:
        address    -- address to check.
        diagnose   -- flag to report a diagnosis or a boolean (default False)

        """

        threshold = BaseDiagnosis.CATEGORIES['VALID']
        return_status = [ValidDiagnosis()]
        parse_data = {}

        # Parse the address into components, character by character
        raw_length = len(address)
        context = Context.LOCALPART              # Where we are
        context_stack = [context]                # Where we've been
        context_prior = Context.LOCALPART        # Where we just came from
        token = ''                               # The current character
        token_prior = ''                         # The previous character
        parse_data[Context.LOCALPART] = ''       # The address' components
        parse_data[Context.DOMAIN] = ''
        atom_list = {
            Context.LOCALPART: [''],
            Context.DOMAIN: ['']
        }                                        # The address' dot-atoms
        element_count = 0
        element_len = 0
        hyphen_flag = False     # Hyphen cannot occur at the end of a subdomain
        end_or_die = False      # CFWS can only appear at the end of an element
        skip = False            # Skip flag that simulates i++
        crlf_count = -1         # crlf_count = -1 == !isset(crlf_count)

        for i in _range(raw_length):

            # Skip simulates the use of ++ operator
            if skip:
                skip = False
                continue

            token = address[i]
            token = to_char(token)

            # Switch to simulate decrementing; needed for FWS
            repeat = True

            while repeat:
                repeat = False

                #--------------------------------------------------------
                # Local part
                #--------------------------------------------------------
                if context == Context.LOCALPART:
                    # http://tools.ietf.org/html/rfc5322#section-3.4.1
                    #   local-part     =  dot-atom / quoted-string /
                    #                      obs-local-part
                    #
                    #   dot-atom       =  [CFWS] dot-atom-text [CFWS]
                    #
                    #   dot-atom-text  =  1*atext *("." 1*atext)
                    #
                    #   quoted-string  =  [CFWS]
                    #                     DQUOTE *([FWS] qcontent) [FWS] DQUOTE
                    #                     [CFWS]
                    #
                    #   obs-local-part =  word *("." word)
                    #
                    #   word           =  atom / quoted-string
                    #
                    #   atom           =  [CFWS] 1*atext [CFWS]
                    if token == Char.OPENPARENTHESIS:
                        if element_len == 0:
                            # Comments are OK at the beginning of an element
                            if element_count == 0:
                                return_status.append(CFWSDiagnosis('COMMENT'))
                            else:
                                return_status.append(
                                    DeprecatedDiagnosis('COMMENT'))
                        else:
                            return_status.append(CFWSDiagnosis('COMMENT'))
                            # We can't start a comment in the middle of an
                            # element, so this better be the end
                            end_or_die = True

                        context_stack.append(context)
                        context = Context.COMMENT
                    elif token == Char.DOT:
                        if element_len == 0:
                            # Another dot, already? Fatal error
                            if element_count == 0:
                                return_status.append(
                                    InvalidDiagnosis('DOT_START'))
                            else:
                                return_status.append(
                                    InvalidDiagnosis('CONSECUTIVEDOTS'))
                        else:
                            # The entire local-part can be a quoted string for
                            # RFC 5321. If it's just one atom that is quoted
                            # then it's an RFC 5322 obsolete form
                            if end_or_die:
                                return_status.append(
                                    DeprecatedDiagnosis('LOCALPART'))

                            # CFWS & quoted strings are OK again now we're at
                            # the beginning of an element (although they are
                            # obsolete forms)
                            end_or_die = False
                            element_len = 0
                            element_count += 1
                            parse_data[Context.LOCALPART] += token
                            atom_list[Context.LOCALPART].append('')
                    elif token == Char.DQUOTE:
                        if element_len == 0:
                            # The entire local-part can be a quoted string for
                            # RFC 5321. If it's just one atom that is quoted
                            # then it's an RFC 5322 obsolete form
                            if element_count == 0:
                                return_status.append(
                                    RFC5321Diagnosis('QUOTEDSTRING'))
                            else:
                                return_status.append(
                                    DeprecatedDiagnosis('LOCALPART'))

                            parse_data[Context.LOCALPART] += token
                            atom_list[Context.LOCALPART][element_count] += token
                            element_len += 1
                            end_or_die = True
                            context_stack.append(context)
                            context = Context.QUOTEDSTRING
                        else:
                            # Fatal error
                            return_status.append(
                                InvalidDiagnosis('EXPECTING_ATEXT'))
                    # Folding White Space (FWS)
                    elif token in [Char.CR, Char.SP, Char.HTAB]:
                        # Skip simulates the use of ++ operator if the latter
                        # check doesn't short-circuit
                        if token == Char.CR:
                            skip = True

                            if (i+1 == raw_length or
                                    to_char(address[i+1]) != Char.LF):
                                return_status.append(
                                    InvalidDiagnosis('CR_NO_LF'))
                                break

                        if element_len == 0:
                            if element_count == 0:
                                return_status.append(CFWSDiagnosis('FWS'))
                            else:
                                return_status.append(DeprecatedDiagnosis('FWS'))
                        else:
                            # We can't start FWS in the middle of an element, so
                            # this better be the end
                            end_or_die = True

                        context_stack.append(context)
                        context = Context.FWS
                        token_prior = token
                    # @
                    elif token == Char.AT:
                        # At this point we should have a valid local-part
                        if len(context_stack) != 1:  # pragma: no cover
                            if diagnose:
                                return InvalidDiagnosis('BAD_PARSE')
                            else:
                                return False

                        if parse_data[Context.LOCALPART] == '':
                            # Fatal error
                            return_status.append(
                                InvalidDiagnosis('NOLOCALPART'))
                        elif element_len == 0:
                            # Fatal error
                            return_status.append(InvalidDiagnosis('DOT_END'))
                        # http://tools.ietf.org/html/rfc5321#section-4.5.3.1.1
                        #   The maximum total length of a user name or other
                        #   local-part is 64 octets.
                        elif len(parse_data[Context.LOCALPART]) > 64:
                            return_status.append(
                                RFC5322Diagnosis('LOCAL_TOOLONG'))
                        # http://tools.ietf.org/html/rfc5322#section-3.4.1
                        #   Comments and folding white space
                        #   SHOULD NOT be used around the "@" in the addr-spec.
                        #
                        # http://tools.ietf.org/html/rfc2119
                        # 4. SHOULD NOT   This phrase, or the phrase "NOT
                        #    RECOMMENDED" mean that there may exist valid
                        #    reasons in particular circumstances when the
                        #    particular behavior is acceptable or even useful,
                        #    but the full implications should be understood and
                        #    the case carefully weighed before implementing any
                        #    behavior described with this label.
                        elif context_prior in [Context.COMMENT, Context.FWS]:
                            return_status.append(
                                DeprecatedDiagnosis('CFWS_NEAR_AT'))

                        # Clear everything down for the domain parsing
                        context = Context.DOMAIN
                        context_stack = []
                        element_count = 0
                        element_len = 0
                        # CFWS can only appear at the end of the element
                        end_or_die = False
                    # atext
                    else:
                        # http://tools.ietf.org/html/rfc5322#section-3.2.3
                        #    atext  =  ALPHA / DIGIT /  ; Printable US-ASCII
                        #              "!" / "#" /      ; characters not
                        #              "$" / "%" /      ; including specials.
                        #              "&" / "'" /      ; Used for atoms.
                        #              "*" / "+" /
                        #              "-" / "/" /
                        #              "=" / "?" /
                        #              "^" / "_" /
                        #              "`" / "{" /
                        #              "|" / "}" /
                        #              "~"
                        if end_or_die:
                            # We have encountered atext where it is no longer
                            # valid
                            if context_prior in [Context.COMMENT, Context.FWS]:
                                return_status.append(
                                    InvalidDiagnosis('ATEXT_AFTER_CFWS'))
                            elif context_prior == Context.QUOTEDSTRING:
                                return_status.append(
                                    InvalidDiagnosis('ATEXT_AFTER_QS'))
                            else:  # pragma: no cover
                                if diagnose:
                                    return InvalidDiagnosis('BAD_PARSE')
                                else:
                                    return False
                        else:
                            context_prior = context
                            o = ord(token)

                            if (o < 33 or o > 126 or o == 10 or
                                    token in Char.SPECIALS):
                                return_status.append(
                                    InvalidDiagnosis('EXPECTING_ATEXT'))

                            parse_data[Context.LOCALPART] += token
                            atom_list[Context.LOCALPART][element_count] += token
                            element_len += 1
                #--------------------------------------------------------
                # Domain
                #--------------------------------------------------------
                elif context == Context.DOMAIN:
                    # http://tools.ietf.org/html/rfc5322#section-3.4.1
                    #   domain         = dot-atom / domain-literal / obs-domain
                    #
                    #   dot-atom       = [CFWS] dot-atom-text [CFWS]
                    #
                    #   dot-atom-text  = 1*atext *("." 1*atext)
                    #
                    #   domain-literal = [CFWS]
                    #                    "[" *([FWS] dtext) [FWS] "]"
                    #                    [CFWS]
                    #
                    #   dtext          = %d33-90 /     ; Printable US-ASCII
                    #                    %d94-126 /    ; characters not
                    #                    obs-dtext     ; including [, ], or \
                    #
                    #   obs-domain     = atom *("." atom)
                    #
                    #   atom           = [CFWS] 1*atext [CFWS]
                    #
                    #
                    # http://tools.ietf.org/html/rfc5321#section-4.1.2
                    #   Mailbox       = Local-part
                    #                   "@"
                    #                   ( Domain / address-literal )
                    #
                    #   Domain        = sub-domain *("." sub-domain)
                    #
                    #   address-literal  = "[" ( IPv4-address-literal /
                    #                            IPv6-address-literal /
                    #                            General-address-literal ) "]"
                    #                    ; See Section 4.1.3
                    #
                    # http://tools.ietf.org/html/rfc5322#section-3.4.1
                    #      Note: A liberal syntax for the domain portion of
                    #      addr-spec is given here.  However, the domain portion
                    #      contains addressing information specified by and used
                    #      in other protocols (e.g., RFC 1034, RFC 1035, RFC
                    #      1123, RFC5321).  It is therefore incumbent upon
                    #      implementations to conform to the syntax of addresses
                    #      for the context in which they are used.
                    # is_email() author's note: it's not clear how to interpret
                    # this in the context of a general address address
                    # validator. The conclusion I have reached is this:
                    # "addressing information" must comply with RFC 5321 (and in
                    # turn RFC 1035), anything that is "semantically invisible"
                    # must comply only with RFC 5322.

                    # Comment
                    if token == Char.OPENPARENTHESIS:
                        if element_len == 0:
                            # Comments at the start of the domain are deprecated
                            # in the text
                            # Comments at the start of a subdomain are
                            # obs-domain
                            # (http://tools.ietf.org/html/rfc5322#section-3.4.1)
                            if element_count == 0:
                                return_status.append(
                                    DeprecatedDiagnosis('CFWS_NEAR_AT'))
                            else:
                                return_status.append(
                                    DeprecatedDiagnosis('COMMENT'))
                        else:
                            return_status.append(CFWSDiagnosis('COMMENT'))
                            # We can't start a comment in the middle of an
                            # element, so this better be the end
                            end_or_die = True

                        context_stack.append(context)
                        context = Context.COMMENT
                    # Next dot-atom element
                    elif token == Char.DOT:
                        if element_len == 0:
                            # Another dot, already? Fatal error
                            if element_count == 0:
                                return_status.append(
                                    InvalidDiagnosis('DOT_START'))
                            else:
                                return_status.append(
                                    InvalidDiagnosis('CONSECUTIVEDOTS'))
                        elif hyphen_flag:
                            # Previous subdomain ended in a hyphen. Fatal error
                            return_status.append(
                                InvalidDiagnosis('DOMAINHYPHENEND'))
                        else:
                            # Nowhere in RFC 5321 does it say explicitly that
                            # the domain part of a Mailbox must be a valid
                            # domain according to the DNS standards set out in
                            # RFC 1035, but this *is* implied in several places.
                            # For instance, wherever the idea of host routing is
                            # discussed the RFC says that the domain must be
                            # looked up in the DNS. This would be nonsense
                            # unless the domain was designed to be a valid DNS
                            # domain. Hence we must conclude that the RFC 1035
                            # restriction on label length also applies to RFC
                            # 5321 domains.
                            #
                            # http://tools.ietf.org/html/rfc1035#section-2.3.4
                            # labels         63 octets or less
                            if element_len > 63:
                                return_status.append(
                                    RFC5322Diagnosis('LABEL_TOOLONG'))

                            # CFWS is OK again now we're at the beginning of an
                            # element (although it may be obsolete CFWS)
                            end_or_die = False
                            element_len = 0
                            element_count += 1
                            atom_list[Context.DOMAIN].append('')
                            parse_data[Context.DOMAIN] += token
                    # Domain literal
                    elif token == Char.OPENSQBRACKET:
                        if parse_data[Context.DOMAIN] == '':
                            # Domain literal must be the only component
                            end_or_die = True
                            element_len += 1
                            context_stack.append(context)
                            context = Context.LITERAL
                            parse_data[Context.DOMAIN] += token
                            atom_list[Context.DOMAIN][element_count] += token
                            parse_data['literal'] = ''
                        else:
                            # Fatal error
                            return_status.append(
                                InvalidDiagnosis('EXPECTING_ATEXT'))

                    # Folding White Space (FWS)
                    elif token in [Char.CR, Char.SP, Char.HTAB]:
                        # Skip simulates the use of ++ operator if the latter
                        # check doesn't short-circuit
                        if token == Char.CR:
                            skip = True

                            if i+1 == raw_length or (to_char(address[i + 1]) !=
                                                     Char.LF):
                                # Fatal error
                                return_status.append(
                                    InvalidDiagnosis('CR_NO_LF'))
                                break

                        if element_len == 0:
                            if element_count == 0:
                                return_status.append(
                                    DeprecatedDiagnosis('CFWS_NEAR_AT'))
                            else:
                                return_status.append(DeprecatedDiagnosis('FWS'))
                        else:
                            return_status.append(CFWSDiagnosis('FWS'))
                            # We can't start FWS in the middle of an element, so
                            # this better be the end
                            end_or_die = True

                        context_stack.append(context)
                        context = Context.FWS
                        token_prior = token
                    # atext
                    else:
                        # RFC 5322 allows any atext...
                        # http://tools.ietf.org/html/rfc5322#section-3.2.3
                        #    atext  =  ALPHA / DIGIT / ; Printable US-ASCII
                        #              "!" / "#" /     ; characters not
                        #              "$" / "%" /     ; including specials.
                        #              "&" / "'" /     ; Used for atoms.
                        #              "*" / "+" /
                        #              "-" / "/" /
                        #              "=" / "?" /
                        #              "^" / "_" /
                        #              "`" / "{" /
                        #              "|" / "}" /
                        #              "~"

                        # But RFC 5321 only allows letter-digit-hyphen to comply
                        # with DNS rules (RFCs 1034 & 1123)
                        # http://tools.ietf.org/html/rfc5321#section-4.1.2
                        #   sub-domain     = Let-dig [Ldh-str]
                        #
                        #   Let-dig        = ALPHA / DIGIT
                        #
                        #   Ldh-str        = *( ALPHA / DIGIT / "-" ) Let-dig
                        #
                        if end_or_die:
                            # We have encountered atext where it is no longer
                            # valid
                            if context_prior in [Context.COMMENT, Context.FWS]:
                                return_status.append(
                                    InvalidDiagnosis('ATEXT_AFTER_CFWS'))
                            elif context_prior == Context.LITERAL:
                                return_status.append(
                                    InvalidDiagnosis('ATEXT_AFTER_DOMLIT'))
                            else:  # pragma: no cover
                                if diagnose:
                                    return InvalidDiagnosis('BAD_PARSE')
                                else:
                                    return False

                        o = ord(token)
                        # Assume this token isn't a hyphen unless we discover
                        # it is
                        hyphen_flag = False

                        if o < 33 or o > 126 or token in Char.SPECIALS:
                            # Fatal error
                            return_status.append(
                                InvalidDiagnosis('EXPECTING_ATEXT'))
                        elif token == Char.HYPHEN:
                            if element_len == 0:
                                # Hyphens can't be at the beginning of a
                                # subdomain
                                # Fatal error
                                return_status.append(
                                    InvalidDiagnosis('DOMAINHYPHENSTART'))

                            hyphen_flag = True
                        elif not (47 < o < 58 or 64 < o < 91 or 96 < o < 123):
                            # Not an RFC 5321 subdomain, but still OK by RFC5322
                            return_status.append(RFC5322Diagnosis('DOMAIN'))

                        parse_data[Context.DOMAIN] += token
                        atom_list[Context.DOMAIN][element_count] += token
                        element_len += 1
                #--------------------------------------------------------
                # Domain literal
                #--------------------------------------------------------
                elif context == Context.LITERAL:
                    # http://tools.ietf.org/html/rfc5322#section-3.4.1
                    #   domain-literal = [CFWS]
                    #                    "[" *([FWS] dtext) [FWS] "]"
                    #                    [CFWS]
                    #
                    #   dtext          = %d33-90 /     ; Printable US-ASCII
                    #                    %d94-126 /    ; characters not
                    #                    obs-dtext     ; including [, ], or \
                    #
                    #   obs-dtext      = obs-NO-WS-CTL / quoted-pair

                    # End of domain literal
                    if token == Char.CLOSESQBRACKET:
                        if (max(return_status) <
                                BaseDiagnosis.CATEGORIES['DEPREC']):
                            # Could be a valid RFC 5321 address literal, so
                            # let's check
                            #
                            # http://tools.ietf.org/html/rfc5321#section-4.1.2
                            #   address-literal  = "[" ( IPv4-address-literal /
                            #                    IPv6-address-literal /
                            #                    General-address-literal ) "]"
                            #                    ; See Section 4.1.3
                            #
                            # http://tools.ietf.org/html/rfc5321#section-4.1.3
                            #   IPv4-address-literal  = Snum 3("."  Snum)
                            #
                            #   IPv6-address-literal  = "IPv6:" IPv6-addr
                            #
                            #   General-address-literal  = Standardized-tag ":"
                            #                              1*dcontent
                            #
                            #   Standardized-tag  = Ldh-str
                            #                     ; Standardized-tag MUST be
                            #                     ; specified in a
                            #                     ; Standards-Track RFC and
                            #                     ; registered with IANA
                            #
                            #   dcontent       = %d33-90 / ; Printable US-ASCII
                            #                    %d94-126  ; excl. "[", "\", "]"
                            #
                            #   Snum           = 1*3DIGIT
                            #                  ; representing a decimal integer
                            #                  ; value in the range 0-255
                            #
                            #   IPv6-addr      = IPv6-full / IPv6-comp /
                            #                    IPv6v4-full / IPv6v4-comp
                            #
                            #   IPv6-hex       = 1*4HEXDIG
                            #
                            #   IPv6-full      = IPv6-hex 7(":" IPv6-hex)
                            #
                            #   IPv6-comp      = [IPv6-hex *5(":" IPv6-hex)]
                            #                    "::"
                            #                    [IPv6-hex *5(":" IPv6-hex)]
                            #                  ; The "::" represents at least 2
                            #                  ; 16-bit groups of zeros. No more
                            #                  ; than 6 groups in addition to
                            #                  ; the "::" may be present.
                            #
                            #   IPv6v4-full    = IPv6-hex 5(":" IPv6-hex) ":"
                            #                    IPv4-address-literal
                            #
                            #   IPv6v4-comp    = [IPv6-hex *3(":" IPv6-hex)]
                            #                    "::"
                            #                    [IPv6-hex *3(":" IPv6-hex) ":"]
                            #                    IPv4-address-literal
                            #                  ; The "::" represents at least 2
                            #                  ; 16-bit groups of zeros. No more
                            #                  ; than 4 groups in addition to
                            #                  ; the "::" and
                            #                  ; IPv4-address-literal may be
                            #                  ; present.

                            max_groups = 8
                            index = False
                            address_literal = parse_data['literal']

                            # Extract IPv4 part from the end of the
                            # address-literal (if there is one)
                            regex = (
                                r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)"
                                r"{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
                            )
                            match_ip = re.search(regex, address_literal)
                            if match_ip:
                                index = address_literal.rfind(match_ip.group(0))
                                if index != 0:
                                    # Convert IPv4 part to IPv6 format for
                                    # further testing
                                    address_literal = (
                                        address_literal[0:index] + '0:0')

                            if index == 0 and index is not False:
                                # Nothing there except a valid IPv4 address
                                return_status.append(
                                    RFC5321Diagnosis('ADDRESSLITERAL'))
                            elif not address_literal.startswith(Char.IPV6TAG):
                                return_status.append(
                                    RFC5322Diagnosis('DOMAINLITERAL'))
                            else:
                                ipv6 = address_literal[5:]
                                # Revision 2.7: Daniel Marschall's new IPv6
                                # testing strategy
                                match_ip = ipv6.split(Char.COLON)
                                grp_count = len(match_ip)
                                index = ipv6.find(Char.DOUBLECOLON)

                                if index == -1:
                                    # we need exactly the right number of groups
                                    if grp_count != max_groups:
                                        return_status.append(
                                            RFC5322Diagnosis('IPV6_GRPCOUNT')
                                        )
                                else:
                                    if index != ipv6.rfind(Char.DOUBLECOLON):
                                        return_status.append(
                                            RFC5322Diagnosis('IPV6_2X2XCOLON')
                                        )
                                    else:
                                        if index == 0 or index == len(ipv6) - 2:
                                            # RFC 4291 allows :: at the start or
                                            # end of an address with 7 other
                                            # groups in addition
                                            max_groups += 1

                                        if grp_count > max_groups:
                                            return_status.append(
                                                RFC5322Diagnosis('IPV6_MAXGRPS')
                                            )
                                        elif grp_count == max_groups:
                                            # Eliding a single "::"
                                            return_status.append(
                                                RFC5321Diagnosis(
                                                    'IPV6DEPRECATED')
                                            )

                                # Revision 2.7: Daniel Marschall's new IPv6
                                # testing strategy
                                if (ipv6[0] == Char.COLON and
                                        ipv6[1] != Char.COLON):
                                    # Address starts with a single colon
                                    return_status.append(
                                        RFC5322Diagnosis('IPV6_COLONSTRT'))
                                elif (ipv6[-1] == Char.COLON and
                                        ipv6[-2] != Char.COLON):
                                    # Address ends with a single colon
                                    return_status.append(
                                        RFC5322Diagnosis('IPV6_COLONEND'))
                                elif ([re.match(r"^[0-9A-Fa-f]{0,4}$", i)
                                       for i in match_ip].count(None) != 0):
                                    # Check for unmatched characters
                                    return_status.append(
                                        RFC5322Diagnosis('IPV6_BADCHAR'))
                                else:
                                    return_status.append(
                                        RFC5321Diagnosis('ADDRESSLITERAL'))
                        else:
                            return_status.append(
                                RFC5322Diagnosis('DOMAINLITERAL'))

                        parse_data[Context.DOMAIN] += token
                        atom_list[Context.DOMAIN][element_count] += token
                        element_len += 1
                        context_prior = context
                        context = context_stack.pop()
                    elif token == Char.BACKSLASH:
                        return_status.append(
                            RFC5322Diagnosis('DOMLIT_OBSDTEXT'))
                        context_stack.append(context)
                        context = Context.QUOTEDPAIR
                    # Folding White Space (FWS)
                    elif token in [Char.CR, Char.SP, Char.HTAB]:
                        # Skip simulates the use of ++ operator if the latter
                        # check doesn't short-circuit
                        if token == Char.CR:
                            skip = True

                            if (i+1 == raw_length or
                                    to_char(address[i+1]) != Char.LF):
                                return_status.append(
                                    InvalidDiagnosis('CR_NO_LF'))
                                break

                        return_status.append(CFWSDiagnosis('FWS'))

                        context_stack.append(context)
                        context = Context.FWS
                        token_prior = token
                    # dtext
                    else:
                        # http://tools.ietf.org/html/rfc5322#section-3.4.1
                        #   dtext         = %d33-90 /   ; Printable US-ASCII
                        #                   %d94-126 /  ; characters not
                        #                   obs-dtext   ; including [, ], or \
                        #
                        #   obs-dtext     = obs-NO-WS-CTL / quoted-pair
                        #
                        #   obs-NO-WS-CTL = %d1-8 /     ; US-ASCII control
                        #                   %d11 /      ; characters that do not
                        #                   %d12 /      ; include the carriage
                        #                   %d14-31 /   ; return, line feed, and
                        #                   %d127       ; white space characters
                        o = ord(token)

                        # CR, LF, SP & HTAB have already been parsed above
                        if o > 127 or o == 0 or token == Char.OPENSQBRACKET:
                            # Fatal error
                            return_status.append(
                                InvalidDiagnosis('EXPECTING_DTEXT'))
                            break
                        elif o < 33 or o == 127:
                            return_status.append(
                                RFC5322Diagnosis('DOMLIT_OBSDTEXT'))

                        parse_data['literal'] += token
                        parse_data[Context.DOMAIN] += token
                        atom_list[Context.DOMAIN][element_count] += token
                        element_len += 1
                #--------------------------------------------------------
                # Quoted string
                #--------------------------------------------------------
                elif context == Context.QUOTEDSTRING:
                    # http://tools.ietf.org/html/rfc5322#section-3.2.4
                    #   quoted-string   =  [CFWS]
                    #                      DQUOTE *([FWS] qcontent) [FWS] DQUOTE
                    #                      [CFWS]
                    #
                    #   qcontent        =  qtext / quoted-pair

                    # Quoted pair
                    if token == Char.BACKSLASH:
                        context_stack.append(context)
                        context = Context.QUOTEDPAIR
                    # Folding White Space (FWS)
                    # Inside a quoted string, spaces are allow as regular
                    # characters. It's only FWS if we include HTAB or CRLF
                    elif token in [Char.CR, Char.HTAB]:
                        # Skip simulates the use of ++ operator if the latter
                        # check doesn't short-circuit
                        if token == Char.CR:
                            skip = True

                            if (i+1 == raw_length or
                                    to_char(address[i+1]) != Char.LF):
                                return_status.append(
                                    InvalidDiagnosis('CR_NO_LF'))
                                break

                        # http://tools.ietf.org/html/rfc5322#section-3.2.2
                        #   Runs of FWS, comment, or CFWS that occur between
                        #   lexical tokens in a structured header field are
                        #   semantically interpreted as a single space
                        #   character.

                        # http://tools.ietf.org/html/rfc5322#section-3.2.4
                        #   the CRLF in any FWS/CFWS that appears within the
                        #   quoted string [is] semantically "invisible" and
                        #   therefore not part of the quoted-string
                        parse_data[Context.LOCALPART] += Char.SP
                        atom_list[Context.LOCALPART][element_count] += Char.SP
                        element_len += 1

                        return_status.append(CFWSDiagnosis('FWS'))
                        context_stack.append(context)
                        context = Context.FWS
                        token_prior = token
                    # End of quoted string
                    elif token == Char.DQUOTE:
                        parse_data[Context.LOCALPART] += token
                        atom_list[Context.LOCALPART][element_count] += token
                        element_len += 1
                        context_prior = context
                        context = context_stack.pop()
                    # qtext
                    else:
                        # http://tools.ietf.org/html/rfc5322#section-3.2.4
                        #   qtext          =  %d33 /      ; Printable US-ASCII
                        #                     %d35-91 /   ; characters not
                        #                     %d93-126 /  ; including "\" or the
                        #                     obs-qtext   ; quote character
                        #
                        #   obs-qtext      =  obs-NO-WS-CTL
                        #
                        #   obs-NO-WS-CTL  =  %d1-8 /     ; US-ASCII control
                        #                     %d11 /      ; characters that do
                        #                     %d12 /      ; not include the CR,
                        #                     %d14-31 /   ; LF, and white space
                        #                     %d127       ; characters
                        o = ord(token)

                        if o > 127 or o == 0 or o == 10:
                            # Fatal error
                            return_status.append(
                                InvalidDiagnosis('EXPECTING_QTEXT'))
                        elif o < 32 or o == 127:
                            return_status.append(
                                DeprecatedDiagnosis('QTEXT'))

                        parse_data[Context.LOCALPART] += token
                        atom_list[Context.LOCALPART][element_count] += token
                        element_len += 1
                #--------------------------------------------------------
                # Quoted pair
                #--------------------------------------------------------
                elif context == Context.QUOTEDPAIR:
                    # http://tools.ietf.org/html/rfc5322#section-3.2.1
                    #   quoted-pair     =   ("\" (VCHAR / WSP)) / obs-qp
                    #
                    #   VCHAR           =  %d33-126    ; visible (printing)
                    #                                  ;  characters
                    #
                    #   WSP             =  SP / HTAB   ; white space
                    #
                    #   obs-qp          =   "\" (%d0 / obs-NO-WS-CTL / LF / CR)
                    #
                    #   obs-NO-WS-CTL   =   %d1-8 /    ; US-ASCII control
                    #                       %d11 /     ;  characters that do not
                    #                       %d12 /     ;  include the carriage
                    #                       %d14-31 /  ;  return, line feed, and
                    #                       %d127      ;  white space characters
                    #
                    # i.e. obs-qp       =  "\" (%d0-8, %d10-31 / %d127)

                    o = ord(token)

                    if o > 127:
                        # Fatal error
                        return_status.append(
                            InvalidDiagnosis('EXPECTING_QPAIR'))
                    elif (o < 31 and o != 9) or o == 127:
                        # SP & HTAB are allowed
                        return_status.append(DeprecatedDiagnosis('QP'))

                    # At this point we know where this qpair occurred so
                    # we could check to see if the character actually
                    # needed to be quoted at all.
                    # http://tools.ietf.org/html/rfc5321#section-4.1.2
                    #   the sending system SHOULD transmit the
                    #   form that uses the minimum quoting possible.
                    context_prior = context
                    context = context_stack.pop()   # End of qpair
                    token = Char.BACKSLASH + token

                    if context == Context.COMMENT:
                        pass
                    elif context == Context.QUOTEDSTRING:
                        parse_data[Context.LOCALPART] += token
                        atom_list[Context.LOCALPART][element_count] += token
                        # The maximum sizes specified by RFC 5321 are octet
                        # counts, so we must include the backslash
                        element_len += 2
                    elif context == Context.LITERAL:
                        parse_data[Context.DOMAIN] += token
                        atom_list[Context.DOMAIN][element_count] += token
                        # The maximum sizes specified by RFC 5321 are octet
                        # counts, so we must include the backslash
                        element_len += 2
                    else:  # pragma: no cover
                        if diagnose:
                            return InvalidDiagnosis('BAD_PARSE')
                        else:
                            return False
                #--------------------------------------------------------
                # Comment
                #--------------------------------------------------------
                elif context == Context.COMMENT:
                    # http://tools.ietf.org/html/rfc5322#section-3.2.2
                    #   comment         =   "(" *([FWS] ccontent) [FWS] ")"
                    #
                    #   ccontent        =   ctext / quoted-pair / comment

                    # Nested comment
                    if token == Char.OPENPARENTHESIS:
                        # Nested comments are OK
                        context_stack.append(context)
                        context = Context.COMMENT
                    # End of comment
                    elif token == Char.CLOSEPARENTHESIS:
                        context_prior = context
                        context = context_stack.pop()
                    # Quoted pair
                    elif token == Char.BACKSLASH:
                        context_stack.append(context)
                        context = Context.QUOTEDPAIR
                    # Folding White Space (FWS)
                    elif token in [Char.CR, Char.SP, Char.HTAB]:
                        # Skip simulates the use of ++ operator if the latter
                        # check doesn't short-circuit
                        if token == Char.CR:
                            skip = True

                            if (i+1 == raw_length or
                                    to_char(address[i+1]) != Char.LF):
                                return_status.append(
                                    InvalidDiagnosis('CR_NO_LF'))
                                break

                        return_status.append(CFWSDiagnosis('FWS'))

                        context_stack.append(context)
                        context = Context.FWS
                        token_prior = token
                    # ctext
                    else:
                        # http://tools.ietf.org/html/rfc5322#section-3.2.3
                        #   ctext           =   %d33-39 /   ; Printable US-ASCII
                        #                       %d42-91 /   ; characters not
                        #                       %d93-126 /  ; including (, ),
                        #                       obs-ctext   ; or \
                        #
                        #   obs-ctext       =   obs-NO-WS-CTL
                        #
                        #   obs-NO-WS-CTL   =   %d1-8 /      ; US-ASCII control
                        #                       %d11 /       ; characters that
                        #                       %d12 /       ; do not include
                        #                       %d14-31 /    ; the CR, LF, and
                        #                                    ; white space
                        #                                    ; characters

                        o = ord(token)

                        if o > 127 or o == 0 or o == 10:
                            # Fatal error
                            return_status.append(
                                InvalidDiagnosis('EXPECTING_CTEXT'))
                            break
                        elif o < 32 or o == 127:
                            return_status.append(DeprecatedDiagnosis('CTEXT'))

                #--------------------------------------------------------
                # Folding White Space (FWS)
                #--------------------------------------------------------
                elif context == Context.FWS:
                    # http://tools.ietf.org/html/rfc5322#section-3.2.2
                    #   FWS             =   ([*WSP CRLF] 1*WSP) /  obs-FWS
                    #                       ; Folding white space
                    #
                    # But note the erratum:
                    # http://www.rfc-editor.org/errata_search.php?rfc=5322&eid=1908
                    #   In the obsolete syntax, any amount of folding white
                    #   space MAY be inserted where the obs-FWS rule is allowed.
                    #   This creates the possibility of having two consecutive
                    #   "folds" in a line, and therefore the possibility that a
                    #   line which makes up a folded header field could be
                    #   composed entirely of white space.
                    #
                    #   obs-FWS         =   1*([CRLF] WSP)

                    if token_prior == Char.CR:
                        if token == Char.CR:
                            # Fatal error
                            return_status.append(
                                InvalidDiagnosis('FWS_CRLF_X2'))
                            break

                        if crlf_count != -1:
                            crlf_count += 1
                            if crlf_count > 1:
                                # Multiple folds = obsolete FWS
                                return_status.append(
                                    DeprecatedDiagnosis('FWS'))
                        else:
                            crlf_count = 1

                    # Skip simulates the use of ++ operator if the latter
                    # check doesn't short-circuit
                    if token == Char.CR:
                        skip = True

                        if (i+1 == raw_length or
                                to_char(address[i+1]) != Char.LF):
                            return_status.append(InvalidDiagnosis('CR_NO_LF'))
                            break
                    elif token in [Char.SP, Char.HTAB]:
                        pass
                    else:
                        if token_prior == Char.CR:
                            # Fatal error
                            return_status.append(
                                InvalidDiagnosis('FWS_CRLF_END'))
                            break

                        if crlf_count != -1:
                            crlf_count = -1

                        context_prior = context
                        # End of FWS
                        context = context_stack.pop()

                        # Look at this token again in the parent context
                        repeat = True

                    token_prior = token

                #--------------------------------------------------------
                # A context we aren't expecting
                #--------------------------------------------------------
                else:  # pragma: no cover
                    if diagnose:
                        return InvalidDiagnosis('BAD_PARSE')
                    else:
                        return False

            # No point in going on if we've got a fatal error
            if max(return_status) > BaseDiagnosis.CATEGORIES['RFC5322']:
                break

        # Some simple final tests
        if max(return_status) < BaseDiagnosis.CATEGORIES['RFC5322']:
            if context == Context.QUOTEDSTRING:
                # Fatal error
                return_status.append(InvalidDiagnosis('UNCLOSEDQUOTEDSTR'))
            elif context == Context.QUOTEDPAIR:
                # Fatal error
                return_status.append(InvalidDiagnosis('BACKSLASHEND'))
            elif context == Context.COMMENT:
                # Fatal error
                return_status.append(InvalidDiagnosis('UNCLOSEDCOMMENT'))
            elif context == Context.LITERAL:
                # Fatal error
                return_status.append(InvalidDiagnosis('UNCLOSEDDOMLIT'))
            elif token == Char.CR:
                # Fatal error
                return_status.append(InvalidDiagnosis('FWS_CRLF_END'))
            elif parse_data[Context.DOMAIN] == '':
                # Fatal error
                return_status.append(InvalidDiagnosis('NODOMAIN'))
            elif element_len == 0:
                # Fatal error
                return_status.append(InvalidDiagnosis('DOT_END'))
            elif hyphen_flag:
                # Fatal error
                return_status.append(InvalidDiagnosis('DOMAINHYPHENEND'))
            # http://tools.ietf.org/html/rfc5321#section-4.5.3.1.2
            # The maximum total length of a domain name or number is 255 octets.
            elif len(parse_data[Context.DOMAIN]) > 255:
                return_status.append(RFC5322Diagnosis('DOMAIN_TOOLONG'))
            # http://tools.ietf.org/html/rfc5321#section-4.1.2
            #   Forward-path   = Path
            #
            #   Path           = "<" [ A-d-l ":" ] Mailbox ">"
            #
            # http://tools.ietf.org/html/rfc5321#section-4.5.3.1.3
            #   The maximum total length of a reverse-path or forward-path is
            #   256 octets (including the punctuation and element separators).
            #
            # Thus, even without (obsolete) routing information, the Mailbox can
            # only be 254 characters long. This is confirmed by this verified
            # erratum to RFC 3696:
            #
            # http://www.rfc-editor.org/errata_search.php?rfc=3696&eid=1690
            #   However, there is a restriction in RFC 2821 on the length of an
            #   address in MAIL and RCPT commands of 254 characters.  Since
            #   addresses that do not fit in those fields are not normally
            #   useful, the upper limit on address lengths should normally be
            #   considered to be 254.
            elif len(parse_data[Context.LOCALPART] + Char.AT +
                     parse_data[Context.DOMAIN]) > 254:
                return_status.append(RFC5322Diagnosis('TOOLONG'))
            # http://tools.ietf.org/html/rfc1035#section-2.3.4
            # labels           63 octets or less
            elif element_len > 63:
                return_status.append(RFC5322Diagnosis('LABEL_TOOLONG'))

        return_status = list(set(return_status))
        final_status = max(return_status)

        if len(return_status) != 1:
            # Remove redundant ValidDiagnosis
            return_status.pop(0)

        parse_data['status'] = return_status

        if final_status < threshold:
            final_status = ValidDiagnosis()

        if diagnose:
            return final_status
        else:
            return final_status < BaseDiagnosis.CATEGORIES['THRESHOLD']