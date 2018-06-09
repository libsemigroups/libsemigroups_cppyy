import unittest
import sys
import os
from libsemigroups_cppyy import Bipartition, Transformation, PartialPerm, BooleanMat, PBR

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path


class TestBipartition(unittest.TestCase):
    def test_init(self):
        Bipartition([-1, -2], [2, -3], [1, 3])
        Bipartition([-7, -6, -5, -4], [3, 2, 1], [-3, -2, -1, 4, 5, 6, 7])
        Bipartition([1, -1, 2, -2])

    def test_init_fail(self):
        with self.assertRaises(ValueError):
            Bipartition([1, -1, 2])
        with self.assertRaises(ValueError):
            Bipartition([1, 2, 3], [-3, -2])
        with self.assertRaises(TypeError):
            Bipartition([0, 1, 2], [-1, -2])
        with self.assertRaises(TypeError):
            Bipartition([1, 2, 3], (-1, -2, -3))
        with self.assertRaises(TypeError):
            Bipartition(1, 2, -1, -2)

    def test_richcmp(self):
        self.assertEqual(Bipartition([3, -4, -1], [2, -3], [4, -2], [1]),
                         Bipartition([4, -2], [3, -4, -1], [1], [2, -3]))
        self.assertFalse(Bipartition([3, -4, -1], [2, -3], [4, -2], [1]) !=
                         Bipartition([4, -2], [3, -4, -1], [1], [2, -3]))
        self.assertLessEqual(Bipartition([1, -1, 3], [-3, 2, -2]),
                             Bipartition([1, -1], [2, 3, -2], [-3]))
        self.assertLess(Bipartition([1, -1], [2, -2]),
                        Bipartition([1, -2], [2, -1]))
        self.assertLessEqual(Bipartition([1, -1], [2, -2]),
                             Bipartition([1, -2], [2, -1]))
        self.assertGreaterEqual(Bipartition([1, -1, 3], [-3, 2, -2]),
                                Bipartition([1, -2], [2, -1]))
        self.assertFalse(Bipartition([1, -1, 3], [-3, 2, -2]) > 
                         Bipartition([1, -1], [2, 3, -2], [-3]))

        with self.assertRaises(TypeError):
            (PartialPerm([1, 2], [2, 1], 3) ==
            Bipartition([1, -1], [2, 3, -2], [-3]))
        with self.assertRaises(TypeError):
            Bipartition([1, -1], [2, -2]) < Transformation([0, 1])
        with self.assertRaises(TypeError):
            Bipartition([1, -1], [2, -2]) != Transformation([0, 1])

    def test_mul(self):
        (self.assertEqual(Bipartition([1, -1, 2, -2]) *
                         Bipartition([1, -1, 2, -2]),
                         Bipartition([1, 2, -1, -2])))
        (self.assertEqual(Bipartition([1, 2], [-1], [-2]) *
                         Bipartition([1, -1], [2, -2]),
                         Bipartition([1, 2], [-1], [-2])))
        (self.assertEqual(Bipartition([1, -1], [2, 3, -2], [-3]) *
                         Bipartition([1, 3, 2, -3], [-2], [-1]),
                         Bipartition([1, 2, 3, -3], [-1], [-2])))

        with self.assertRaises(TypeError):
            (Bipartition([1, -1], [2, 3, -3], [-2]) *
            PartialPerm([0, 1], [1, 2], 3))
        with self.assertRaises(TypeError):
            Transformation([0, 2, 1]) * Bipartition([1, -1], [2, 3, -3], [-2])
        with self.assertRaises(TypeError):
            Bipartition([1, -1], [2, 3, -3], [-2]) * 26

        with self.assertRaises(ValueError):
            (Bipartition([1, -1], [2, 3, -3], [-2]) *
            Bipartition([1, -1, 2, -2]))

    def test_pow(self):
        self.assertEqual(Bipartition([-7, -6, -5, -4], [3, 2, 1],
                                     [-3, -2, -1, 4, 5, 6, 7]) ** 20,
                         Bipartition([1, 2, 3], [4, 5, 6, 7], [-1, -2, -3],
                                     [-4, -5, -6, -7]))
        self.assertEqual(Bipartition([1, -1, 2, -2]) ** 26,
                         Bipartition([1, 2, -1, -2]))
        self.assertEqual(Bipartition([-1, -2], [2, -3], [1, 3]) ** 3,
                         Bipartition([1, 3], [2, -3], [-1, -2]))

        with self.assertRaises(ValueError):
            Bipartition([1, -1, 2, -2]) ** -26

        self.assertEqual(Bipartition([1], [-1, 2, -2]) ** 0,
                         Bipartition([1], [-1, 2, -2]).identity())

        with self.assertRaises(TypeError):
            Bipartition([1, 2], [-1], [-2]) ** 3.141592653589793238462643383279
        with self.assertRaises(TypeError):
            Bipartition([1, 2], [-1], [-2]) ** 'c'

    def test_dealloc(self):
        A = Bipartition([1, -1, 2, -2])
        B = Bipartition([-7, -6, -5, -4], [3, 2, 1], [-3, -2, -1, 4, 5, 6, 7])
        del A, B
        with self.assertRaises(NameError):
            A
        with self.assertRaises(NameError):
            B

    def test_blocks1(self):
        self.assertEqual(Bipartition([1, 2], [-2, -1]).blocks(),
                         [[1, 2], [-1, -2]])
        self.assertEqual(Bipartition([-7, -6, -5, -4], [3, 2, 1],
                                     [-3, -2, -1, 4, 5, 6, 7]).blocks(),
                         [[1, 2, 3], [4, 5, 6, 7, -1, -2, -3],
                          [-4, -5, -6, -7]])
        self.assertEqual(Bipartition([-1, -2], [2, -3], [1, 3]).blocks(),
                         [[1, 3], [2, -3], [-1, -2]])

        x = Bipartition([-1, -2], [2, -3], [1, 3])
        self.assertEqual((x * x).blocks(), [[1, 3], [2, -3], [-1, -2]])

    def test_blocks2(self):
        x = Bipartition([1, 2], [-2, -1, 3], [-3])
        self.assertEqual(x.blocks(), [[1, 2], [3, -1, -2], [-3]])
        self.assertEqual((x * x.identity()).blocks(),
                         [[1, 2], [3, -1, -2], [-3]])

    def test_nr_blocks(self):
        self.assertEqual(Bipartition([1, 2], [-2, -1]).nr_blocks(), 2)
        self.assertEqual(Bipartition([-7, -6, -5, -4], [3, 2, 1], [-3, -2,
                                      -1, 4, 5, 6, 7]).nr_blocks(), 3)
        self.assertEqual(Bipartition([-1, -2], [2, -3],
                                     [1, 3]).nr_blocks(), 3)

    def test_degree(self):
        self.assertEqual(Bipartition([1, 2], [-2, -1]).degree(), 2)
        self.assertEqual(Bipartition([-7, -6, -5, -4], [3, 2, 1],
                                     [-3, -2, -1, 4, 5, 6, 7]).degree(), 7)
        self.assertEqual(Bipartition([-1, -2], [2, -3], [1, 3]).degree(), 3)

    def test_block(self):
        self.assertEqual(Bipartition([1, 2], [-2, -1]).block(-2), 1)
        self.assertEqual(Bipartition([-7, -6, -5, -4], [3, 2, 1],
                                     [-3, -2, -1, 4, 5, 6, 7]).block(3), 0)
        self.assertEqual(Bipartition([-1, -2], [2, -3], [1, 3]).block(-1), 2)

        with self.assertRaises(IndexError):
            Bipartition([1, 2], [-2, -1]).block(-3)
        with self.assertRaises(IndexError):
            Bipartition([-7, -6, -5, -4], [3, 2, 1],
                        [-3, -2, -1, 4, 5, 6, 7]).block(26)
        with self.assertRaises(TypeError):
            Bipartition([-1, -2], [2, -3], [1, 3]).block('a')

    def test_is_transverse_block(self):
        self.assertEqual(Bipartition([1, 2],
                                     [-2, -1]).is_transverse_block(1), False)
        self.assertEqual(Bipartition([-7, -6, -5, -4], [3, 2, 1], [-3, -2, -1,
                                      4, 5, 6, 7]).is_transverse_block(1), True)
        self.assertEqual(Bipartition([-1, -2], [2, -3],
                                     [1, 3]).is_transverse_block(1), True)

        with self.assertRaises(IndexError):
            Bipartition([1, 2], [-2, -1]).is_transverse_block(-3)
        with self.assertRaises(IndexError):
            Bipartition([-7, -6, -5, -4], [3, 2, 1],
                        [-3, -2, -1, 4, 5, 6, 7]).is_transverse_block(26)

        with self.assertRaises(TypeError):
            Bipartition([-1, -2], [2, -3], [1, 3]).is_transverse_block('a')
        with self.assertRaises(TypeError):
            Bipartition([-1, -2], [2, -3], [1, 3]).is_transverse_block([7, 26])

    def test_identity(self):
        self.assertEqual(Bipartition([1, 2], [-2, -1]).identity(),
                         Bipartition([1, -1], [2, -2]))
        self.assertEqual(Bipartition([-7, -6, -5, -4], [3, 2, 1],
                                     [-3, -2, -1, 4, 5, 6, 7]).identity(),
                         Bipartition([1, -1], [2, -2], [3, -3], [4, -4],
                                     [5, -5], [6, -6], [7, -7]))
        self.assertEqual(Bipartition([-1, -2], [2, -3], [1, 3]).identity(),
                         Bipartition([1, -1], [2, -2], [3, -3]))

    def test_repr(self):
        self.assertEqual(eval(Bipartition([1, 2], [-2, -1]).__repr__()),
                         Bipartition([1, 2], [-2, -1]))
        self.assertEqual(eval(Bipartition([-1, -2], [2, -3],
                                          [1, 3]).__repr__()),
                         Bipartition([-1, -2], [2, -3], [1, 3]))
        self.assertEqual(eval(Bipartition([-7, -6, -5, -4], [3, 2, 1],
                                     [-3, -2, -1, 4, 5, 6, 7]).__repr__()),
                         Bipartition([-7, -6, -5, -4], [3, 2, 1],
                                     [-3, -2, -1, 4, 5, 6, 7]))

    def test_generator(self):
        self.assertEqual(list(Bipartition([1, 2], [-2, -1])),
                         [0, 0, 1, 1])
        self.assertEqual(list(Bipartition([-1, -2], [2, -3], [1, 3])),
                         [0, 1, 0, 2, 2, 1])
        self.assertEqual(list(Bipartition([-7, -6, -5, -4], [3, 2, 1],
                                          [-3, -2, -1, 4, 5, 6, 7])),
                         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2])

