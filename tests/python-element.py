import cppyy
import libsemigroups_cppyy

cppyy.include("python3.6m/Python.h")
cppyy.include("./python_element.h")

from cppyy.gbl import PythonElement
from libsemigroups_cppyy import Semigroup

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

S = Semigroup([PythonElement(-1), PythonElement(0)])
assert S.size() == 3


# With Sage
G = IntegerModRing(2^32)
S = Semigroup([PythonElement(G(2))])
assert S.size() == 32L
