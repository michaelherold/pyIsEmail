from pyisemail import EmailValidator
from pyisemail.grammars import RFC2822, RFC5322, RFC5322Obsolete


class GrammarValidator(EmailValidator):

    def __init__(self):
        self.grammars = {
            'rfc2822': RFC2822(),
            'rfc5322': RFC5322(),
            'rfc5322_obsolete': RFC5322Obsolete()
        }

    def is_email(self, address, diagnose=False):
        return self.grammars['rfc5322'].parse(address, diagnose)
