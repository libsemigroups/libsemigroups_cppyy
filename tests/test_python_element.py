import unittest
from libsemigroups_cppyy import FroidurePin, PythonElement, ReportGuard


class TestPythonElement(unittest.TestCase):
    def test_basic(self):
        ReportGuard(False)
        s1 = PythonElement(1)
        s2 = PythonElement(2)
        s3 = PythonElement(3)
        self.assertEqual(s3.get_value(), 3)
        self.assertTrue(not s1 < s1)
        self.assertTrue(s1 < s2)

        s = s2 * s3
        self.assertEqual(s.get_value(), 6)  # Fails with Sage Integers

        S = FroidurePin([s1])
        self.assertEqual(S.size(), 1)

        S = FroidurePin([s1, s2, s3])
        S.enumerate(100)
        self.assertEqual(S.current_size(), 8195)
        self.assertEqual(S.current_nr_rules(), 6)


# import sys
# if 'sage' in sys.modules:
#     G = IntegerModRing(2^32)
#     S = Semigroup([PythonElement(G(2))])
#     assert S.size() == 32
# else:
#     print("skipping sage specific tests")
