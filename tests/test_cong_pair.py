import unittest, libsemigroups_cppyy
from libsemigroups_cppyy import (
    CongruenceByPairs,
    Transformation,
    FroidurePin,
    ReportGuard,
)


class TestCongruenceByPairs(unittest.TestCase):
    def test_congruence_by_pairs1(self):
        ReportGuard(False)
        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        C = CongruenceByPairs("left", S)
        C.add_pair([0], [1])
        self.assertEqual(C.nr_classes(), 1)
        self.assertEqual(S.size(), 4)
