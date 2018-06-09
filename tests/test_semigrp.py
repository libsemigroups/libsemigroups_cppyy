import unittest
import sys
import os
from semigroups import (Semigroup, Transformation, Bipartition,
                        full_transformation_monoid, CayleyGraph)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if path not in sys.path:
    sys.path.insert(1, path)
del path


class TestSemigroup(unittest.TestCase):
    def test_init(self):
        Semigroup(-1)
        Semigroup(Transformation([1, 0, 1]), Transformation([0, 0, 0]))

        with self.assertRaises(ValueError):
            Semigroup()

        with self.assertRaises(TypeError):
            Semigroup(Bipartition([1, -1], [2], [-2]), Transformation([0, 1]))

        with self.assertRaises(TypeError):
            Semigroup({2, 3})

    def test_right_cayley_graph(self):
        Semigroup(-1).right_cayley_graph()
        self.assertTrue(isinstance(Semigroup(-1).right_cayley_graph(),
                                   CayleyGraph))

    def test_left_cayley_graph(self):
        Semigroup(Transformation([0, 1])).right_cayley_graph()
        self.assertTrue(isinstance(Semigroup(-1).left_cayley_graph(),
                                   CayleyGraph))

class TestOtherFunctions(unittest.TestCase):
    def test_full_transformation_monoid(self):
        self.assertEqual(full_transformation_monoid(3)[7],
                         Semigroup(Transformation([1, 0, 2]),
                                   Transformation([0, 0, 2]),
                                   Transformation([2, 0, 1]))[7])
        self.assertEqual(full_transformation_monoid(2)[5],
                         Semigroup(Transformation([0, 0]),
                                   Transformation([0, 1]))[5])
        self.assertEqual(full_transformation_monoid(1)[0],
                         Semigroup(Transformation([0]))[0])

        with self.assertRaises(TypeError):
            full_transformation_monoid(2.5)

        with self.assertRaises(ValueError):
            full_transformation_monoid(-7)

if __name__ == "__main__":
    unittest.main()
