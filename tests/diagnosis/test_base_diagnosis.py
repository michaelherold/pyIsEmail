import unittest
from pyisemail.diagnosis import BaseDiagnosis


class BaseDiagnosisTest(unittest.TestCase):
    def test_lt(self):
        d1 = BaseDiagnosis("test")
        d1.code = 1
        d2 = BaseDiagnosis("test")
        d2.code = 2

        self.assertLess(d1, d2)
        self.assertLess(d1, 3)

    def test_gt(self):
        d1 = BaseDiagnosis("test")
        d1.code = 1
        d2 = BaseDiagnosis("test")
        d2.code = 2

        self.assertGreater(d2, d1)
        self.assertGreater(3, d1)

    def test_eq(self):
        d1 = BaseDiagnosis("test")
        d1.code = 1
        d2 = BaseDiagnosis("test")
        d2.code = 1

        self.assertEqual(d1, d2)

    def test_hash(self):
        d1 = BaseDiagnosis("test")
        d2 = BaseDiagnosis("test")

        self.assertEqual(hash(d1), hash(d2))
