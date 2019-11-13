import libsemigroups_cppyy
from libsemigroups_cppyy import Semigroup, PythonElement

sNone = PythonElement(None)
s1 = PythonElement(1)
s2 = PythonElement(2)
s3 = PythonElement(3)
assert s3.get_value() == 3
assert not s1 < s1
assert s1 < s2

s = s2 * s3
assert s.get_value() == 6 # Fails with Sage Integers

S = Semigroup([s1])
assert S.size() == 1

S = Semigroup([-1, 0])
assert S.size() == 3


import sys
if 'sage' in sys.modules:
    G = IntegerModRing(2^32)
    S = Semigroup([PythonElement(G(2))])
    assert S.size() == 32
else:
    print("skipping sage specific tests")
