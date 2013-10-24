__author__ = "Michael Herold"
__copyright__ = "Copyright (c) 2012 Michael Herold"
__license__ = "BSD"

import re
import dns.resolver

# Categories
ISEMAIL_VALID_CATEGORY = 1
ISEMAIL_DNSWARN = 7
ISEMAIL_RFC5321 = 15
ISEMAIL_CFWS = 31
ISEMAIL_DEPREC = 63
ISEMAIL_RFC5322 = 127
ISEMAIL_ERR = 255

# Diagnoses
# Address is valid
ISEMAIL_VALID = 0
# Address is valid but a DNS check was not successful
ISEMAIL_DNSWARN_NO_MX_RECORD = 5
ISEMAIL_DNSWARN_NO_RECORD = 6
# Address is valid for SMTP but has unusual elements
ISEMAIL_RFC5321_TLD = 9
ISEMAIL_RFC5321_TLDNUMERIC = 10
ISEMAIL_RFC5321_QUOTEDSTRING = 11
ISEMAIL_RFC5321_ADDRESSLITERAL = 12
ISEMAIL_RFC5321_IPV6DEPRECATED = 13
# Address is valid within the message but cannot be used unmodified for the
# envelope
ISEMAIL_CFWS_COMMENT = 17
ISEMAIL_CFWS_FWS = 18
# Address contains deprecated elements but may still be valid in restricted
# contexts
ISEMAIL_DEPREC_LOCALPART = 33
ISEMAIL_DEPREC_FWS = 34
ISEMAIL_DEPREC_QTEXT = 35
ISEMAIL_DEPREC_QP = 36
ISEMAIL_DEPREC_COMMENT = 37
ISEMAIL_DEPREC_CTEXT = 38
ISEMAIL_DEPREC_CFWS_NEAR_AT = 49
# The address is only valid according to the broad definition of RFC 5322.
# It is otherwise invalid.
ISEMAIL_RFC5322_DOMAIN = 65
ISEMAIL_RFC5322_TOOLONG = 66
ISEMAIL_RFC5322_LOCAL_TOOLONG = 67
ISEMAIL_RFC5322_DOMAIN_TOOLONG = 68
ISEMAIL_RFC5322_LABEL_TOOLONG = 69
ISEMAIL_RFC5322_DOMAINLITERAL = 70
ISEMAIL_RFC5322_DOMLIT_OBSDTEXT = 71
ISEMAIL_RFC5322_IPV6_GRPCOUNT = 72
ISEMAIL_RFC5322_IPV6_2X2XCOLON = 73
ISEMAIL_RFC5322_IPV6_BADCHAR = 74
ISEMAIL_RFC5322_IPV6_MAXGRPS = 75
ISEMAIL_RFC5322_IPV6_COLONSTRT = 76
ISEMAIL_RFC5322_IPV6_COLONEND = 77
# Address is invalid for any purpose
ISEMAIL_ERR_EXPECTING_DTEXT = 129
ISEMAIL_ERR_NOLOCALPART = 130
ISEMAIL_ERR_NODOMAIN = 131
ISEMAIL_ERR_CONSECUTIVEDOTS = 132
ISEMAIL_ERR_ATEXT_AFTER_CFWS = 133
ISEMAIL_ERR_ATEXT_AFTER_QS = 134
ISEMAIL_ERR_ATEXT_AFTER_DOMLIT = 135
ISEMAIL_ERR_EXPECTING_QPAIR = 136
ISEMAIL_ERR_EXPECTING_ATEXT = 137
ISEMAIL_ERR_EXPECTING_QTEXT = 138
ISEMAIL_ERR_EXPECTING_CTEXT = 139
ISEMAIL_ERR_BACKSLASHEND = 140
ISEMAIL_ERR_DOT_START = 141
ISEMAIL_ERR_DOT_END = 142
ISEMAIL_ERR_DOMAINHYPHENSTART = 143
ISEMAIL_ERR_DOMAINHYPHENEND = 144
ISEMAIL_ERR_UNCLOSEDQUOTEDSTR = 145
ISEMAIL_ERR_UNCLOSEDCOMMENT = 146
ISEMAIL_ERR_UNCLOSEDDOMLIT = 147
ISEMAIL_ERR_FWS_CRLF_X2 = 148
ISEMAIL_ERR_FWS_CRLF_END = 149
ISEMAIL_ERR_CR_NO_LF = 150

# function control
ISEMAIL_THRESHOLD = 16

# Email parts
ISEMAIL_COMPONENT_LOCALPART = 0
ISEMAIL_COMPONENT_DOMAIN = 1
ISEMAIL_COMPONENT_LITERAL = 2
ISEMAIL_CONTEXT_COMMENT = 3
ISEMAIL_CONTEXT_FWS = 4
ISEMAIL_CONTEXT_QUOTEDSTRING = 5
ISEMAIL_CONTEXT_QUOTEDPAIR = 6

# Miscellaneous string constants
ISEMAIL_STRING_AT = '@'
ISEMAIL_STRING_BACKSLASH = '\\'
ISEMAIL_STRING_DOT = '.'
ISEMAIL_STRING_DQUOTE = '"'
ISEMAIL_STRING_OPENPARENTHESIS = '('
ISEMAIL_STRING_CLOSEPARENTHESIS = ')'
ISEMAIL_STRING_OPENSQBRACKET = '['
ISEMAIL_STRING_CLOSESQBRACKET = ']'
ISEMAIL_STRING_HYPHEN = '-'
ISEMAIL_STRING_COLON = ':'
ISEMAIL_STRING_DOUBLECOLON = '::'
ISEMAIL_STRING_SP = ' '
ISEMAIL_STRING_HTAB = "\t"
ISEMAIL_STRING_CR = "\r"
ISEMAIL_STRING_LF = "\n"
ISEMAIL_STRING_IPV6TAG = 'IPv6:'
# US-ASCII visible characters not valid for atext 
# (http:#tools.ietf.org/html/rfc5322#section-3.2.3)
ISEMAIL_STRING_SPECIALS = '()<>[]:;@\\,."'

E_ERROR = 1
E_WARNING = 2

DEBUG = False

def _unicode_help(token):
    """Transforms the ASCII control character symbols to their real character.
    
    Note: If the token is not an ASCII control character symbol, just return
    the token.
    
    Keyword arguments:
    token -- the token to transform
    
    """
    if ord(token) in range(9216, 9229+1):
        token = unichr(ord(token) - 9216)
    
    return token

