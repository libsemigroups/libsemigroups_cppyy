import unittest
import cppyy
import libsemigroups_cppyy
cppyy.cppdef("""
template <>
int libsemigroups::one(int) {
    return 1;
    }
template <>
uint8_t libsemigroups::one(uint8_t) {
    return 1;
    }
libsemigroups::Semigroup<int> S({2});
auto x = S.cbegin();
""")

S = cppyy.gbl.S
T = cppyy.gbl.libsemigroups.Semigroup("uint8_t")([2,3])

class TestSemigroupInt(unittest.TestCase):
    def test_size(self):
        self.assertEqual(S.size(), 32)
        self.assertEqual(T.size(), 130)

    def test_nridempotents(self):
        self.assertEqual(S.nridempotents(), 1)
        self.assertEqual(T.nridempotents(), 2)

    def test_list(self):
        # TODO: those test currently fail if the calculation of the semigroup
        # is not triggered explicitly
        # S.size()
        # T.size()
        self.assertEqual(len(list(S)), 32)
        self.assertEqual(len(list(T)), 130)

if __name__ == '__main__':
    unittest.main()
