__version__ = '0.0.1'
__author__ = "Michael Herold"

from pyisemail.diagnosis import BaseDiagnosis
from pyisemail.email_validator import EmailValidator
from pyisemail.reference import Reference
from pyisemail.validators import ParserValidator
from pyisemail.validators.dns_validator import DNSValidator


def is_email(address, check_dns=False, diagnose=False):
    """Validate an email address.

    Keyword arguments:
    address   --- the email address as a string
    check_dns --- flag for whether to check the DNS status of the domain
    diagnose  --- flag for whether to return True/False or a Diagnosis

    """

    d = ParserValidator().is_email(address, True)
    if check_dns is True and d < BaseDiagnosis.CATEGORIES["DNSWARN"]:
        d = max(d, DNSValidator().is_valid(address.split("@")[1], True))

    return d if diagnose else d < BaseDiagnosis.CATEGORIES["THRESHOLD"]