def is_email(email, checkDNS = False, errorLevel = False, parseData = {}):
    """Check that an email address conforms to RFCs 5321, 5322 and others

    As of Version 3.0, we are now distinguishing clearly between a Mailbox
    as defined by RFC 5321 and an addr-spec as defined by RFC 5322. Depending
    on the context, either can be regarded as a valid email address. The
    RFC 5321 Mailbox specification is more restrictive (comments, white space
    and obsolete forms are not allowed)
    
    Keyword arguments:
    email	   -- email address to check.
    checkDNS   -- flag to do a DNS check for MX records
    errorLevel -- the status code below which the email is valid 
    parseData  -- If passed, returns the parsed address components
    
    """

    # Check that $email is a valid address. Read the following RFCs to
    # understand the constraints:
	# 	(http://tools.ietf.org/html/rfc5321)
	# 	(http://tools.ietf.org/html/rfc5322)
	# 	(http://tools.ietf.org/html/rfc4291#section-2.2)
	# 	(http://tools.ietf.org/html/rfc1123#section-2.1)
	# 	(http://tools.ietf.org/html/rfc3696) (guidance only)
    # version 2.0: Enhance $diagnose parameter to $errorlevel
    # version 3.0: Introduced status categories
    # revision 3.1: BUG: $parsedata was passed by value instead of by reference
    if isinstance(errorLevel, bool):
        threshold = ISEMAIL_VALID
        diagnose = errorLevel
    else:
        diagnose = True
        
    if errorLevel == E_WARNING:
        threshold = ISEMAIL_THRESHOLD # For backward compatibility
    elif errorLevel == E_ERROR:
        threshold = ISEMAIL_VALID # For backward compatibility
    else:
        threshold = errorLevel
        
    return_status = [ISEMAIL_VALID]
    
    # Parse the address into components, character by character
    raw_length = len(email)
    context = ISEMAIL_COMPONENT_LOCALPART           # Where we are
    context_stack = [context]                       # Where we've been
    context_prior = ISEMAIL_COMPONENT_LOCALPART     # Where we just came from    
    token = ''                                      # The current character
    token_prior = ''                                # The previous character
    parseData[ISEMAIL_COMPONENT_LOCALPART] = ''     # The address' components
    parseData[ISEMAIL_COMPONENT_DOMAIN] = ''                                  
    atomList = {
        ISEMAIL_COMPONENT_LOCALPART : [''],
        ISEMAIL_COMPONENT_DOMAIN : ['']
    }                                               # The address' dot-atoms
    element_count = 0
    element_len = 0
    hyphen_flag = False         # Hyphen cannot occur at the end of a subdomain
    end_or_die = False          # CFWS can only appear at the end of an element
    skip = False                # Skip flag that simulates i++
    crlf_count = -1             # crlf_count = -1 == !isset(crlf_count)

    if DEBUG:
        print "con\tend\ttok\tret\tcon\tend\ttok\tret\tpar\t\tat"

    for i in xrange(raw_length):
    
        # Skip simulates the use of ++ operator
        if skip:
            skip = False
            continue
            
        token = email[i]
        
        # NoteMJH: Since PHP casts the symbols for ASCII control
        #    characters down to the actual ASCII control characters, we
        #    must do this so ensure it works the same way
        token = _unicode_help(token)

        if DEBUG:
            print u"%i\t%s\t%s\t%i\t" % (context, end_or_die, ord(token), max(return_status)),
        
        # Switch to simulate decrementing; needed for FWS
        repeat = True
        
        while repeat:
            repeat = False
        
            #--------------------------------------------------------
            # Local part
            #--------------------------------------------------------
            if context == ISEMAIL_COMPONENT_LOCALPART:
                # http://tools.ietf.org/html/rfc5322#section-3.4.1
                #   local-part      =   dot-atom / quoted-string /
                #                       obs-local-part
                #
                #   dot-atom        =   [CFWS] dot-atom-text [CFWS]
                #
                #   dot-atom-text   =   1*atext *("." 1*atext)
                #
                #   quoted-string   =   [CFWS]
                #                       DQUOTE *([FWS] qcontent) [FWS] DQUOTE
                #                       [CFWS]
                #
                #   obs-local-part  =   word *("." word)
                #
                #   word            =   atom / quoted-string
                #
                #   atom            =   [CFWS] 1*atext [CFWS]
                if token == ISEMAIL_STRING_OPENPARENTHESIS:
                    if element_len == 0:
                        # Comments are OK at the beginning of an element
                        if element_count == 0:
                            return_status.append(ISEMAIL_CFWS_COMMENT)
                        else:
                            return_status.append(ISEMAIL_DEPREC_COMMENT)
                    else:
                        return_status.append(ISEMAIL_CFWS_COMMENT)
                        # We can't start a comment in the middle of an element,
                        # so this better be the end
                        end_or_die = True
                    
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_COMMENT
                elif token == ISEMAIL_STRING_DOT:
                    if element_len == 0:
                        # Another dot, already? Fatal error
                        if element_count == 0:
                            return_status.append(ISEMAIL_ERR_DOT_START)
                        else:
                            return_status.append(ISEMAIL_ERR_CONSECUTIVEDOTS)
                    else:
                        # The entire local-part can be a quoted string for RFC
                        # 5321. If it's just one atom that is quoted then it's
                        # an RFC 5322 obsolete form
                        if end_or_die:
                            return_status.append(ISEMAIL_DEPREC_LOCALPART)
                        
                        # CFWS & quoted strings are OK again now we're at the
                        # beginning of an element (although they are obsolete
                        # forms)
                        end_or_die = False
                        element_len = 0
                        element_count += 1
                        parseData[ISEMAIL_COMPONENT_LOCALPART] += token
                        atomList[ISEMAIL_COMPONENT_LOCALPART].append('')
                elif token == ISEMAIL_STRING_DQUOTE:
                    if element_len == 0:
                        # The entire local-part can be a quoted string for RFC
                        # 5321. If it's just one atom that is quoted then it's
                        # an RFC 5322 obsolete form
                        if element_count == 0:
                            return_status.append(ISEMAIL_RFC5321_QUOTEDSTRING)
                        else:
                            return_status.append(ISEMAIL_DEPREC_LOCALPART)
                            
                        parseData[ISEMAIL_COMPONENT_LOCALPART] += token
                        atomList[ISEMAIL_COMPONENT_LOCALPART][element_count] += token
                        element_len += 1
                        end_or_die = True
                        context_stack.append(context)
                        context = ISEMAIL_CONTEXT_QUOTEDSTRING
                    else:
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_EXPECTING_ATEXT)
                # Folding White Space (FWS)
                elif token in [ISEMAIL_STRING_CR, ISEMAIL_STRING_SP,
                    ISEMAIL_STRING_HTAB]:
                    
                    # TODO: Clean this up!
                    # Skip simulates the use of ++ operator if the latter check
                    # doesn't short-circuit
                    if token == ISEMAIL_STRING_CR:
                        skip = True

                    if (token == ISEMAIL_STRING_CR and (i+1 == raw_length or 
                        _unicode_help(email[i+1]) != ISEMAIL_STRING_LF)):
                        
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_CR_NO_LF)
                        break
                    
                    if element_len == 0:
                        if element_count == 0:
                            return_status.append(ISEMAIL_CFWS_FWS)
                        else:
                            return_status.append(ISEMAIL_DEPREC_FWS)
                    else:
                        # We can't start FWS in the middle of an element, so
                        # this better be the end
                        end_or_die = True
                    
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_FWS
                    token_prior = token
                # @
                elif token == ISEMAIL_STRING_AT:
                    # At this point we should have a valid local-part
                    if len(context_stack) != 1:
                        raise SystemExit("Unexpected item on context stack")
                    
                    if parseData[ISEMAIL_COMPONENT_LOCALPART] == '':
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_NOLOCALPART)
                    elif element_len == 0:
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_DOT_END)
                    # http://tools.ietf.org/html/rfc5321#section-4.5.3.1.1
                    #   The maximum total length of a user name or other
                    #   local-part is 64 octets.
                    elif len(parseData[ISEMAIL_COMPONENT_LOCALPART]) > 64:
                        return_status.append(ISEMAIL_RFC5322_LOCAL_TOOLONG)
                    # http://tools.ietf.org/html/rfc5322#section-3.4.1
                    #   Comments and folding white space
                    #   SHOULD NOT be used around the "@" in the addr-spec.
                    #
                    # http://tools.ietf.org/html/rfc2119
                    # 4. SHOULD NOT   This phrase, or the phrase "NOT
                    #    RECOMMENDED" mean that there may exist valid reasons
                    #    in particular circumstances when the particular
                    #    behavior is acceptable or even useful, but the full
                    #    implications should be understood and the case
                    #    carefully weighed before implementing any behavior
                    #    described with this label.
                    elif context_prior in [ISEMAIL_CONTEXT_COMMENT,
                        ISEMAIL_CONTEXT_FWS]:
                        return_status.append(ISEMAIL_DEPREC_CFWS_NEAR_AT)
                    
                    # Clear everything down for the domain parsing
                    context = ISEMAIL_COMPONENT_DOMAIN     # Where we are
                    context_stack = []                     # Where we have been
                    element_count = 0
                    element_len = 0
                    # CFWS can only appear at the end of the element
                    end_or_die = False
                # atext
                else:
                    # http://tools.ietf.org/html/rfc5322#section-3.2.3
                    #    atext  =  ALPHA / DIGIT /  ; Printable US-ASCII
                    #              "!" / "#" /      ; characters not including
                    #              "$" / "%" /      ; specials. Used for atoms.
                    #              "&" / "'" /
                    #              "*" / "+" /
                    #              "-" / "/" /
                    #              "=" / "?" /
                    #              "^" / "_" /
                    #              "`" / "{" /
                    #              "|" / "}" /
                    #              "~"
                    if end_or_die:
                        # We have encountered atext where it is no longer valid
                        if context_prior in [ISEMAIL_CONTEXT_COMMENT,
                            ISEMAIL_CONTEXT_FWS]:
                            return_status.append(ISEMAIL_ERR_ATEXT_AFTER_CFWS)
                        elif context_prior == ISEMAIL_CONTEXT_QUOTEDSTRING:
                            return_status.append(ISEMAIL_ERR_ATEXT_AFTER_QS)
                        else:
                            raise SystemExit(
                                ("More atext found where none is allowed, "
                                 "but unrecognized prior context: %s" %
                                 context_prior))
                    else:
                        context_prior = context
                        o = ord(token)
                        
                        if (o < 33 or o > 126 or o == 10 or 
                            token in ISEMAIL_STRING_SPECIALS):
                            # Fatal error
                            return_status.append(ISEMAIL_ERR_EXPECTING_ATEXT)
                            
                        parseData[ISEMAIL_COMPONENT_LOCALPART] += token
                        atomList[ISEMAIL_COMPONENT_LOCALPART][element_count] += token
                        element_len += 1
            #--------------------------------------------------------
            # Domain
            #--------------------------------------------------------
            elif context == ISEMAIL_COMPONENT_DOMAIN:
                # http://tools.ietf.org/html/rfc5322#section-3.4.1
                #   domain         = dot-atom / domain-literal / obs-domain
                #
                #   dot-atom       = [CFWS] dot-atom-text [CFWS]
                #
                #   dot-atom-text  = 1*atext *("." 1*atext)
                #
                #   domain-literal = [CFWS] "[" *([FWS] dtext) [FWS] "]" [CFWS]
                #
                #   dtext          = %d33-90 /     ; Printable US-ASCII
                #                    %d94-126 /    ;  characters not including
                #                    obs-dtext     ;  "[", "]", or "\"
                #
                #   obs-domain     = atom *("." atom)
                #
                #   atom           = [CFWS] 1*atext [CFWS]
                #
                #
                # http://tools.ietf.org/html/rfc5321#section-4.1.2
                #   Mailbox       = Local-part "@" ( Domain / address-literal )
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
                #      contains addressing information specified by and used in
                #      other protocols (e.g., [RFC1034], [RFC1035], [RFC1123],
                #      [RFC5321]).  It is therefore incumbent upon
                #      implementations to conform to the syntax of addresses
                #      for the context in which they are used.
                # is_email() author's note: it's not clear how to interpret
                # this in the context of a general email address validator. The
                # conclusion I have reached is this: "addressing information"
                # must comply with RFC 5321 (and in turn RFC 1035), anything
                # that is "semantically invisible" must comply only with RFC
                # 5322.
                
                # Comment
                if token == ISEMAIL_STRING_OPENPARENTHESIS:
                    if element_len == 0:
                        # Comments at the start of the domain are deprecated in
                        # the text
                        # Comments at the start of a subdomain are obs-domain
                        # (http://tools.ietf.org/html/rfc5322#section-3.4.1)
                        if element_count == 0:
                            return_status.append(ISEMAIL_DEPREC_CFWS_NEAR_AT)
                        else:
                            return_status.append(ISEMAIL_DPREC_COMMENT)
                    else:
                        return_status.append(ISEMAIL_CFWS_COMMENT)
                        # We can't start a comment in the middle of an element,
                        # so this better be the end
                        end_or_die = True
                    
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_COMMENT
                # Next dot-atom element
                elif token == ISEMAIL_STRING_DOT:
                    if element_len == 0:
                        # Another dot, already? Fatal error
                        if element_count == 0:
                            return_status.append(ISEMAIL_ERR_DOT_START)
                        else:
                            return_status.append(ISEMAIL_ERR_CONSECUTIVEDOTS)
                    elif hyphen_flag:
                        # Previous subdomain ended in a hyphen. Fatal error
                        return_status.append(ISEMAIL_ERR_DOMAINHYPHENEND)
                    else:
                        # Nowhere in RFC 5321 does it say explicitly that the
                        # domain part of a Mailbox must be a valid domain
                        # according to the DNS standards set out in RFC 1035,
                        # but this *is* implied in several places. For
                        # instance, wherever the idea of host routing is
                        # discussed the RFC says that the domain must be looked
                        # up in the DNS. This would be nonsense unless the
                        # domain was designed to be a valid DNS domain. Hence
                        # we must conclude that the RFC 1035 restriction on
                        # label length also applies to RFC 5321 domains.
                        #
                        # http://tools.ietf.org/html/rfc1035#section-2.3.4
                        # labels         63 octets or less
                        if element_len > 63:
                            return_status.append(ISEMAIL_RFC5322_LABEL_TOOLONG)
                        
                        # CFWS is OK again now we're at the beginning of an
                        # element (although it may be obsolete CFWS)
                        end_or_die = False
                        element_len = 0
                        element_count += 1
                        atomList[ISEMAIL_COMPONENT_DOMAIN].append('')
                        parseData[ISEMAIL_COMPONENT_DOMAIN] += token
                # Domain literal
                elif token == ISEMAIL_STRING_OPENSQBRACKET:
                    if parseData[ISEMAIL_COMPONENT_DOMAIN] == '':
                        # Domain literal must be the only component
                        end_or_die = True
                        element_len += 1
                        context_stack.append(context)
                        context = ISEMAIL_COMPONENT_LITERAL
                        parseData[ISEMAIL_COMPONENT_DOMAIN] += token
                        atomList[ISEMAIL_COMPONENT_DOMAIN][element_count] += token
                        parseData[ISEMAIL_COMPONENT_LITERAL] = ''
                    else:
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_EXPECTING_ATEXT)
                    
                # Folding White Space (FWS)
                elif token in [ISEMAIL_STRING_CR, ISEMAIL_STRING_SP,
                    ISEMAIL_STRING_HTAB]:
                    
                    # TODO: Clean this up!
                    # Skip simulates the use of ++ operator if the latter check
                    # doesn't short-circuit
                    if token == ISEMAIL_STRING_CR:
                        skip = True
                    
                    if (token == ISEMAIL_STRING_CR and (i+1 == raw_length or
                        _unicode_help(email[i+1]) != ISEMAIL_STRING_LF)):
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_CR_NO_LF)
                        break
                    
                    if element_len == 0:
                        if element_count == 0:
                            return_status.append(ISEMAIL_DEPREC_CFWS_NEAR_AT)
                        else:
                            return_status.append(ISEMAIL_DEPREC_FWS)
                    else:
                        return_status.append(ISEMAIL_CFWS_FWS)
                        # We can't start FWS in the middle of an element, so
                        # this better be the end
                        end_or_die = True
                        
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_FWS
                    token_prior = token
                # atext
                else:
                    # RFC 5322 allows any atext...
                    # http://tools.ietf.org/html/rfc5322#section-3.2.3
                    #    atext  =  ALPHA / DIGIT / ; Printable US-ASCII
                    #              "!" / "#" /     ; characters not including
                    #              "$" / "%" /     ; specials.  Used for atoms.
                    #              "&" / "'" /
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
                        # We have encountered atext where it is no longer valid
                        if context_prior in [ISEMAIL_CONTEXT_COMMENT,
                            ISEMAIL_CONTEXT_FWS]:
                            return_status.append(ISEMAIL_ERR_ATEXT_AFTER_CFWS)
                        elif context_prior == ISEMAIL_COMPONENT_LITERAL:
                            return_status.append(ISEMAIL_ERR_ATEXT_AFTER_DOMLIT)
                        else:
                            raise SystemExit(
                                ("More atext found where none is allowed, but"
                                 "unrecognised prior context: %s" %
                                 context_prior))
                    
                    
                    o = ord(token)
                    # Assume this token isn't a hyphen unless we discover it is
                    hyphen_flag = False
                    
                    if (o < 33 or o > 126 or
                        token in ISEMAIL_STRING_SPECIALS):
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_EXPECTING_ATEXT)
                    elif token == ISEMAIL_STRING_HYPHEN:
                        if element_len == 0:
                            # Hyphens can't be at the beginning of a subdomain
                            # Fatal error
                            return_status.append(ISEMAIL_ERR_DOMAINHYPHENSTART)
                        
                        hyphen_flag = True
                    elif not ((o > 47 and o < 58) or
                        (o > 64 and o < 91) or
                        (o > 96 and o < 123)):
                        # Not an RFC 5321 subdomain, but still OK by RFC 5322
                        return_status.append(ISEMAIL_RFC5322_DOMAIN)
                    
                    parseData[ISEMAIL_COMPONENT_DOMAIN] += token
                    atomList[ISEMAIL_COMPONENT_DOMAIN][element_count] += token
                    element_len += 1
            #--------------------------------------------------------
            # Domain literal
            #--------------------------------------------------------
            elif context == ISEMAIL_COMPONENT_LITERAL:
                # http://tools.ietf.org/html/rfc5322#section-3.4.1
                #   domain-literal  =   [CFWS] "[" *([FWS] dtext) [FWS] "]" [CFWS]
                #
                #   dtext           =   %d33-90 /     ; Printable US-ASCII
                #                       %d94-126 /    ;  characters not including
                #                       obs-dtext     ;  "[", "]", or "\"
                #
                #   obs-dtext       =   obs-NO-WS-CTL / quoted-pair
                
                # End of domain literal
                if token == ISEMAIL_STRING_CLOSESQBRACKET:
                    if max(return_status) < ISEMAIL_DEPREC:
                        # Could be a valid RFC 5321 address literal, so let's
                        # check
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
                        #                     ; specified in a Standards-Track
                        #                     ; RFC and registered with IANA
                        #
                        #   dcontent       = %d33-90 / ; Printable US-ASCII
                        #                    %d94-126  ; excl. "[", "\", "]"
                        #
                        #   Snum           = 1*3DIGIT
                        #                  ; representing a decimal integer
                        #                  ; value in the range 0 through 255
                        #
                        #   IPv6-addr      = IPv6-full / IPv6-comp /
                        #                    IPv6v4-full / IPv6v4-comp
                        #
                        #   IPv6-hex       = 1*4HEXDIG
                        #
                        #   IPv6-full      = IPv6-hex 7(":" IPv6-hex)
                        #
                        #   IPv6-comp      = [IPv6-hex *5(":" IPv6-hex)] "::"
                        #                    [IPv6-hex *5(":" IPv6-hex)]
                        #                  ; The "::" represents at least 2
                        #                  ; 16-bit groups of zeros. No more
                        #                  ; than 6 groups in addition to the
                        #                  ; "::" may be present.
                        #
                        #   IPv6v4-full    = IPv6-hex 5(":" IPv6-hex) ":" 
                        #                    IPv4-address-literal
                        #
                        #   IPv6v4-comp    = [IPv6-hex *3(":" IPv6-hex)] "::"
                        #                    [IPv6-hex *3(":" IPv6-hex) ":"]
                        #                    IPv4-address-literal
                        #                  ; The "::" represents at least 2
                        #                  ; 16-bit groups of zeros.  No more
                        #                  ; than 4 groups in addition to the
                        #                  ; "::" and IPv4-address-literal may
                        #                  ; be present.
                        
                        max_groups = 8
                        index = False
                        addressLiteral = parseData[ISEMAIL_COMPONENT_LITERAL]
                        
                        # Extract IPv4 part from the end of the address-literal
                        # (if there is one)
                        regex = (   
                            r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)"
                            r"{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
                        )
                        matchesIP = re.search(regex, addressLiteral)
                        if matchesIP:
                            index = addressLiteral.rfind(matchesIP.group(0))
                            if index != 0:
                                # Convert IPv4 part to IPv6 format for further 
                                # testing
                                addressLiteral = addressLiteral[0:index] + '0:0'
                        
                        if index == 0 and index is not False:
                            # Nothing there except a valid IPv4 address, so ...
                            return_status.append(ISEMAIL_RFC5321_ADDRESSLITERAL)
                        elif not addressLiteral.startswith(ISEMAIL_STRING_IPV6TAG):
                            return_status.append(ISEMAIL_RFC5322_DOMAINLITERAL)
                        else:
                            IPv6 = addressLiteral[5:]
                            # Revision 2.7: Daniel Marschall's new IPv6 testing
                            # strategy
                            matchesIP = IPv6.split(ISEMAIL_STRING_COLON)
                            groupCount = len(matchesIP)
                            index = IPv6.find(ISEMAIL_STRING_DOUBLECOLON)
                            
                            if index == -1:
                                # we need exactly the right number of groups
                                if groupCount != max_groups:
                                    return_status.append(
                                        ISEMAIL_RFC5322_IPV6_GRPCOUNT
                                    )
                            else:                                
                                if index != IPv6.rfind(ISEMAIL_STRING_DOUBLECOLON):
                                    return_status.append(
                                        ISEMAIL_RFC5322_IPV6_2X2XCOLON
                                    )
                                else:
                                    if index == 0 or index == len(IPv6) - 2:
                                        # RFC 4291 allows :: at the start or
                                        # end of an address with 7 other groups
                                        # in addition
                                        max_groups += 1
                                        
                                    if groupCount > max_groups:
                                        return_status.append(
                                            ISEMAIL_RFC5322_IPV6_MAXGRPS
                                        )
                                    elif groupCount == max_groups:
                                        # Eliding a single "::"
                                        return_status.append(
                                            ISEMAIL_RFC5321_IPV6DEPRECATED
                                        )
                            
                            # Revision 2.7: Daniel Marschall's new IPv6 testing
                            # strategy
                            if (IPv6[0] == ISEMAIL_STRING_COLON and 
                                IPv6[1] != ISEMAIL_STRING_COLON):
                                # Address starts with a single colon
                                return_status.append(ISEMAIL_RFC5322_IPV6_COLONSTRT)
                            elif (IPv6[-1] == ISEMAIL_STRING_COLON and
                                  IPv6[-2] != ISEMAIL_STRING_COLON):
                                # Address ends with a single colon
                                return_status.append(ISEMAIL_RFC5322_IPV6_COLONEND)
                            elif ([re.match(r"^[0-9A-Fa-f]{0,4}$", i)
                                  for i in matchesIP].count(None) != 0):
                                # Check for unmatched characters
                                return_status.append(ISEMAIL_RFC5322_IPV6_BADCHAR)
                            else:
                                return_status.append(ISEMAIL_RFC5321_ADDRESSLITERAL)
                    else:
                        return_status.append(ISEMAIL_RFC5322_DOMAINLITERAL)
                    
                    parseData[ISEMAIL_COMPONENT_DOMAIN] += token
                    atomList[ISEMAIL_COMPONENT_DOMAIN][element_count] += token
                    element_len += 1
                    context_prior = context
                    context = context_stack.pop()
                elif token == ISEMAIL_STRING_BACKSLASH:
                    return_status.append(ISEMAIL_RFC5322_DOMLIT_OBSDTEXT)
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_QUOTEDPAIR
                # Folding White Space (FWS)
                elif token in [ISEMAIL_STRING_CR, ISEMAIL_STRING_SP,
                    ISEMAIL_STRING_HTAB]:
                    
                    # TODO: Clean this up!
                    # Skip simulates the use of ++ operator if the latter check
                    # doesn't short-circuit
                    if token == ISEMAIL_STRING_CR:
                        skip = True
                    
                    if (token == ISEMAIL_STRING_CR and (i+1 == raw_length or
                        _unicode_help(email[i+1]) != ISEMAIL_STRING_LF)):
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_CR_NO_LF)
                        break
                    
                    return_status.append(ISEMAIL_CFWS_FWS)
                    
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_FWS
                    token_prior = token
                # dtext
                else:
                    # http://tools.ietf.org/html/rfc5322#section-3.4.1
                    #   dtext         = %d33-90 /   ; Printable US-ASCII
                    #                   %d94-126 /  ;  characters not including
                    #                   obs-dtext   ;  "[", "]", or "\"
                    #
                    #   obs-dtext     = obs-NO-WS-CTL / quoted-pair
                    #
                    #   obs-NO-WS-CTL = %d1-8 /     ; US-ASCII control
                    #                   %d11 /      ;  characters that do not
                    #                   %d12 /      ;  include the carriage
                    #                   %d14-31 /   ;  return, line feed, and
                    #                   %d127       ;  white space characters
                    o = ord(token)
                    
                    # CR, LF, SP & HTAB have already been parsed above
                    if (o > 127 or o == 0 or 
                        token == ISEMAIL_STRING_OPENSQBRACKET):
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_EXPECTING_DTEXT)
                        break
                    elif o < 33 or o == 127:
                        return_status.append(ISEMAIL_RFC5322_DOMLIT_OBSDTEXT)
                    
                    
                    parseData[ISEMAIL_COMPONENT_LITERAL] += token
                    parseData[ISEMAIL_COMPONENT_DOMAIN] += token
                    atomList[ISEMAIL_COMPONENT_DOMAIN][element_count] += token
                    element_len += 1
            #--------------------------------------------------------
            # Quoted string
            #--------------------------------------------------------
            elif context == ISEMAIL_CONTEXT_QUOTEDSTRING:
                # http://tools.ietf.org/html/rfc5322#section-3.2.4
                #   quoted-string   =   [CFWS]
                #                       DQUOTE *([FWS] qcontent) [FWS] DQUOTE
                #                       [CFWS]
                #
                #   qcontent        =   qtext / quoted-pair
                
                # Quoted pair
                if token == ISEMAIL_STRING_BACKSLASH:
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_QUOTEDPAIR
                # Foloing White Space (FWS)
                # Inside a quoted string, spaces are allow as regular
                # characters. It's only FWS if we include HTAB or CRLF
                elif token in [ISEMAIL_STRING_CR, ISEMAIL_STRING_HTAB]:
                    
                    # TODO: Clean this up!
                    # Skip simulates the use of ++ operator if the latter check
                    # doesn't short-circuit
                    if token == ISEMAIL_STRING_CR:
                        skip = True
                
                    if (token == ISEMAIL_STRING_CR and (i+1 == raw_length or
                        _unicode_help(email[i+1]) != ISEMAIL_STRING_LF)):
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_CR_NO_LF)
                        break
                        
                    # http://tools.ietf.org/html/rfc5322#section-3.2.2
                    #   Runs of FWS, comment, or CFWS that occur between
                    #   lexical tokens in a structured header field are
                    #   semantically interpreted as a single space character.

                    # http://tools.ietf.org/html/rfc5322#section-3.2.4
                    #   the CRLF in any FWS/CFWS that appears within the quoted
                    #   string [is] semantically "invisible" and therefore not
                    #   part of the quoted-string
                    parseData[ISEMAIL_COMPONENT_LOCALPART] += ISEMAIL_STRING_SP
                    atomList[ISEMAIL_COMPONENT_LOCALPART][element_count] += (
                        ISEMAIL_STRING_SP)
                    element_len += 1
                    
                    return_status.append(ISEMAIL_CFWS_FWS)
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_FWS
                    token_prior = token
                # End of quoted string
                elif token == ISEMAIL_STRING_DQUOTE:
                    parseData[ISEMAIL_COMPONENT_LOCALPART] += token
                    atomList[ISEMAIL_COMPONENT_LOCALPART][element_count] += token
                    element_len += 1
                    context_prior = context
                    context	= context_stack.pop()
                # qtext
                else:
                    # http://tools.ietf.org/html/rfc5322#section-3.2.4
                    #   qtext          =  %d33 /      ; Printable US-ASCII
                    #                     %d35-91 /   ;  characters not
                    #                     %d93-126 /  ;  including "\" or the
                    #                     obs-qtext   ;  quote character
                    #                  
                    #   obs-qtext      =  obs-NO-WS-CTL
                    #                  
                    #   obs-NO-WS-CTL  =  %d1-8 /     ; US-ASCII control
                    #                     %d11 /      ;  characters that do not
                    #                     %d12 /      ;  include the carriage
                    #                     %d14-31 /   ;  return, line feed, and
                    #                     %d127       ;  white space characters
                    o = ord(token)
                    
                    if o > 127 or o == 0 or o == 10:
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_EXPECTING_QTEXT)
                    elif o < 32 or o == 127:
                        return_status.append(ISEMAIL_DEPREC_QTEXT)
                        
                    parseData[ISEMAIL_COMPONENT_LOCALPART] += token
                    atomList[ISEMAIL_COMPONENT_LOCALPART][element_count] += token
                    element_len += 1
                
                # TODO
                # http://tools.ietf.org/html/rfc5322#section-3.4.1
                #   If the string can be represented as a dot-atom (that is, it
                #   contains no characters other than atext characters or "."
                #   surrounded by atext characters), then the dot-atom form
                #   SHOULD be used and the quoted-string form SHOULD NOT be
                #   used.
                
            #--------------------------------------------------------
            # Quoted pair
            #--------------------------------------------------------
            elif context == ISEMAIL_CONTEXT_QUOTEDPAIR:
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
                    return_status.append(ISEMAIL_ERR_EXPECTING_QPAIR)
                elif (o < 31 and o != 9) or o == 127:
                    # SP & HTAB are allowed
                    return_status.append(ISEMAIL_DEPREC_QP)
                    
                # At this point we know where this qpair occurred so
                # we could check to see if the character actually
                # needed to be quoted at all.
                # http://tools.ietf.org/html/rfc5321#section-4.1.2
                #   the sending system SHOULD transmit the
                #   form that uses the minimum quoting possible.
                # TODO: check whether the character needs to be quoted
                #       (escaped) in this context
                
                context_prior = context
                context = context_stack.pop()   # End of qpair
                token = ISEMAIL_STRING_BACKSLASH + token
                
                if context == ISEMAIL_CONTEXT_COMMENT:
                    pass
                elif context == ISEMAIL_CONTEXT_QUOTEDSTRING:
                    parseData[ISEMAIL_COMPONENT_LOCALPART] += token
                    atomList[ISEMAIL_COMPONENT_LOCALPART][element_count] += token
                    # The maximum sizes specified by RFC 5321 are octet counts,
                    # so we must include the backslash
                    element_len += 2
                elif context == ISEMAIL_COMPONENT_LITERAL:
                    parseData[ISEMAIL_COMPONENT_DOMAIN] += token
                    atomList[ISEMAIL_COMPONENT_DOMAIN][element_count] += token
                    # The maximum sizes specified by RFC 5321 are octet counts,
                    # so we must include the backslash
                    element_len += 2
                else:
                    SystemExit(
                        ("Quoted pair logic invoked in an invalid "
                         "context: %s" % context))
            
            #--------------------------------------------------------
            # Comment
            #--------------------------------------------------------
            elif context == ISEMAIL_CONTEXT_COMMENT:
                # http://tools.ietf.org/html/rfc5322#section-3.2.2
                #   comment         =   "(" *([FWS] ccontent) [FWS] ")"
                #
                #   ccontent        =   ctext / quoted-pair / comment
                
                # Nested comment
                if token == ISEMAIL_STRING_OPENPARENTHESIS:
                    # Nested comments are OK
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_COMMENT
                # End of comment
                elif token == ISEMAIL_STRING_CLOSEPARENTHESIS:
                    context_prior = context
                    context = context_stack.pop()
                    
                    # http://tools.ietf.org/html/rfc5322#section-3.2.2
                    #   Runs of FWS, comment, or CFWS that occur between
                    #   lexical tokens in a structured header field are
                    #   semantically interpreted as a single space character.
                    #
                    # is_email() author's note: This *cannot* mean that we must
                    # add a space to the address wherever CFWS appears. This
                    # would result in any addr-spec that had CFWS outside a
                    # quoted string being invalid for RFC 5321.
                    
                    # if context in [ISEMAIL_COMPONENT_LOCALPART,
                    #    ISEMAIL_COMPONENT_DOMAIN]:
                    #    parseData[context] += ISEMAIL_STRING_SP
                    #    atomList[context][element_count] += ISEMAIL_STRING_SP
                    #    element_len += 1
                # Quoted pair
                elif token == ISEMAIL_STRING_BACKSLASH:
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_QUOTEDPAIR
                # Folding White Space (FWS)
                elif token in [ISEMAIL_STRING_CR, ISEMAIL_STRING_SP,
                    ISEMAIL_STRING_HTAB]:
                    
                    # TODO: Clean this up!
                    # Skip simulates the use of ++ operator if the latter check
                    # doesn't short-circuit
                    if token == ISEMAIL_STRING_CR:
                        skip = True
                    
                    if token == ISEMAIL_STRING_CR and (i+1 == raw_length or
                        _unicode_help(email[i+1]) != ISEMAIL_STRING_LF):
                        
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_CR_NO_LF)
                        break
                        
                    return_status.append(ISEMAIL_CFWS_FWS)
                    
                    context_stack.append(context)
                    context = ISEMAIL_CONTEXT_FWS
                    token_prior = token
                # ctext
                else:
                    # http://tools.ietf.org/html/rfc5322#section-3.2.3
                    #   ctext           =   %d33-39 /   ; Printable US-ASCII
                    #                       %d42-91 /   ;  characters not 
                    #                       %d93-126 /  ;  including "(", ")",
                    #                       obs-ctext   ;  or "\"
                    #
                    #   obs-ctext       =   obs-NO-WS-CTL
                    #
                    #   obs-NO-WS-CTL   =   %d1-8 /      ; US-ASCII control
                    #                       %d11 /       ;  characters that do
                    #                       %d12 /       ;  not include the
                    #                       %d14-31 /    ;  carriage return, 
                    #                       %d127        ;  line feed, and 
                    #                                    ;  white space
                    #                                    ;  characters
                    
                    o = ord(token)
                    
                    if o > 127 or o == 0 or o == 10:
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_EXPECTING_CTEXT)
                        break
                    elif o < 32 or o == 127:
                        return_status.append(ISEMAIL_DEPREC_CTEXT)
                    
            
            #--------------------------------------------------------
            # Folding White Space (FWS)
            #--------------------------------------------------------
            elif context == ISEMAIL_CONTEXT_FWS:
                # http://tools.ietf.org/html/rfc5322#section-3.2.2
                #   FWS             =   ([*WSP CRLF] 1*WSP) /  obs-FWS
                #                       ; Folding white space
                #
                # But note the erratum:
                # http://www.rfc-editor.org/errata_search.php?rfc=5322&eid=1908:
                #   In the obsolete syntax, any amount of folding white space
                #   MAY be inserted where the obs-FWS rule is allowed.  This
                #   creates the possibility of having two consecutive "folds"
                #   in a line, and therefore the possibility that a line which
                #   makes up a folded header field could be composed entirely
                #   of white space.
                #
                #   obs-FWS         =   1*([CRLF] WSP)
                
                if token_prior == ISEMAIL_STRING_CR:
                    if token == ISEMAIL_STRING_CR:
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_FWS_CRLF_X2)
                        break
                    
                    if crlf_count != -1:
                        crlf_count += 1
                        if crlf_count > 1:
                            # Multiple folds = obsolete FWS
                            return_status.append(ISEMAIL_DEPREC_FWS)
                    else:
                        crlf_count = 1
                
                if token == ISEMAIL_STRING_CR:
                    
                    # Skip simulates the use of ++ operator
                    skip = True
                
                    if (i+1 == raw_length or
                        _unicode_help(email[i+1]) != ISEMAIL_STRING_LF):
                                                
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_CR_NO_LF)
                elif token in [ISEMAIL_STRING_SP, ISEMAIL_STRING_HTAB]:
                    pass
                else:
                    if token_prior == ISEMAIL_STRING_CR:
                        # Fatal error
                        return_status.append(ISEMAIL_ERR_FWS_CRLF_END)
                        break
                    
                    if crlf_count != -1:
                        crlf_count = -1
                    
                    context_prior = context
                    # End of FWS
                    context = context_stack.pop()
                    
                    # http://tools.ietf.org/html/rfc5322#section-3.2.2
                    #   Runs of FWS, comment, or CFWS that occur between
                    #   lexical tokens in a structured header field are
                    #   semantically interpreted as a single space character.
                    #
                    # is_email() author's note: This *cannot* mean that we must
                    # add a space to the address wherever CFWS appears. This
                    # would result in any addr-spec that had CFWS outside a
                    # quoted string being invalid for RFC 5321.
                    
                    # if context in [ISEMAIL_COMPONENT_LOCALPART,
                    #    ISEMAIL_COMPONENT_DOMAIN]:
                    #    parseData[context] += ISEMAIL_STRING_SP
                    #    atomList[context][element_count] += ISEMAIL_STRING_SP
                    #    element_len += 1
                    
                    # Look at this token again in the parent context
                    repeat = True
                
                token_prior = token
                
            #--------------------------------------------------------
            # A context we aren't expecting
            #--------------------------------------------------------
            else:
                SystemExit("Unknown context: %s" % context)
                
        if DEBUG:
            print u"%i\t%s\t%s\t%i\t%s" % (context, end_or_die, ord(token), max(return_status), str(parseData))

        # No point in going on if we've got a fatal error
        if max(return_status) > ISEMAIL_RFC5322:
            break
    
    
        
    # Some simple final tests
    if max(return_status) < ISEMAIL_RFC5322:
        if context == ISEMAIL_CONTEXT_QUOTEDSTRING:
            # Fatal error
            return_status.append(ISEMAIL_ERR_UNCLOSEDQUOTEDSTR)
        elif context == ISEMAIL_CONTEXT_QUOTEDPAIR:
            # Fatal error
            return_status.append(ISEMAIL_ERR_BACKSLASHEND)
        elif context == ISEMAIL_CONTEXT_COMMENT:
            # Fatal error
            return_status.append(ISEMAIL_ERR_UNCLOSEDCOMMENT)
        elif context == ISEMAIL_COMPONENT_LITERAL:
            # Fatal error
            return_status.append(ISEMAIL_ERR_UNCLOSEDDOMLIT)
        elif token == ISEMAIL_STRING_CR:
            # Fatal error
            return_status.append(ISEMAIL_ERR_FWS_CRLF_END)
        elif parseData[ISEMAIL_COMPONENT_DOMAIN] == '':
            # Fatal error
            return_status.append(ISEMAIL_ERR_NODOMAIN)
        elif element_len == 0:
            # Fatal error
            return_status.append(ISEMAIL_ERR_DOT_END)
        elif hyphen_flag:
            # Fatal error
            return_status.append(ISEMAIL_ERR_DOMAINHYPHENEND)
        # http://tools.ietf.org/html/rfc5321#section-4.5.3.1.2
		#   The maximum total length of a domain name or number is 255 octets.
        elif len(parseData[ISEMAIL_COMPONENT_DOMAIN]) > 255:
            return_status.append(ISEMAIL_RFC5322_DOMAIN_TOOLONG)
        # http://tools.ietf.org/html/rfc5321#section-4.1.2
		#   Forward-path   = Path
		#
		#   Path           = "<" [ A-d-l ":" ] Mailbox ">"
		#
		# http://tools.ietf.org/html/rfc5321#section-4.5.3.1.3
		#   The maximum total length of a reverse-path or forward-path is 256
		#   octets (including the punctuation and element separators).
		#
		# Thus, even without (obsolete) routing information, the Mailbox can
		# only be 254 characters long. This is confirmed by this verified
		# erratum to RFC 3696:
		#
		# http://www.rfc-editor.org/errata_search.php?rfc=3696&eid=1690
		#   However, there is a restriction in RFC 2821 on the length of an
		#   address in MAIL and RCPT commands of 254 characters.  Since
        #   addresses that do not fit in those fields are not normally useful,
        #   the upper limit on address lengths should normally be considered to
        #   be 254.
        elif len(parseData[ISEMAIL_COMPONENT_LOCALPART] + ISEMAIL_STRING_AT +
                 parseData[ISEMAIL_COMPONENT_DOMAIN]) > 254:
            return_status.append(ISEMAIL_RFC5322_TOOLONG)
        # http://tools.ietf.org/html/rfc1035#section-2.3.4
		# labels           63 octets or less
        elif element_len > 63:
            return_status.append(ISEMAIL_RFC5322_LABEL_TOOLONG)
            
    # Check DNS?
    dns_checked = False
    
    if checkDNS and max(return_status) < ISEMAIL_DNSWARN:
        # http://tools.ietf.org/html/rfc5321#section-2.3.5
		#   Names that can
		#   be resolved to MX RRs or address (i.e., A or AAAA) RRs (as
        #   discussed in Section 5) are permitted, as are CNAME RRs whose
        #   targets can be resolved, in turn, to MX or address RRs.
		#
		# http://tools.ietf.org/html/rfc5321#section-5.1
		#   The lookup first attempts to locate an MX record associated with
        #   the name.  If a CNAME record is found, the resulting name is
        #   processed as if it were the initial name. ... If an empty list of
        #   MXs is returned, the address is treated as if it was associated
        #   with an implicit MX RR, with a preference of 0, pointing to that
        #   host.
		#
		# is_email() author's note: We will regard the existence of a CNAME to
        # be sufficient evidence of the domain's existence. For performance
        # reasons we will not repeat the DNS lookup for the CNAME's target, but
        # we will raise a warning because we didn't immediately find an MX
        # record.
        
        # Checking TLD DNS seems to work only if you explicitly check for the
        # root
        if element_count == 0:
            parseData[ISEMAIL_COMPONENT_DOMAIN] += '.'
        
        try:
            result = dns.resolver.query(parseData[ISEMAIL_COMPONENT_DOMAIN],
                'MX')
            dns_checked = True
        except dns.resolver.NXDOMAIN:
            # Domain can't be found in DNS
            return_status.append(ISEMAIL_DNSWARN_NO_RECORD)
        except dns.resolver.NoAnswer:
            # MX-record for domain can't be found
            return_status.append(ISEMAIL_DNSWARN_NO_MX_RECORD)
            
            try:
                # TODO: See if we can/need to narrow to A / CNAME
                result = dns.resolver.query(parseData[ISEMAIL_COMPONENT_DOMAIN])
            except dns.resolver.NoAnswer:
                # No usable records for the domain can be found
                return_status.append(ISEMAIL_DNSWARN_NO_RECORD)
            
    # Check for TLD addresses
	# -----------------------
	# TLD addresses are specifically allowed in RFC 5321 but they are
	# unusual to say the least. We will allocate a separate
	# status to these addresses on the basis that they are more likely
	# to be typos than genuine addresses (unless we've already
	# established that the domain does have an MX record)
	#
	# http://tools.ietf.org/html/rfc5321#section-2.3.5
	#   In the case
	#   of a top-level domain used by itself in an email address, a single
	#   string is used without any dots.  This makes the requirement,
	#   described in more detail below, that only fully-qualified domain
	#   names appear in SMTP transactions on the public Internet,
	#   particularly important where top-level domains are involved.
	#
	# TLD format
	# ----------
	# The format of TLDs has changed a number of times. The standards
	# used by IANA have been largely ignored by ICANN, leading to
	# confusion over the standards being followed. These are not defined
	# anywhere, except as a general component of a DNS host name (a label).
	# However, this could potentially lead to 123.123.123.123 being a
	# valid DNS name (rather than an IP address) and thereby creating
	# an ambiguity. The most authoritative statement on TLD formats that
	# the author can find is in a (rejected!) erratum to RFC 1123
	# submitted by John Klensin, the author of RFC 5321:
	#
	# http://www.rfc-editor.org/errata_search.php?rfc=1123&eid=1353
	#   However, a valid host name can never have the dotted-decimal
	#   form #.#.#.#, since this change does not permit the highest-level
	#   component label to start with a digit even if it is not all-numeric.
    
    if not dns_checked and max(return_status) < ISEMAIL_DNSWARN:
        if element_count == 0:
            return_status.append(ISEMAIL_RFC5321_TLD)
        
        try:
            float(atomList[ISEMAIL_COMPONENT_DOMAIN][element_count][0])
            return_status.append(ISEMAIL_RFC5321_TLDNUMERIC)
        except ValueError:
            pass
            
    return_status = list(set(return_status))
    final_status = max(return_status)
    
    if len(return_status) != 1:
        # Remove redundant ISEMAIL_VALID
        return_status.pop(0)
        
    parseData['status'] = return_status
    
    if final_status < threshold:
        final_status = ISEMAIL_VALID
    
    return final_status if diagnose else final_status < ISEMAIL_THRESHOLD
