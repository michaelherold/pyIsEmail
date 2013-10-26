from pyisemail.grammars import RFC2822, RFC5322, RFC5322Obsolete


class EmailValidator(object):

    def __init__(self):
        self.grammars = {
            'rfc2822': RFC2822(),
            'rfc5322': RFC5322(),
            'rfc5322_obsolete': RFC5322Obsolete()
        }

    def is_email(self, address, diagnose=False, grammar='rfc5322'):
        return self.grammars[grammar].parse(address, diagnose)

    is_valid = is_email
