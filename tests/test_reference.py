import unittest
from pyisemail import Reference


class ReferenceTest(unittest.TestCase):

    def test_repr(self):
        r = Reference('local-part')

        result = repr(r)
        expected = "%s (%r)" % (r.__class__, r.__dict__)

        self.assertEqual(result, expected)

    def test_str(self):
        r = Reference('local-part')

        result = str(r)
        expected = "%s <%s>" % (r.citation, r.link)

        self.assertEqual(result, expected)
