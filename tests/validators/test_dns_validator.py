import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
import dns.name
import dns.resolver
from pyisemail.diagnosis import DNSDiagnosis, RFC5321Diagnosis, ValidDiagnosis
from pyisemail.validators import DNSValidator


class DNSValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self.validator = DNSValidator()
        self.is_valid = self.validator.is_valid


@patch('dns.resolver.query')
class TestWorkingMXRecordTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('example.com'), True)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('example.com', diagnose=True),
            ValidDiagnosis())


@patch('dns.resolver.query', side_effect=dns.resolver.NXDOMAIN)
class TestNonExistantDomainTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('example.com'), False)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('example.com', diagnose=True),
            DNSDiagnosis('NO_RECORD'))


@patch('dns.resolver.query', side_effect=dns.name.NameTooLong)
class TestDomainTooLongTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('example.com'), False)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('example.com', diagnose=True),
            DNSDiagnosis('NO_RECORD'))


@patch('dns.resolver.query', side_effect=dns.resolver.NoAnswer)
class TestNoMxOrARecordsTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('example.com'), False)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('example.com', diagnose=True),
            DNSDiagnosis('NO_RECORD'))


@patch('dns.resolver.query', side_effect=[dns.resolver.NoAnswer, None])
class TestNoMxWithARecordTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('example.com'), False)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('example.com', diagnose=True),
            DNSDiagnosis('NO_MX_RECORD'))


@patch('dns.resolver.query', side_effect=dns.resolver.NXDOMAIN)
class TestNoMxOnTldTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('com'), False)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('com', diagnose=True),
            DNSDiagnosis('NO_RECORD'))


@patch('dns.resolver.query', side_effect=dns.resolver.NoAnswer)
class TestNoRecordsOnTldTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('com'), False)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('com', diagnose=True),
            RFC5321Diagnosis('TLD'))


@patch('dns.resolver.query', side_effect=dns.resolver.NoAnswer)
class TestNoRecordsOnNumericTldTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('iana.123'), False)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('iana.123', diagnose=True),
            RFC5321Diagnosis('TLDNUMERIC'))


@patch('dns.resolver.query', side_effect=dns.resolver.NoNameservers)
class NoNameserversRespondTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('example.com'), False)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('example.com', diagnose=True),
            DNSDiagnosis('NO_NAMESERVERS'))


@patch('dns.resolver.query', side_effect=dns.resolver.Timeout)
class DNSTimeoutTestCase(DNSValidatorTestCase):

    def testWithoutDiagnosis(self, mocked_method):
        self.assertEqual(self.is_valid('example.com'), False)

    def testWithDiagnosis(self, mocked_method):
        self.assertEqual(
            self.is_valid('example.com', diagnose=True),
            DNSDiagnosis('DNS_TIMEDOUT'))


if __name__ == '__main__':
    unittest.run()
