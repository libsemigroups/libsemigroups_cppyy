# pylint: disable = C0103,E0611,C0111,W0104,R0201
import unittest
import sys
import os
from semigroups import (CayleyGraph, Semigroup, Transformation,
                        full_transformation_monoid)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if path not in sys.path:
    sys.path.insert(1, path)
del path

class TestCayleyGraph(unittest.TestCase):
    def test_init(self):
        self.assertEqual(CayleyGraph().__init__(), None)

        with self.assertRaises(TypeError):
            CayleyGraph(1)

    def test_eq(self):
        G = Semigroup(Transformation([0, 1, 1]),
                       Transformation([0, 0, 0])).right_cayley_graph()
        H = Semigroup(Transformation([0, 1, 1]),
                       Transformation([0, 0, 0])).right_cayley_graph()
        self.assertEqual(G, H)
        G = full_transformation_monoid(3).right_cayley_graph()
        H = full_transformation_monoid(3).right_cayley_graph()
        self.assertEqual(G, H)

    def test_ne(self):
        G = Semigroup(Transformation([0, 1, 1])).right_cayley_graph()
        H = Semigroup(Transformation([0, 1, 1]),
                       Transformation([0, 0, 0])).right_cayley_graph()
        self.assertNotEqual(G, H)
        G = full_transformation_monoid(3).right_cayley_graph()
        H = full_transformation_monoid(4).right_cayley_graph()
        self.assertNotEqual(G, H)

    def test_ordered_adjacencies(self):
        G = Semigroup(Transformation([0, 1, 1]),
                       Transformation([0, 0, 0])).right_cayley_graph()
        L = G.ordered_adjacencies()
        self.assertEqual(L, [[0, 1], [1, 1]])

        L = Semigroup(complex(0, 1)).right_cayley_graph().ordered_adjacencies()
        self.assertEqual(L, [[1], [2], [3], [0]])

        G = full_transformation_monoid(3).right_cayley_graph()
        L = G.ordered_adjacencies()
        M = [[3, 1, 4], [5, 1, 6], [7, 8, 9], [0, 1, 2], [9, 10, 7],
             [1, 1, 11], [12, 12, 13], [2, 8, 0], [14, 8, 15], [4, 10, 3],
             [16, 10, 17], [13, 18, 12], [6, 12, 5], [11, 18, 1], [8, 8, 19],
             [20, 20, 21], [10, 10, 22], [23, 23, 24], [25, 18, 26],
             [21, 18, 20], [15, 20, 14], [19, 18, 8], [24, 18, 23],
             [17, 23, 16], [22, 18, 10], [18, 18, 18], [26, 26, 25]]
        self.assertEqual(L, M)

        with self.assertRaises(TypeError):
            S = full_transformation_monoid(2)
            S.right_cayley_graph().ordered_adjacencies(1)

    def test_strongly_connected_components(self):
        G = Semigroup(Transformation([0, 1, 1]),
                       Transformation([0, 0, 0])).right_cayley_graph()
        L = G.strongly_connected_components()
        self.assertEqual(L, [{1}, {0}])

        G = Semigroup(complex(0, 1)).right_cayley_graph()
        L = G.strongly_connected_components()
        self.assertEqual(L, [{0, 1, 2, 3}])

        G = full_transformation_monoid(3).right_cayley_graph()
        L = G.strongly_connected_components()
        M = [{25, 18, 26}, {1, 5, 6, 11, 12, 13}, {8, 14, 15, 19, 20, 21},
             {10, 16, 17, 22, 23, 24}, {0, 2, 3, 4, 7, 9}]
        self.assertEqual(L, M)

        with self.assertRaises(TypeError):
            S = full_transformation_monoid(2)
            S.right_cayley_graph().strongly_connected_components(1)

    def test_edges(self):
        G = Semigroup(Transformation([0, 1, 1]),
                       Transformation([0, 0, 0])).right_cayley_graph()
        L = G.edges()
        self.assertEqual(L, [(0, 0), (0, 1), (1, 1), (1, 1)])

        L = Semigroup(complex(0, 1)).right_cayley_graph().edges()
        self.assertEqual(L, [(0, 1), (1, 2), (2, 3), (3, 0)])

        G = full_transformation_monoid(3).right_cayley_graph()
        L = G.edges()
        M = [(0, 3), (0, 1), (0, 4), (1, 5), (1, 1), (1, 6), (2, 7), (2, 8),
             (2, 9), (3, 0), (3, 1), (3, 2), (4, 9), (4, 10), (4, 7), (5, 1),
             (5, 1), (5, 11), (6, 12), (6, 12), (6, 13), (7, 2), (7, 8),
             (7, 0), (8, 14), (8, 8), (8, 15), (9, 4), (9, 10), (9, 3),
             (10, 16), (10, 10), (10, 17), (11, 13), (11, 18), (11, 12),
             (12, 6), (12, 12), (12, 5), (13, 11), (13, 18), (13, 1), (14, 8),
             (14, 8), (14, 19), (15, 20), (15, 20), (15, 21), (16, 10),
             (16, 10), (16, 22), (17, 23), (17, 23), (17, 24), (18, 25),
             (18, 18), (18, 26), (19, 21), (19, 18), (19, 20), (20, 15),
             (20, 20), (20, 14), (21, 19), (21, 18), (21, 8), (22, 24),
             (22, 18), (22, 23), (23, 17), (23, 23), (23, 16), (24, 22),
             (24, 18), (24, 10), (25, 18), (25, 18), (25, 18), (26, 26),
             (26, 26), (26, 25)]

        self.assertEqual(L, M)

        with self.assertRaises(TypeError):
            S = full_transformation_monoid(2)
            S.right_cayley_graph().edges(1)

    def test_nodes(self):
        G = Semigroup(Transformation([0, 1, 1]),
                       Transformation([0, 0, 0])).right_cayley_graph()
        L = G.nodes()
        self.assertEqual(L, [0, 1])

        L = Semigroup(complex(0, 1)).right_cayley_graph().nodes()
        self.assertEqual(L, [0, 1, 2, 3])

        G = full_transformation_monoid(3).right_cayley_graph()
        L = G.nodes()
        self.assertEqual(L, list(range(27)))

        with self.assertRaises(TypeError):
            S = full_transformation_monoid(2)
            S.right_cayley_graph().edges(1)

if __name__ == "__main__":
    unittest.main()