class TestBooleanMat(unittest.TestCase):
    def test_init(self):
        BooleanMat([[True, True], [False, False]])
        BooleanMat([[False, True, True], [True, True, False],
                    [False, False, False]])
        BooleanMat([[True]])
        BooleanMat([[True, False], [False, True]])
        BooleanMat([[1, 0], [0, 0]])

    def test_init_fail(self):
        with self.assertRaises(TypeError):
            BooleanMat(True)
        with self.assertRaises(TypeError):
            BooleanMat(set([True, False]), set([False, True]))
        with self.assertRaises(TypeError):
            BooleanMat(26)
        with self.assertRaises(TypeError):
            BooleanMat([[1., 0.], [0., 1.]])
        with self.assertRaises(TypeError):
            BooleanMat([[True, False], ["i", range(10)]])

        with self.assertRaises(ValueError):
            BooleanMat([[True], [False]])
        with self.assertRaises(ValueError):
            BooleanMat([[True, False], [False, False], [True, True]])
        with self.assertRaises(ValueError):
            BooleanMat([[True, True, False], [False, False]])
        with self.assertRaises(ValueError):
            BooleanMat()

    def test_richcmp(self):
        self.assertEqual(BooleanMat([[True, False], [False, True]]),
                         BooleanMat([[True, False], [False, True]]))
        self.assertFalse(BooleanMat([[True, False], [False, True]]) !=
                         BooleanMat([[True, False], [False, True]]))
        self.assertFalse(BooleanMat([[True, False], [False, True]]) ==
                         BooleanMat([[False, False], [False, True]]))
        self.assertLess(BooleanMat([[False]]), BooleanMat([[True]]))
        self.assertFalse(BooleanMat([[False, True, True],
                                     [True, True, False],
                                     [False, False, False]]) <
                         BooleanMat([[False, True, False],
                                     [True, False, False],
                                     [False, False, True]]))
        self.assertLessEqual(BooleanMat([[False]]), BooleanMat([[False]]))
        self.assertGreater(BooleanMat([[True, False], [False, True]]),
                           BooleanMat([[True, False], [False, False]]))
        self.assertFalse(BooleanMat([[True, False], [False, True]]) >
                         BooleanMat([[True, False], [False, True]]))
        self.assertGreaterEqual(BooleanMat([[False]]), BooleanMat([[False]]))

        with self.assertRaises(TypeError):
            (Bipartition([1, -2], [-1, 2]) >=
            BooleanMat([False, False], [True, False]))
        with self.assertRaises(TypeError):
            BooleanMat([False, False], [True, False]) < Transformation([0, 1])
        with self.assertRaises(TypeError):
            (BooleanMat([True, False], [False, True]) ==
            PartialPerm([0], [1], 2))

    def test_getitem(self):
        self.assertEqual(BooleanMat([[1, 0], [0, 0]])[0], [1, 0])
        self.assertEqual(BooleanMat([[1, 0], [0, 0]])[1], [0, 0])

        with self.assertRaises(IndexError):
            BooleanMat([[1, 0, 1], [1, 0, 0], [0, 1, 1]])[3]

    def test_mul(self):
        (self.assertEqual(BooleanMat([[True, False], [False, True]]) *
                          BooleanMat([[False, False], [False, True]]),
                          BooleanMat([[False, False], [False, True]])))
        self.assertEqual(BooleanMat([[False]]) * BooleanMat([[True]]),
                         BooleanMat([[False]]))
        (self.assertEqual(BooleanMat([[False, True, True],
                                      [True, True, False],
                                      [False, False, False]]) *
                          BooleanMat([[False, True, False],
                                      [True, False, False],
                                      [False, False, True]]),
                          BooleanMat([[True, False, True],
                                      [True, True, False],
                                      [False, False, False]])))

        with self.assertRaises(TypeError):
            BooleanMat([[True, True], [False, False]]) * Transformation([1, 1])
        with self.assertRaises(TypeError):
            BooleanMat([[False, True, True],
                        [True, True, False],
                        [False, False, False]]) * PartialPerm([0, 1], [1, 2], 3)
        with self.assertRaises(TypeError):
            BooleanMat([[True]]) * [[True]]
        with self.assertRaises(TypeError):
            BooleanMat([[True, False], [False, True]]) * Bipartition([1, 2], [-1], [-2])

        with self.assertRaises(ValueError):
            (BooleanMat([[False, True, True],
                         [True, True, False],
                         [False, False, False]]) * 
            BooleanMat([[True, False], [False, True]]))

    def test_pow(self):
        self.assertEqual(BooleanMat([[True, False], [False, True]]) ** 30,
                         BooleanMat([[True, False], [False, True]]))
        self.assertEqual(BooleanMat([[True, False], [True, True]]) ** 7,
                         BooleanMat([[True, False], [True, True]]))
        self.assertEqual(BooleanMat([[True]]) ** 26, BooleanMat([True]))

        with self.assertRaises(TypeError):
            BooleanMat([[True, False], [True, True]]) ** 'i'
        with self.assertRaises(TypeError):
            BooleanMat([[True]]) ** range(10)
        with self.assertRaises(TypeError):
            BooleanMat([[True]]) ** BooleanMat([[True]])

        self.assertEqual(BooleanMat([[True, False], [True, True]]) ** 0,
                         BooleanMat([[1, 0], [0, 1]]))
        with self.assertRaises(ValueError):
            BooleanMat([[False, True, True],
                        [True, True, False],
                        [False, False, False]]) ** -7

    def test_dealloc(self):
        A = BooleanMat([[True, False], [True, True]])
        B = BooleanMat([[False, False], [False, True]])
        del A, B
        assert 'A' not in globals()
        assert 'B' not in globals()

    def test_degree(self):
        self.assertEqual(BooleanMat([[True, True], [False, False]]).degree(), 2)
        self.assertEqual(BooleanMat([[False, True, True],
                                     [True, True, False],
                                     [False, False, False]]).degree(), 3)
        self.assertEqual(BooleanMat([True]).degree(), 1)

    def test_identity(self):
        self.assertEqual(BooleanMat([[True, True], [False, False]]).identity(),
                         BooleanMat([[True, False], [False, True]]))
        self.assertEqual(BooleanMat([[False, True, True],
                                     [True, True, False],
                                     [False, False, False]]).identity(),
                         BooleanMat([[True, False, False],
                                     [False, True, False],
                                     [False, False, True]]))
        self.assertEqual(BooleanMat([False]).identity(), BooleanMat([True]))

    def test_rows(self):
        self.assertEqual(BooleanMat([[True, True], [False, False]]).rows(),
                         [[True, True], [False, False]])
        self.assertEqual(BooleanMat([[False, True, True],
                                     [True, True, False],
                                     [False, False, False]]).rows(),
                         [[False, True, True],
                          [True, True, False],
                          [False, False, False]])
        self.assertEqual(BooleanMat([[False]]).rows(), [[False]])
        self.assertEqual(BooleanMat([[0, 0], [0, 0]]).identity().rows(), [[1, 0], [0, 1]])

    def test_repr(self):
        self.assertEqual(eval(BooleanMat([[True, True], [False, False]]).__repr__()),
                         BooleanMat([[True, True], [False, False]]))
        self.assertEqual(eval(BooleanMat([[False, True, True],
                                    [True, True, False],
                                    [False, False, False]]).__repr__()),
                         BooleanMat([[False, True, True],
                                     [True, True, False],
                                     [False, False, False]]))
        self.assertEqual(eval(BooleanMat([[True, False, False],
                                    [False, True, False],
                                    [False, False, True]]).__repr__()),
                         BooleanMat([[True, False, False],
                                     [False, True, False],
                                     [False, False, True]]))

