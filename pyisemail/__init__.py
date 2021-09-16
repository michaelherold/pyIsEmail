from pyisemail.diagnosis import BaseDiagnosis
from pyisemail.email_validator import EmailValidator
from pyisemail.reference import Reference
from pyisemail.validators import DNSValidator
from pyisemail.validators import GTLDValidator
from pyisemail.validators import ParserValidator
from pyisemail.version import VERSION

__version__ = VERSION
__all__ = ["is_email"]


def is_email(address, check_dns=False, diagnose=False, allow_gtld=True):
    """Validate an email address.

    Keyword arguments:
    address   --- the email address as a string
    check_dns --- flag for whether to check the DNS status of the domain
    diagnose  --- flag for whether to return True/False or a Diagnosis
    allow_gtld --- flag for whether to prevent gTLDs as the domain

    """

    threshold = BaseDiagnosis.CATEGORIES["THRESHOLD"]
    d = ParserValidator().is_email(address, True)

    if d < BaseDiagnosis.CATEGORIES["DNSWARN"]:
        domain = address.split("@")[1]

        if check_dns is True or allow_gtld is False:
            threshold = BaseDiagnosis.CATEGORIES["VALID"]
        if check_dns is True:
            d = max(d, DNSValidator().is_valid(domain, True))
        if allow_gtld is False:
            d = max(d, GTLDValidator().is_valid(domain, True))

    return d if diagnose else d < threshold
