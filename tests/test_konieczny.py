from libsemigroups_cppyy import compare_version_numbers, libsemigroups_version

if compare_version_numbers(libsemigroups_version(), "1.3.0"):
    import unittest
    from libsemigroups_cppyy import (
        Konieczny,
        Transformation,
        PartialPerm,
        ReportGuard,
    )
    import cppyy.gbl.std as std

    class TestKonieczny(unittest.TestCase):
        def test_init(self):
            ReportGuard(False)
            S = Konieczny(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
            self.assertEqual(S.size(), 4)
            self.assertEqual(S.number_of_generators(), 2)

            with self.assertRaises(KeyError):
                Konieczny()

            with self.assertRaises(ValueError):
                Konieczny(PartialPerm([1, 2], [0, 1], 3), Transformation([0, 1]))

            with self.assertRaises(TypeError):
                Konieczny({2, 3})
