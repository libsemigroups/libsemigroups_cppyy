import unittest, libsemigroups_cppyy
from libsemigroups_cppyy import PartialPerm, LeftAction, RightAction


class TestPartialPerm(unittest.TestCase):
    def test_right(self):
        x = PartialPerm(range(16))
        o = RightAction(type(x), type(x))
        o.add_seed(x)
        o.add_generator(
            PartialPerm(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0],
                16,
            )
        )
        o.add_generator(
            PartialPerm(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                [1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                16,
            )
        )
        o.add_generator(
            PartialPerm(
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                16,
            )
        )
        o.add_generator(
            PartialPerm(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                16,
            )
        )
        self.assertEqual(o.size(), 65536)
        self.assertEqual(o.digraph().nr_scc(), 17)


    def test_left(self):
        x = PartialPerm(range(16))
        o = LeftAction(type(x), type(x))
        o.add_seed(x)
        o.add_generator(
            PartialPerm(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0],
                16,
            )
        )
        o.add_generator(
            PartialPerm(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                [1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                16,
            )
        )
        o.add_generator(
            PartialPerm(
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                16,
            )
        )
        o.add_generator(
            PartialPerm(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                16,
            )
        )
        self.assertEqual(o.size(), 65536)
        self.assertEqual(o.digraph().nr_scc(), 17)
