# Minimal tests that transformation semigroups can be created.
# See test_semigrp for more elaborate tests

import unittest
from libsemigroups_cppyy import *

t = Transformation([1,0,2])
c = Transformation([1,2,0])
S = Semigroup([c,t])

class TestSemigroup(unittest.TestCase):
    def test_size(self):
        return self.assertEqual(S.size(), 6)

    def test_list(self):
        return self.assertEqual(len(S.list()), 6)
