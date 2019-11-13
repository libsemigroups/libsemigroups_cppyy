import unittest
import sys
import os
from semigroups import (SemiringABC, Integers, MaxPlusSemiring,
                        MinPlusSemiring, BooleanSemiring,
                        TropicalMaxPlusSemiring, TropicalMinPlusSemiring,
                        NaturalSemiring)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

class TestIntegers(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Integers().__init__(), None)

        with self.assertRaises(TypeError):
            Integers(10)

    def test_plus(self):
        self.assertEqual(Integers().plus(7, 3), 10)
        self.assertEqual(Integers().plus(-2000, 5), -1995)
        self.assertEqual(Integers().plus(0, 20), 20)

        with self.assertRaises(TypeError):
            Integers().plus(10)
        with self.assertRaises(TypeError):
            Integers().plus(10.0, 1)
        with self.assertRaises(TypeError):
            Integers().plus(0, '2')
        with self.assertRaises(TypeError):
            Integers().prod(0, -float('inf'))

    def test_prod(self):
        self.assertEqual(Integers().prod(7, 3), 21)
        self.assertEqual(Integers().prod(-2000, 5), -10000)
        self.assertEqual(Integers().prod(0, 20), 0)

        with self.assertRaises(TypeError):
            Integers().prod(10)
        with self.assertRaises(TypeError):
            Integers().prod(10.0, 1)
        with self.assertRaises(TypeError):
            Integers().prod(0, '2')
        with self.assertRaises(TypeError):
            Integers().prod(0, float('inf'))

    def test_zero(self):
        self.assertEqual(Integers().zero(), 0)

        with self.assertRaises(TypeError):
            Integers().zero(26)

    def test_one(self):
        self.assertEqual(Integers().one(), 1)

        with self.assertRaises(TypeError):
            Integers().one(26)

class TestMaxPlusSemiring(unittest.TestCase):
    def test_init(self):
        MaxPlusSemiring()

        with self.assertRaises(TypeError):
            MaxPlusSemiring(10)

    def test_plus(self):
        self.assertEqual(MaxPlusSemiring().plus(7, 3), 7)
        self.assertEqual(MaxPlusSemiring().plus(-2000, 5), 5)
        self.assertEqual(MaxPlusSemiring().plus(0, 20), 20)
        self.assertEqual(MaxPlusSemiring().plus(-float('inf'), 20), 20)

        with self.assertRaises(TypeError):
            MaxPlusSemiring().plus(10)
        with self.assertRaises(TypeError):
            MaxPlusSemiring().plus(10.0, 1)
        with self.assertRaises(TypeError):
            MaxPlusSemiring().plus(0, '2')
        with self.assertRaises(TypeError):
            MaxPlusSemiring().plus(0, float('inf'))

    def test_prod(self):
        self.assertEqual(MaxPlusSemiring().prod(7, 3), 10)
        self.assertEqual(MaxPlusSemiring().prod(-2000, 5), -1995)
        self.assertEqual(MaxPlusSemiring().prod(0, 20), 20)
        self.assertEqual(MaxPlusSemiring().prod(-float('inf'), 20),
                         -float('inf'))

        with self.assertRaises(TypeError):
            MaxPlusSemiring().prod(10)
        with self.assertRaises(TypeError):
            MaxPlusSemiring().prod(10.0, 1)
        with self.assertRaises(TypeError):
            MaxPlusSemiring().prod(0, '2')
        with self.assertRaises(TypeError):
            MaxPlusSemiring().prod(0, float('inf'))

    def test_zero(self):
        self.assertEqual(MaxPlusSemiring().zero(), -float('inf'))

        with self.assertRaises(TypeError):
            MaxPlusSemiring().zero(26)

    def test_one(self):
        self.assertEqual(MaxPlusSemiring().one(), 0)

        with self.assertRaises(TypeError):
            MaxPlusSemiring().one(26)

class TestMinPlusSemiring(unittest.TestCase):
    def test_init(self):
        MinPlusSemiring()

        with self.assertRaises(TypeError):
            MinPlusSemiring(10)

    def test_plus(self):
        self.assertEqual(MinPlusSemiring().plus(7, 3), 3)
        self.assertEqual(MinPlusSemiring().plus(-2000, 5), -2000)
        self.assertEqual(MinPlusSemiring().plus(0, 20), 0)
        self.assertEqual(MinPlusSemiring().plus(float('inf'), 20), 20)

        with self.assertRaises(TypeError):
            MinPlusSemiring().plus(10)
        with self.assertRaises(TypeError):
            MinPlusSemiring().plus(10.0, 1)
        with self.assertRaises(TypeError):
            MinPlusSemiring().plus(0, '2')
        with self.assertRaises(TypeError):
            MinPlusSemiring().plus(0, -float('inf'))

    def test_prod(self):
        self.assertEqual(MinPlusSemiring().prod(7, 3), 10)
        self.assertEqual(MinPlusSemiring().prod(-2000, 5), -1995)
        self.assertEqual(MinPlusSemiring().prod(0, 20), 20)
        self.assertEqual(MinPlusSemiring().prod(float('inf'), 20),
                         float('inf'))

        with self.assertRaises(TypeError):
            MinPlusSemiring().prod(10)
        with self.assertRaises(TypeError):
            MinPlusSemiring().prod(10.0, 1)
        with self.assertRaises(TypeError):
            MinPlusSemiring().prod(0, '2')
        with self.assertRaises(TypeError):
            MinPlusSemiring().prod(0, -float('inf'))

    def test_zero(self):
        self.assertEqual(MinPlusSemiring().zero(), float('inf'))

        with self.assertRaises(TypeError):
            MinPlusSemiring().zero(26)

    def test_one(self):
        self.assertEqual(MinPlusSemiring().one(), 0)

        with self.assertRaises(TypeError):
            MinPlusSemiring().one(26)

