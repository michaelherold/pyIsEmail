from pyisemail.diagnosis import BaseDiagnosis
from pyisemail.email_validator import EmailValidator
from pyisemail.reference import Reference
from pyisemail.validators import DNSValidator
from pyisemail.validators import ParserValidator
from pyisemail.version import VERSION

__version__ = VERSION
__all__ = ['is_email']


def is_email(address, check_dns=False, diagnose=False):
    """Validate an email address.

    Keyword arguments:
    address   --- the email address as a string
    check_dns --- flag for whether to check the DNS status of the domain
    diagnose  --- flag for whether to return True/False or a Diagnosis

    """

    threshold = BaseDiagnosis.CATEGORIES["THRESHOLD"]
    d = ParserValidator().is_email(address, True)
    if check_dns is True and d < BaseDiagnosis.CATEGORIES["DNSWARN"]:
        threshold = BaseDiagnosis.CATEGORIES["VALID"]
        d = max(d, DNSValidator().is_valid(address.split("@")[1], True))

    return d if diagnose else d < threshold
