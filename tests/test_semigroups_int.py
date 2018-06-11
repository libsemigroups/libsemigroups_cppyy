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

assert len(list(cppyy.gbl.S)) == 32


cppyy.gbl.S
assert cppyy.gbl.S.size() == 32
assert cppyy.gbl.S.nridempotents() == 1

T = cppyy.gbl.libsemigroups.Semigroup("uint8_t")([2,3])
assert T.size() == 130
assert T.nridempotents() == 2
list(T) **bang**