class TestBooleanSemiring(unittest.TestCase):
    def test_init(self):
        BooleanSemiring()

        with self.assertRaises(TypeError):
            BooleanSemiring(False)

    def test_plus(self):
        self.assertEqual(BooleanSemiring().plus(True, True), True)
        self.assertEqual(BooleanSemiring().plus(True, False), True)
        self.assertEqual(BooleanSemiring().plus(False, False), False)

        with self.assertRaises(TypeError):
            BooleanSemiring().plus(1, 0)
        with self.assertRaises(TypeError):
            BooleanSemiring().plus('True', 'False')
        with self.assertRaises(TypeError):
            BooleanSemiring().plus(True)

    def test_prod(self):
        self.assertEqual(BooleanSemiring().prod(True, True), True)
        self.assertEqual(BooleanSemiring().prod(True, False), False)
        self.assertEqual(BooleanSemiring().prod(False, False), False)

        with self.assertRaises(TypeError):
            BooleanSemiring().prod(1, 0)
        with self.assertRaises(TypeError):
            BooleanSemiring().prod('True', 'False')
        with self.assertRaises(TypeError):
            BooleanSemiring().prod(True)

class TestTropicalMaxPlusSemiring(unittest.TestCase):
    def test_init(self):
        TropicalMaxPlusSemiring(20)
        TropicalMaxPlusSemiring(0)

        with self.assertRaises(ValueError):
            TropicalMaxPlusSemiring(-10)
        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring()
        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(20.0)
        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(float('inf'))

    def test_plus(self):
        self.assertEqual(TropicalMaxPlusSemiring(10).plus(7, 3), 7)
        self.assertEqual(TropicalMaxPlusSemiring(30).plus(30, 5), 30)
        self.assertEqual(TropicalMaxPlusSemiring(73).plus(0, 20), 20)
        self.assertEqual(TropicalMaxPlusSemiring(26).plus(-float('inf'), 20), 20)

        with self.assertRaises(ValueError):
            TropicalMaxPlusSemiring(8).plus(10, 7)
        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(12).plus(10.0, 1)
        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(3).plus(0, '2')
        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(8000).plus(0, float('inf'))
        with self.assertRaises(ValueError):
            TropicalMaxPlusSemiring(8000).plus(0, -5)

    def test_prod(self):
        self.assertEqual(TropicalMaxPlusSemiring(10).prod(7, 3), 10)
        self.assertEqual(TropicalMaxPlusSemiring(30).prod(30, 5), 30)
        self.assertEqual(TropicalMaxPlusSemiring(73).prod(0, 20), 20)
        self.assertEqual(TropicalMaxPlusSemiring(26).prod(-float('inf'), 20),
                         -float('inf'))

        with self.assertRaises(ValueError):
            TropicalMaxPlusSemiring(8).prod(10, 7)
        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(12).prod(10.0, 1)
        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(3).prod(0, '2')
        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(8000).prod(0, float('inf'))
        with self.assertRaises(ValueError):
            TropicalMaxPlusSemiring(8000).prod(0, -5)

    def test_zero(self):
        self.assertEqual(TropicalMaxPlusSemiring(10).zero(), -float('inf'))

        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(20).zero(26)

    def test_one(self):
        self.assertEqual(TropicalMaxPlusSemiring(73).one(), 0)

        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(7).one(26)

    def test_threshold(self):
        self.assertEqual(TropicalMaxPlusSemiring(20).threshold(), 20)

        with self.assertRaises(TypeError):
            TropicalMaxPlusSemiring(83).threshold(1)