class TestPartialPerm(unittest.TestCase):
    def test_init(self):
        PartialPerm([1, 0, 2], [2, 0, 1], 3)
        PartialPerm([1, 0], [0, 1], 5)
        PartialPerm([0, 3, 4, 5, 8, 20, 23373],
                    [1, 2, 34, 23423, 233, 432, 26], 26260)

    def test_init_fail(self):
        with self.assertRaises(TypeError):
            PartialPerm([1, 3], [0, 1], 3)
        with self.assertRaises(TypeError):
            PartialPerm([1, 2], [3, 2], 3)
        with self.assertRaises(TypeError):
            PartialPerm([-2, 2], [0, 1], 3)
        with self.assertRaises(TypeError):
            PartialPerm([1, 2], [-1, 2], 3)
        with self.assertRaises(TypeError):
            PartialPerm([1, 2], [2, 2], 3)
        with self.assertRaises(TypeError):
            PartialPerm([1, 1], [0, 2], 3)
        with self.assertRaises(TypeError):
            PartialPerm([], [], -1)
        with self.assertRaises(TypeError):
            PartialPerm([1, 2], [0, 1, 2], 3)

        with self.assertRaises(TypeError):
            PartialPerm([1, 2], [0, 'i'], 3)
        with self.assertRaises(TypeError):
            PartialPerm([1, [0]], [1, 2], 3)
        with self.assertRaises(TypeError):
            PartialPerm([0, 1], [2, 3], [4])
        with self.assertRaises(TypeError):
            PartialPerm([0, 1], [2, 3], 4.3)

    def test_richcmp(self):
        self.assertEqual(PartialPerm([1, 2, 3], [2, 1, 0], 5),
                         PartialPerm([1, 2, 3], [2, 1, 0], 5))
        self.assertFalse(PartialPerm([1, 2, 3], [2, 1, 0], 5) != 
                         PartialPerm([1, 2, 3], [2, 1, 0], 5))
        self.assertFalse(PartialPerm([1, 2, 4], [2, 1, 0], 5) == 
                          PartialPerm([1, 2, 3], [2, 3, 0], 5))
        self.assertNotEqual(PartialPerm([1, 2, 4], [2, 1, 0], 5),
                            PartialPerm([1, 2, 3], [2, 3, 0], 5))
        self.assertFalse(PartialPerm([1, 2, 4], [2, 1, 0], 5) < 
                          PartialPerm([1, 2, 3], [2, 3, 0], 5))
        self.assertLess(PartialPerm([1, 2], [0, 1], 3),
                        PartialPerm([2, 0], [0, 1], 3))
        self.assertFalse(PartialPerm([1, 2], [0, 1], 3) > 
                         PartialPerm([2, 0], [0, 1], 3))
        self.assertGreater(PartialPerm([1, 2], [1, 2], 3),
                           PartialPerm([1, 2], [0, 1], 3))
        self.assertGreaterEqual(PartialPerm([1, 2], [1, 2], 3),
                                PartialPerm([1, 2], [0, 1], 3))
        self.assertLessEqual(PartialPerm([1, 2, 3], [2, 1, 0], 5),
                             PartialPerm([1, 2, 3], [2, 1, 0], 5))

        with self.assertRaises(TypeError):
            (PartialPerm([1, 2], [2, 1], 3) ==
            Bipartition([1, -1], [2, 3, -2], [-3]))
        with self.assertRaises(TypeError):
            PartialPerm([0, 1], [0, 1], 2) < Transformation([0, 1])
        with self.assertRaises(TypeError):
            PartialPerm([0, 1], [0, 1], 2) != Transformation([0, 1])

    def test_mul(self):
        (self.assertEqual(PartialPerm([0, 1], [0, 1], 2) *
                         PartialPerm([0, 1], [0, 1], 2),
                         PartialPerm([0, 1], [0, 1], 2)))
        (self.assertEqual(PartialPerm([1, 2, 4, 6, 7, 23],
                                     [0, 5, 2, 4, 6, 7], 26) *
                         PartialPerm([2, 4, 3, 5, 0, 19],
                                     [7, 8, 2, 3, 23, 0], 26),
                         PartialPerm([1, 2, 4, 6], [23, 3, 7, 8], 26)))
        (self.assertEqual(PartialPerm([0, 3, 7, 2], [5, 7, 1, 3], 8) *
                         PartialPerm([4, 7, 3, 6], [5, 0, 3, 2], 8),
                         PartialPerm([2, 3], [3, 0], 8)))

        with self.assertRaises(TypeError):
            PartialPerm([0, 1], [0, 1], 2) * Transformation([0, 1])
        with self.assertRaises(TypeError):
            PartialPerm([0, 1], [0, 1], 2) * Bipartition([-2, 1], [-1, 2])

        with self.assertRaises(ValueError):
            PartialPerm([1, 2], [0, 1], 3) * PartialPerm([1, 2], [0, 1], 4)

    def test_pow(self):
        self.assertEqual(PartialPerm([0, 1], [0, 1], 2) ** 20,
                         PartialPerm([0, 1], [0, 1], 2))
        self.assertEqual(PartialPerm([1, 2, 4, 6, 7, 23],
                                     [0, 5, 2, 4, 6, 7], 26) ** 5,
                         PartialPerm([23], [5], 26))
        self.assertEqual(PartialPerm([0, 3, 7, 2], [5, 7, 1, 3], 8) ** 10,
                         PartialPerm([], [], 8))
        self.assertEqual(PartialPerm([1, 2, 4, 6, 7, 23],
                                     [0, 5, 2, 4, 6, 7],
                                     26) ** 0,
                         PartialPerm([], [], 26).identity())

        with self.assertRaises(ValueError):
            PartialPerm([1, 2], [0, 1], 3) ** -1
        with self.assertRaises(TypeError):
            PartialPerm([0, 1], [0, 1], 2) ** 1.5
        with self.assertRaises(TypeError):
            PartialPerm([1, 4, 2], [2, 3, 4], 6) ** 'a'

    def test_rank(self):
        self.assertEqual(PartialPerm([1, 4, 2], [2, 3, 4], 6).rank(), 3)
        self.assertEqual(PartialPerm([1, 2, 4, 6, 7, 23],
                                     [0, 5, 2, 4, 6, 7], 26).rank(), 6)

        with self.assertRaises(TypeError):
            PartialPerm([1, 2], [0, 1], 3).rank(2)

    def test_domain(self):
        self.assertEqual(set(PartialPerm([1, 4, 2], [2, 3, 4], 6).domain()),
                         set([1, 4, 2]))
        self.assertEqual(set(PartialPerm([7, 26, 3, 5],
                                         [23, 13, 19, 11], 29).domain()),
                         set([7, 26, 3, 5]))

        with self.assertRaises(TypeError):
            PartialPerm([1, 2], [0, 1], 3).domain('a')

    def test_range(self):
        self.assertEqual(set(PartialPerm([1, 4, 2], [2, 3, 4], 6).range()),
                         set([2, 3, 4]))
        self.assertEqual(set(PartialPerm([7, 26, 3, 5],
                                         [23, 13, 19, 11], 29).range()),
                         set([23, 13, 19, 11]))

        with self.assertRaises(TypeError):
            PartialPerm([1, 2], [0, 1], 3).range([3])

    def test_degree(self):
        self.assertEqual(PartialPerm([1, 4, 2], [2, 3, 4], 6).degree(), 6)
        self.assertEqual(PartialPerm([7, 26, 3, 5],
                                     [23, 13, 19, 11], 29).degree(), 29)

        with self.assertRaises(TypeError):
            PartialPerm([1, 2], [0, 1], 3).degree(8.5)

    def test_dealloc(self):
        t = PartialPerm([0, 1], [1, 0], 2)
        del t
        with self.assertRaises(NameError):
            t

    def test_identity(self):
        self.assertEqual(PartialPerm([0, 1], [1, 0], 2).identity(),
                         PartialPerm([0, 1], [0, 1], 2))
        self.assertEqual(PartialPerm([1, 2, 4, 6, 7, 3],
                                     [0, 5, 2, 4, 6, 7], 8).identity(),
                         PartialPerm([0, 1, 2, 3, 4, 5, 6, 7],
                                     [0, 1, 2, 3, 4, 5, 6, 7], 8))
        self.assertEqual(PartialPerm([0, 3, 4, 2], [2, 4, 1, 3], 5).identity(),
                         PartialPerm([0, 1, 2, 3, 4], [0, 1, 2, 3, 4], 5))

    def test_repr(self):
        self.assertEqual(eval(PartialPerm([0, 3, 4, 2],
                                          [2, 4, 1, 3], 5).__repr__()),
                         PartialPerm([0, 3, 4, 2], [2, 4, 1, 3], 5))
        self.assertEqual(eval(PartialPerm([1, 4, 2], [2, 3, 4], 6).__repr__()),
                         PartialPerm([1, 4, 2], [2, 3, 4], 6))
        self.assertEqual(eval(PartialPerm([1, 2, 3], [2, 1, 0], 5).__repr__()),
                         PartialPerm([1, 2, 3], [2, 1, 0], 5))

    def test_init_dom_ran(self):
        X = PartialPerm([0, 1, 3], [0, 2, 4], 5) ** 2
        X._init_dom_ran()
        self.assertTrue(X._range is not None)
        self.assertTrue(X._domain is not None)

