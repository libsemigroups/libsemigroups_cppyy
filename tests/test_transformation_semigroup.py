from libsemigroups_cppyy import *
t = Transformation([1,0,2])
S = Semigroup([t]) # Segfaults