class TestTropicalMinPlusSemiring(unittest.TestCase):
    def test_init(self):
        TropicalMinPlusSemiring(20)
        TropicalMinPlusSemiring(0)

        with self.assertRaises(ValueError):
            TropicalMinPlusSemiring(-10)
        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring()
        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(20.0)
        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(float('inf'))

    def test_plus(self):
        self.assertEqual(TropicalMinPlusSemiring(10).plus(7, 3), 3)
        self.assertEqual(TropicalMinPlusSemiring(30).plus(30, 5), 5)
        self.assertEqual(TropicalMinPlusSemiring(73).plus(0, 20), 0)
        self.assertEqual(TropicalMinPlusSemiring(26).plus(float('inf'), 20), 20)

        with self.assertRaises(ValueError):
            TropicalMinPlusSemiring(8).plus(10, 7)
        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(12).plus(10.0, 1)
        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(3).plus(0, '2')
        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(8000).plus(0, -float('inf'))
        with self.assertRaises(ValueError):
            TropicalMinPlusSemiring(8000).plus(0, -5)

    def test_prod(self):
        self.assertEqual(TropicalMinPlusSemiring(10).prod(7, 3), 10)
        self.assertEqual(TropicalMinPlusSemiring(30).prod(30, 5), 30)
        self.assertEqual(TropicalMinPlusSemiring(73).prod(0, 20), 20)
        self.assertEqual(TropicalMinPlusSemiring(26).prod(float('inf'), 20),
                         float('inf'))

        with self.assertRaises(ValueError):
            TropicalMinPlusSemiring(8).prod(10, 7)
        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(12).prod(10.0, 1)
        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(3).prod(0, '2')
        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(8000).prod(0, -float('inf'))
        with self.assertRaises(ValueError):
            TropicalMinPlusSemiring(8000).prod(0, -5)

    def test_zero(self):
        self.assertEqual(TropicalMinPlusSemiring(10).zero(), float('inf'))

        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(20).zero(26)

    def test_one(self):
        self.assertEqual(TropicalMinPlusSemiring(73).one(), 0)

        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(7).one(26)

    def test_threshold(self):
        self.assertEqual(TropicalMinPlusSemiring(20).threshold(), 20)

        with self.assertRaises(TypeError):
            TropicalMinPlusSemiring(83).threshold(1)

class TestNaturalSemiring(unittest.TestCase):
    def test_init(self):
        self.assertEqual(NaturalSemiring(23, 5).__init__(23, 5), None)
        self.assertEqual(NaturalSemiring(0, 1).__init__(0, 1), None)

        with self.assertRaises(ValueError):
            NaturalSemiring(23, 0)
        with self.assertRaises(ValueError):
            NaturalSemiring(-1, 26)
        with self.assertRaises(TypeError):
            NaturalSemiring(23, 0.0)
        with self.assertRaises(TypeError):
            NaturalSemiring()
        with self.assertRaises(TypeError):
            NaturalSemiring(23)
        with self.assertRaises(TypeError):
            NaturalSemiring('23', 0)

    def test_plus(self):
        self.assertEqual(NaturalSemiring(5, 7).plus(3, 11), 7)
        self.assertEqual(NaturalSemiring(0, 1).plus(0, 0), 0)
        self.assertEqual(NaturalSemiring(26, 73).plus(26, 83), 36)

        with self.assertRaises(TypeError):
            NaturalSemiring(26, 73).plus(26, float('inf'))
        with self.assertRaises(TypeError):
            NaturalSemiring(26, 73).plus(26)
        with self.assertRaises(TypeError):
            NaturalSemiring(26, 73).plus()
        with self.assertRaises(ValueError):
            NaturalSemiring(26, 73).plus(26, 169)
        with self.assertRaises(ValueError):
            NaturalSemiring(26, 73).plus(26, -3)

    def test_prod(self):
        self.assertEqual(NaturalSemiring(5, 7).prod(3, 11), 5)
        self.assertEqual(NaturalSemiring(0, 1).prod(0, 0), 0)
        self.assertEqual(NaturalSemiring(26, 73).prod(26, 83), 41)

        with self.assertRaises(TypeError):
            NaturalSemiring(26, 73).prod(26, float('inf'))
        with self.assertRaises(TypeError):
            NaturalSemiring(26, 73).prod(26)
        with self.assertRaises(TypeError):
            NaturalSemiring(26, 73).prod()
        with self.assertRaises(ValueError):
            NaturalSemiring(26, 73).prod(26, 169)
        with self.assertRaises(ValueError):
            NaturalSemiring(26, 73).prod(26, -3)

    def test_zero(self):
        self.assertEqual(NaturalSemiring(8, 2).zero(), 0)

        with self.assertRaises(TypeError):
            NaturalSemiring(7, 26).zero(26)

    def test_one(self):
        self.assertEqual(NaturalSemiring(8, 17).one(), 1)

        with self.assertRaises(TypeError):
            NaturalSemiring(27, 89).one(26)

    def test_period(self):
        self.assertEqual(NaturalSemiring(7, 26).period(), 26)

        with self.assertRaises(TypeError):
           NaturalSemiring(7, 26).period(1)

    def test_threshold(self):
        self.assertEqual(NaturalSemiring(20, 6).threshold(), 20)

        with self.assertRaises(TypeError):
            NaturalSemiring(83, 6).threshold(1)

if __name__ == '__main__':
    unittest.main()
