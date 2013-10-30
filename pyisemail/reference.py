class Reference(object):

    """A container for diagnosis references, for more information.

    Holds the citation in the pertinent RFC, as well as a link to the specific
    section of the RFC being referred to.

    """

    DATA = {
        'local-part': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC5322 section 3.4.1",
        },
        'local-part-maximum': {
            'link': "http://tools.ietf.org/html/rfc5321#section-4.5.3.1.1",
            'citation': "RFC5321 section 4.5.3.1.1",
        },
        'obs-local-part': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC 5322 section 3.4.1",
        },
        'dot-atom': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC 5322 section 3.4.1",
        },
        'quoted-string': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC 5322 section 3.4.1",
        },
        'CFWS-near-at': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC 5322 section 3.4.1",
        },
        'SHOULD-NOT': {
            'link': "http://tools.ietf.org/html/rfc2119",
            'citation': "RFC2119 section 4",
        },
        'atext': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.2.3",
            'citation': "RFC5322 section 3.2.3",
        },
        'obs-domain': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC5322 section 3.4.1",
        },
        'domain-RFC5322': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC5322 section 3.4.1",
        },
        'domain-RFC5321': {
            'link': "http://tools.ietf.org/html/rfc5321#section-4.1.2",
            'citation': "RFC5321 section 4.1.2",
        },
        'label': {
            'link': "http://tools.ietf.org/html/rfc1035#section-2.3.4",
            'citation': "RFC1035 section 2.3.4",
        },
        'CRLF': {
            'link': "http://tools.ietf.org/html/rfc5234#section-2.3",
            'citation': "RFC5234 section 2.3",
        },
        'CFWS': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.2.2",
            'citation': "RFC5322 section 3.2.2",
        },
        'domain-literal': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC5322 section 3.4.1",
        },
        'address-literal': {
            'link': "http://tools.ietf.org/html/rfc5321#section-4.1.2",
            'citation': "RFC5321 section 4.1.2",
        },
        'address-literal-IPv4': {
            'link': "http://tools.ietf.org/html/rfc5321#section-4.1.3",
            'citation': "RFC5321 section 4.1.3",
        },
        'address-literal-IPv6': {
            'link': "http://tools.ietf.org/html/rfc5321#section-4.1.3",
            'citation': "RFC5321 section 4.1.3",
        },
        'dtext': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC5322 section 3.4.1",
        },
        'obs-dtext': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC5322 section 3.4.1",
        },
        'qtext': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.2.4",
            'citation': "RFC5322 section 3.2.4",
        },
        'obs-qtext': {
            'link': "http://tools.ietf.org/html/rfc5322#section-4.1",
            'citation': "RFC5322 section 4.1",
        },
        'ctext': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.2.3",
            'citation': "RFC5322 section 3.2.3",
        },
        'obs-ctext': {
            'link': "http://tools.ietf.org/html/rfc5322#section-4.1",
            'citation': "RFC5322 section 4.1",
        },
        'quoted-pair': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.2.1",
            'citation': "RFC5322 section 3.2.1",
        },
        'obs-qp': {
            'link': "http://tools.ietf.org/html/rfc5322#section-4.1",
            'citation': "RFC5322 section 4.1",
        },
        'TLD': {
            'link': "http://tools.ietf.org/html/rfc5321#section-2.3.5",
            'citation': "RFC5321 section 2.3.5",
        },
        'TLD-format': {
            'link': "http://www.rfc-editor.org/errata_search.php?eid=1353",
            'citation': "John Klensin, RFC 1123 erratum 1353",
        },
        'mailbox-maximum': {
            'link': "http://www.rfc-editor.org/errata_search.php?eid=1690",
            'citation': "Dominic Sayers, RFC 3696 erratum 1690",
        },
        'domain-maximum': {
            'link': "http://tools.ietf.org/html/rfc1035#section-4.5.3.1.2",
            'citation': "RFC 5321 section 4.5.3.1.2",
        },
        'mailbox': {
            'link': "http://tools.ietf.org/html/rfc5321#section-4.1.2",
            'citation': "RFC 5321 section 4.1.2",
        },
        'addr-spec': {
            'link': "http://tools.ietf.org/html/rfc5322#section-3.4.1",
            'citation': "RFC 5322 section 3.4.1",
        },
    }

    def __init__(self, name=""):
        data = self.DATA.get(name, {'link': "", 'citation': ""})
        self.link = data['link']
        self.citation = data['citation']

    def __repr__(self):
        return "%s (%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "%s <%s>" % (self.citation, self.link)
