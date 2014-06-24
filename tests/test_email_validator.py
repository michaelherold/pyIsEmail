import unittest
from pyisemail import EmailValidator


class EmailValidatorTest(unittest.TestCase):

    def test_abstract_is_email(self):
        v = EmailValidator()

        self.assertRaises(NotImplementedError, v.is_email, "test@example.com")
