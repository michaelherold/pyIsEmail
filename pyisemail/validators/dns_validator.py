import dns.resolver
from pyisemail.diagnosis import DNSDiagnosis, BaseDiagnosis, RFC5321Diagnosis


class DNSValidator(object):

    def is_valid(self, domain):

        return_status = []
        dns_checked = False

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
            parseData[Context.DOMAIN] += '.'

        try:
            result = dns.resolver.query(domain, 'MX')
            dns_checked = True
        except dns.resolver.NXDOMAIN:
            # Domain can't be found in DNS
            return_status.append(DNSDiagnosis('NO_RECORD'))
        except dns.resolver.NoAnswer:
            # MX-record for domain can't be found
            return_status.append(DNSDiagnosis('NO_MX_RECORD'))

            try:
                # TODO: See if we can/need to narrow to A / CNAME
                result = dns.resolver.query(domain)
            except dns.resolver.NoAnswer:
                # No usable records for the domain can be found
                return_status.append(DNSDiagnosis('NO_RECORD'))

        if len(return_status) == 0:
            return True
        else:
            return max(return_status)