class TestPBR(unittest.TestCase):
    def test_init(self):
        PBR([[1, -1]], [[1]])
        PBR([[1, -1], [-2, -1]], [[1], [-2, -1]])
        PBR([[1, -1], [-2, -1, 2]], [[2], [-2]])
        PBR([[1, -1, 3], [-2, -1, 2], [3, -2]], [[2], [-2], [1, -1, 2]])
        PBR([[1, 2], [-2, 1, 2], [3, -3]], [[2, 1], [-2, 2, 1], [1, -1]])
        PBR([[1, 2], [-2, 1, 2], [3, -3]], [[2, 1], [-2, 2, 1], [1, -1]])
        PBR([[[1, 2], [-2, 1, 2], [3, -3]], [[2, 1], [-2, 2, 1], [1, -1]]])

    def test_init_fail(self):
        with self.assertRaises(ValueError):
            PBR([[1, -1]], [[1]], [[1]])
        with self.assertRaises(TypeError):
            PBR(set([(1, -1)]), set([(1)]))
        with self.assertRaises(TypeError):
            PBR('a', 2)

        with self.assertRaises(ValueError):
            PBR([[1, -1], [2, -1]], [[1]])
        with self.assertRaises(ValueError):
            PBR([[1, -1], [-2, -1]], [[0], [-2, -1]])
        with self.assertRaises(ValueError):
            PBR([[1, -1], [-2, -1, 2]], [[3], [-2]])
        with self.assertRaises(ValueError):
            PBR([[1, -1, 3], [-2, -1, 2], [3, 3, -2]], [[2], [-2], [1, -1, 2]])

    def test_richcmp(self):
        self.assertEqual(PBR([[1, -1], [-2, -1, 2]], [[2], [-2]]),
                          PBR([[1, -1], [-2, -1, 2]], [[2], [-2]]))
        self.assertEqual(PBR([[1, -1], [-2, -1, 2]], [[2], [-2]]),
                          PBR([[1, -1], [-2, -1, 2]], [[2], [-2]]))
        self.assertNotEqual(PBR([[1, -1], [-2, -1, 2]], [[2], [-2]]),
                             PBR([[1, 2], [-2, 1, 2], [3, -3]],
                                 [[2, 1], [-2, 2, 1], [1, -1]]))
        self.assertTrue(PBR([[1], [1, 2, -1]], [[1], [2, -1, 1]]) <
                        PBR([[1], [2]], [[-1], [-2]]))
        self.assertTrue(PBR([[1, -1, 3], [-2, -1, 2], [3, -2]],
                            [[2], [-2], [1, -1, 2]])
                        > PBR([[1, -1], [-2, -1, 2]], [[2], [-2]]))
        self.assertTrue(PBR([[1, -1, 3], [-2, -1, 2], [3, -2]],
                            [[2], [-2], [1, -1, 2]])
                        >= PBR([[1, -1], [-2, -1, 2]], [[2], [-2]]))
        self.assertTrue(PBR([[1, -1], [-2, -1, 2]], [[2], [-2]])
                        <= PBR([[1, -1], [-2, -1, 2]], [[2], [-2]]))

        with self.assertRaises(TypeError):
            (PBR([[1, -1, 3], [-2, -1, 2], [3, -2]],
                 [[2], [-2], [1, -1, 2]]) ==
             Bipartition([1, -1], [2, 3, -2], [-3]))
        with self.assertRaises(TypeError):
            PBR([[1, -1], [-2, -1]], [[1], [-2, -1]]) < Transformation([0, 1])
        with self.assertRaises(TypeError):
            (PBR([[1, -1], [-2, -1]], [[1], [-2, -1]]) !=
            PartialPerm([0, 1], [1, 0], 2))
        with self.assertRaises(TypeError):
            PBR([[1, -1]], [[1]]) < 3

    def test_mul(self):
        self.assertEqual(PBR([[1, -1]], [[1]]) * PBR([[1, -1]], [[1]]),
                         PBR([[1, -1]], [[1]]))
        self.assertEqual(PBR([[1, -1], [-2, -1]], [[1], [-2, -1]])
                         * PBR([[-1, 1, 2], [2]], [[-1, 1], [-2, 2]]),
                         PBR([[1, -1], [1, -1]], [[1, -1], [1, -1, -2]]))
        self.assertEqual(PBR([[-1, 1, 2], [2]], [[-1, 1], [-2, 2]])
                         * PBR([[1, -1], [-2, -1]], [[1], [-2, -1]]),
                         PBR([[-1, 1, 2], [2]], [[-1, 1], [-2, -1]]))
        self.assertEqual(PBR([[1, -1, 3], [-2, -1, 2], [3, -2]],
                             [[2], [-2], [1, -1, 2]]) *
                         PBR([[1, -1, 3], [-2, -1, 2], [3, -3, -2]],
                             [[1, 2], [-2, 3, -3], [1, -1]]),
                         PBR([[-1, 1, 2, 3], [-2, -1, 1, 2], [-2, -1, 3]],
                             [[-2, -1, 2], [-3, -2, -1, 1, 2], [-1, 2]]))

        with self.assertRaises(TypeError):
            (Transformation([0, 2, 1]) *
            PBR([[1, -1, 3], [-2, -1, 2], [3, -2]], [[2], [-2], [1, -1, 2]]))
        with self.assertRaises(TypeError):
            (PBR([[1, -1, 3], [-2, -1, 2], [3, -2]],
                [[2], [-2], [1, -1, 2]]) *
            Bipartition([1, -1], [2, 3, -3], [-2]))
        with self.assertRaises(TypeError):
            PBR([[1, -1]], [[1]]) * 0.142857

        with self.assertRaises(ValueError):
            PBR([[1, -1, 3], [-2, -1, 2], [3, -2]],
                [[2], [-2], [1, -1, 2]]) * PBR([[1, -1]], [[1]])

    def test_pow(self):
        self.assertEqual(PBR([[1, -1, 3], [-2, -1, 2], [3, -2]],
                             [[2], [-2], [1, -1, 2]]) ** 5,
                         PBR([[-2, -1, 1, 2, 3], [-2, -1, 1, 2],
                              [-2, -1, 2, 3]],
                             [[-2, -1], [-2], [-2, -1, 2]]))
        self.assertEqual(PBR([[1, -1]], [[1]]) ** 26, PBR([[1, -1]], [[1]]))
        self.assertEqual(PBR([[-1, 1, 2], [2]], [[-1, 1], [-2, 2]]) ** 4,
                         PBR([[1, 2, -1], [2]], [[1, 2, -1], [2, -2]]))

        with self.assertRaises(ValueError):
            PBR([[1, -1, 3], [-2, -1, 2], [3, -2]],
                [[2], [-2], [1, -1, 2]]) ** -26
        self.assertEqual(PBR([[1, 2, 3, -1, -2, -3],
                               [1, 2, 3, -1, -2, -3], [3, -2, -3]],
                              [[2], [3, -2, -3], [1, 2, 3, -2, -3]]) ** 0,
                          PBR([[1, 2, 3, -1, -2, -3],
                               [1, 2, 3, -1, -2, -3], [3, -2, -3]],
                              [[2], [3, -2, -3],
                               [1, 2, 3, -2, -3]]).identity())

        with self.assertRaises(TypeError):
            PBR([[1, -1]], [[1]]) ** 0.21813
        with self.assertRaises(TypeError):
            PBR([[1, -1]], [[1]]) ** 'a'

    def test_dealloc(self):
        A = PBR([[1, -1]], [[1]]),
        B = PBR([[1, -1, 3], [-2, -1, 2], [3, -2]], [[2], [-2], [1, -1, 2]])
        del A, B
        assert not 'A' in globals()
        assert not 'B' in globals()

    def test_degree(self):
        self.assertEqual(PBR([[1, -1]], [[1]]).degree(), 1)
        self.assertEqual(PBR([[1, 2, 3, -1, -2, -3],
                              [1, 2, 3, -1, -2, -3], [3, -2, -3]],
                              [[2], [3, -2, -3], [1, 2, 3, -2, -3]]).degree(), 3)
        self.assertEqual(PBR([[1, -1], [-2, -1, 2]], [[2], [-2]]).degree(), 2)

    def test_identity(self):
        self.assertEqual(PBR([[-1, 1, 2], [2]], [[-1, 1], [-2, 2]]).identity(),
                         PBR([[-1], [-2]], [[1], [2]]))

        self.assertEqual(PBR([[1, 2, 3, -1, -2, -3],
                              [1, 2, 3, -1, -2, -3], [3, -2, -3]],
                             [[2], [3, -2, -3], [1, 2, 3, -2, -3]]).identity(),
                         PBR([[-1], [-2], [-3]], [[1], [2], [3]]))
        self.assertEqual(PBR([[1, -1]], [[1]]).identity(), PBR([[-1]], [[1]]))

    def test_repr(self):
        self.assertEqual(eval(PBR([[-1, 1, 2], [2]], [[-1, 1], [-2, 2]]).__repr__()),
                         PBR([[-1, 1, 2], [2]], [[-1, 1], [-2, 2]]))

        self.assertEqual(eval(PBR([[1, 2, 3, -1, -2, -3],
                                   [1, 2, 3, -1, -2, -3], [3, -2, -3]],
                                  [[2], [3, -2, -3], 
                                   [1, 2, 3, -2, -3]]).__repr__()),
                         PBR([[1, 2, 3, -1, -2, -3],
                              [1, 2, 3, -1, -2, -3], [3, -2, -3]],
                              [[2], [3, -2, -3], [1, 2, 3, -2, -3]]))
        self.assertEqual(eval(PBR([[1, -1]], [[1]]).__repr__()), 
                              PBR([[1, -1]], [[1]]))
        self.assertEqual(eval(PBR([[1, 2], [1, -1]], 
                                  [[1], [2]]).identity().__repr__()),
                         PBR([[-1], [-2]], [[1], [2]]))


class TestTransformation(unittest.TestCase):
    def test_init(self):
        Transformation([0, 1, 2, 3])
        Transformation([1, 1, 3, 2, 4, 3])
        Transformation([9, 3, 1, 2, 0, 8, 1, 2, 0, 5])

    def test_init_fail(self):
        with self.assertRaises(TypeError):
            Transformation([1, 5, 26])
        with self.assertRaises(TypeError):
            Transformation([1])

        with self.assertRaises(TypeError):
            Transformation(26)
        with self.assertRaises(TypeError):
            Transformation(['a', 'b'])
        with self.assertRaises(TypeError):
            Transformation([0.1, 1.0])

    def test_richcmp(self):
        self.assertEqual(Transformation([1, 2, 2, 0]), Transformation([1, 2, 2, 0]))
        self.assertFalse(Transformation([1, 2, 2, 0]) == Transformation([1, 2, 1, 3]))
        self.assertNotEqual(Transformation([1, 2, 2, 0]), Transformation([1, 2, 1, 3]))
        self.assertFalse(Transformation([2, 2, 1]) < Transformation([0, 1, 2]))
        self.assertGreater(Transformation([2, 2, 1]), Transformation([0, 1, 2]))
        self.assertLessEqual(Transformation([2, 2, 1]), Transformation([2, 2, 2]))
        self.assertLessEqual(Transformation([2, 2, 2]), Transformation([2, 2, 2]))
        self.assertGreaterEqual(Transformation([2, 2, 2]), Transformation([2, 2, 0]))
        self.assertGreaterEqual(Transformation([3, 2, 3, 0]), Transformation([3, 2, 0, 1]))

        with self.assertRaises(TypeError):
            Transformation([2, 2, 0]) == Bipartition([1, -1], [2, 3, -2], [-3])
        with self.assertRaises(TypeError):
            Bipartition([1, -1], [2, -2]) < Transformation([0, 1])
        with self.assertRaises(TypeError):
            Bipartition([1, -1], [2, -2]) != Transformation([0, 1])

    def test_mul(self):
        (self.assertEqual(Transformation([1, 3, 2, 1]) *
                         Transformation([0, 3, 2, 2]),
                         Transformation([3, 2, 2, 3])))
        self.assertEqual(Transformation([2, 2, 2]) * Transformation([1, 0, 1]),
                         Transformation([1, 1, 1]))
        (self.assertEqual(Transformation([0, 1, 2, 3, 4, 5]) *
                         Transformation([3, 2, 2, 3, 1, 4]),
                         Transformation([3, 2, 2, 3, 1, 4])))

        with self.assertRaises(TypeError):
            Transformation([0, 2, 1]) * PartialPerm([0, 1], [1, 2], 3)
        with self.assertRaises(TypeError):
            Transformation([0, 2, 1]) * Bipartition([1, -1], [2, 3, -3], [-2])
        with self.assertRaises(TypeError):
            Transformation([0, 1, 2, 3, 4, 5]) * 8

        with self.assertRaises(ValueError):
            Transformation([0, 2, 1]) * Transformation([1, 2, 3, 0])

    def test_pow(self):
        self.assertEqual(Transformation([9, 3, 1, 2, 0, 8, 1, 2, 0, 5]) ** 6,
                         Transformation([5, 1, 2, 3, 9, 0, 2, 3, 9, 8]))
        self.assertEqual(Transformation([2, 2, 2]) ** 30,
                         Transformation([2, 2, 2]))
        self.assertEqual(Transformation([1, 2, 3, 3]) ** 8,
                         Transformation([3, 3, 3, 3]))
        self.assertEqual(Transformation([1, 1, 3, 2, 4, 3]) ** 0,
                         Transformation([1, 1, 3, 2, 4, 3]).identity())

        with self.assertRaises(ValueError):
            Transformation([1, 2, 3, 0]) ** -1
        with self.assertRaises(TypeError):
            Transformation([1, 0, 1, 2]) ** 1.5
        with self.assertRaises(TypeError):
            Transformation([3, 2, 0, 0]) ** 'l'

    def test_dealloc(self):
        U, V = Transformation([1, 0, 1, 2]), Transformation([1, 1, 3, 2, 4, 3])
        del U, V
        with self.assertRaises(NameError):
            V
        with self.assertRaises(NameError):
            U

    def test_identity(self):
        self.assertEqual(Transformation([9, 3, 1, 2, 0,
                                         8, 1, 2, 0, 5]).identity(),
                         Transformation([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(Transformation([2, 2, 2]).identity(),
                         Transformation([0, 1, 2]))
        self.assertEqual(Transformation([1, 2, 3, 3]).identity(),
                         Transformation([0, 1, 2, 3]))

    def test_degree(self):
        self.assertEqual(Transformation([9, 3, 1, 2, 0,
                                         8, 1, 2, 0, 5]).degree(), 10)
        self.assertEqual(Transformation([2, 2, 2]).degree(), 3)
        self.assertEqual(Transformation([1, 2, 3, 3]).degree(), 4)

    def test_repr(self):
        self.assertEqual(eval(Transformation([9, 3, 1, 2, 0,
                                         8, 1, 2, 0, 5]).__repr__()),
                         Transformation([9, 3, 1, 2, 0,
                                         8, 1, 2, 0, 5]))
        self.assertEqual(eval(Transformation([2, 2, 2]).__repr__()),
                         Transformation([2, 2, 2]))
        self.assertEqual(eval(Transformation([1, 2, 3, 3]).__repr__()),
                         Transformation([1, 2, 3, 3]))

if __name__ == '__main__':
    unittest.main()
