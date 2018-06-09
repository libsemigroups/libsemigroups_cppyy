# pylint: disable = C0103,E0611,C0111,W0104,R0201
import unittest
import sys
import os
from semigroups import FpSemigroup, FpMonoid

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if path not in sys.path:
    sys.path.insert(1, path)
del path

class TestFpSemigroup(unittest.TestCase):
    def test_valid_init(self):
        with self.assertRaises(TypeError):
            FpSemigroup(['a'],[])
        with self.assertRaises(ValueError):
            FpSemigroup('aa',[])
        with self.assertRaises(TypeError):
            FpSemigroup('a', []).check_word({})
        FpSemigroup('a', [])
        FpSemigroup('~', [])
        FpSemigroup('a', [['a', 'aa']])
        FpSemigroup('ab', [['b', 'a(a)']])
        FpSemigroup('a', [['a', 'a^4']])
        FpSemigroup('ab', [['b', '(ab)^2a']])

    def test_parse_word(self):
        S = FpSemigroup('~', [])
        self.assertFalse(S._pure_letter_alphabet)
        self.assertEqual(S._parse_word("~"),"~")
        S = FpSemigroup('a', [])
        self.assertEqual(S._parse_word("aa"),"aa")
        self.assertEqual(S._parse_word("()(()())"),"")
        self.assertEqual(S._parse_word("ba^10b"),"baaaaaaaaaab")
        self.assertEqual(S._parse_word("((b)a)^3b"),"bababab")
        with self.assertRaises(ValueError):
            S._parse_word(")(")
        with self.assertRaises(ValueError):
            S._parse_word("(((b)^2(a))))")
        with self.assertRaises(ValueError):
            S._parse_word("(((b)^2)))((((a))(b))")
        with self.assertRaises(ValueError):
            S._parse_word("^2")
        with self.assertRaises(ValueError):
            S._parse_word("a^")
        with self.assertRaises(ValueError):
            S._parse_word("a^a")

    def test_alphabet(self):
        with self.assertRaises(ValueError):
            FpSemigroup('', [['a', 'aa']])
        with self.assertRaises(ValueError):
            FpSemigroup('a', [['b', 'aa']])
        with self.assertRaises(ValueError):
            FpSemigroup('aa', [['b', 'aa']])

    def test_rels(self):
        with self.assertRaises(TypeError):
            FpSemigroup("ab", "[\"a\", \"aa\"]")
        with self.assertRaises(TypeError):
            FpSemigroup("ab", ["\"b", "aa\""])
        with self.assertRaises(TypeError):
            FpSemigroup("ab", [["a", "aa", "b"]])
        with self.assertRaises(TypeError):
            FpSemigroup("ab", [["b", ["a", "a"]]])
        with self.assertRaises(ValueError):
            FpSemigroup("ab", [["b", "ca"]])

    def test_set_report(self):
        S = FpSemigroup("a", [["a", "aa"]])
        S.set_report(True)
        S.set_report(False)
        with self.assertRaises(TypeError):
            S.set_report("False")

    def test_is_finite(self):
        S = FpSemigroup("ab", [["a", "aa"], ["b", "bb"], ["ab", "ba"]])
        self.assertEqual(S.is_finite(), True)
        S = FpSemigroup("ab", [])
        self.assertEqual(S.is_finite(), False)
        S = FpSemigroup("ab", [["a","a"],["a","a"]])
        self.assertEqual(S.is_finite(), False)

    def test_size(self):
        S = FpSemigroup("a", [["a", "aa"]])
        self.assertEqual(S.size(), 1)
        S = FpSemigroup("ab", [["a", "aa"], ["b", "bb"], ["ab", "ba"]])
        self.assertEqual(S.size(), 3)
        S = FpSemigroup("ab", [])
        self.assertEqual(S.size(), float("inf"))

    def test_normal_form(self):
        S = FpSemigroup("a", [["a", "aa"]])
        self.assertEqual(S.normal_form("a^1000"), "a")
        S = FpMonoid("a", [["a", "aa"]])
        self.assertEqual(S.normal_form("a^0"), "1")
        S = FpSemigroup("ab", [["a", "aaa"], ["b", "bb"], ["ab", "ba"]])
        self.assertEqual(S.normal_form("(ba)^10"), "aab")

    def test_word_to_class_index(self):
        S = FpSemigroup("ab", [["a", "aa"], ["b", "bb"], ["ab", "ba"]])
        self.assertIsInstance(S.word_to_class_index("aba"), int)
        with self.assertRaises(TypeError):
            S.word_to_class_index([1, "0"])
        with self.assertRaises(TypeError):
            S.word_to_class_index(["aba"])
        self.assertEqual(S.word_to_class_index("aba"),
                        S.word_to_class_index("abaaabb"))
        S = FpSemigroup("ab",[])
        with self.assertRaises(ValueError):
            S.word_to_class_index("aba")

    def test_equal(self):
        S = FpSemigroup("ab",[["a", "a^5"],["b","bb"],["ab","ba"]])
        self.assertTrue(S.equal("a","a^5"))
        self.assertTrue(S.equal("a","aaaaa"))
        self.assertTrue(S.equal("abb","ba"))
        self.assertTrue(S.equal("ab","((a)^3b)^167"))
        S = FpSemigroup("ab",[])
        with self.assertRaises(ValueError):
            S.equal("a", "b")

    def test_contains(self):
        FpS = FpSemigroup("ab", [["aa", "a"], ["bbb", "b"], ["ba", "ab"]])
        self.assertFalse(1 in FpS)
        self.assertTrue("abb" in FpS)
        self.assertFalse("c" in FpS)
        self.assertFalse("" in FpS)

    def test_enumerate(self):
        S = FpSemigroup("ab",[["a", "a^5"],["b","bb"],["ab","ba"]])
        S.enumerate(73)
        S = FpSemigroup("ab",[])
        with self.assertRaises(ValueError):
            S.enumerate(73)

    def test_nridempotents(self):
        S = FpSemigroup("ab",[["a", "a^5"],["b","bb"],["ab","ba"]])
        self.assertEqual(S.nridempotents(),3)
        S = FpMonoid("ab",[["a", "a^5"], ["b","bb"], ["ab","ba"]])
        self.assertEqual(S.nridempotents(),4)
        S = FpSemigroup("ab",[])
        with self.assertRaises(ValueError):
            S.nridempotents()

    def test_factorisation(self):
        S = FpSemigroup("ab",[["a", "a^5"],["b","bb"],["ab","ba"]])
        self.assertEqual(S.factorisation("aba"),[0, 0, 1])
        S = FpSemigroup("ab",[])
        with self.assertRaises(ValueError):
            S.factorisation("aba")

    def test_repr(self):
        S = FpSemigroup("ab", [["aa", "a"], ["bbb", "ab"], ["ab", "ba"]])
        self.assertEqual(S.__repr__(),
                         "<fp semigroup with 2 generators and 3 relations>")

class TestFpMonoid(unittest.TestCase):

    def test_valid_init(self):
        FpMonoid("", [])
        FpMonoid("a", [])
        with self.assertRaises(ValueError):
            FpMonoid("1", [])
        FpMonoid("a", [["a", "aa"]])
        FpMonoid("ab", [["b", "aa"]])
        FpMonoid("ab", [["1", "aa"]])
        FpMonoid("ab", [["b", "a^2"]])
        FpMonoid("ab", [["1", "(a)^6"]])

    def test_alphabet(self):
        with self.assertRaises(ValueError):
            FpMonoid("", [["a", "aa"]])
        with self.assertRaises(ValueError):
            FpMonoid("a", [["b", "aa"]])
        with self.assertRaises(ValueError):
            FpMonoid("aa", [["b", "aa"]])

    def test_rels(self):
        with self.assertRaises(TypeError):
            FpMonoid("ab", "[\"a\", \"aa\"]")
        with self.assertRaises(TypeError):
            FpMonoid("ab", ["\"b\", \"aa\""])
        with self.assertRaises(TypeError):
            FpMonoid("ab", [["a", "aa", "b"]])
        with self.assertRaises(TypeError):
            FpMonoid("ab", [["b", ["a", "a"]]])
        with self.assertRaises(ValueError):
            FpMonoid("ab", [["b", "ca"]])

    def test_contains(self):
        FpM = FpMonoid("ab", [["aa", "a"], ["bbb", "b"], ["ba", "ab"]])
        self.assertFalse(1 in FpM)
        self.assertTrue("abb" in FpM)
        self.assertTrue("" in FpM)

    def test_set_report(self):
        M = FpMonoid("a", [["a", "aa"]])
        M.set_report(True)
        M.set_report(False)
        with self.assertRaises(TypeError):
            M.set_report("False")

    def test_current_max_word_length(self):
        S = FpSemigroup("ab",[["a", "a^5"],["b","bb"],["ab","ba"]])
        S.current_max_word_length()

    def test_size(self):
        self.assertEqual(FpMonoid("a", [["a", "aa"]]).size(), 2)
        self.assertEqual(FpMonoid("ab", [["a", "aa"], ["b", "bb"],
        ["ab", "ba"]]).size(), 4)

    def test_word_to_class_index(self):
        M = FpMonoid("ab", [["a", "aa"], ["b", "bb"], ["ab", "ba"]])
        self.assertEqual(M.word_to_class_index('a'),
                         M.word_to_class_index('aa'))
        self.assertNotEqual(M.word_to_class_index('a'),
                            M.word_to_class_index('bb'))
        self.assertIsInstance(M.word_to_class_index('aba'), int)

    def test_repr(self):
        M = FpMonoid("ab", [["aa", "a"], ["bbb", "ab"], ["ab", "ba"]])
        self.assertEqual(M.__repr__(),
                         "<fp monoid with 2 generators and 3 relations>")

class Test_FPSOME(unittest.TestCase):

    def test_valid_init(self):
        FpS = FpSemigroup("ab", [["aa", "a"], ["bbb", "b"], ["ba", "ab"]])
        FpS.equal("a", "aba")
        FpS = FpSemigroup("mo", [["m", "mm"], ["ooo", "o"], ["mo", "om"]])
        FpS.equal("moo", "ooo")
        FpS = FpSemigroup("cowie", [["c", "o"], ["o", "w"], ["w", "i"],
                                   ["i", "e"], ["ee", "e"]])
        FpS.equal("cowie","cowie")
        FpS2 = FpSemigroup('~', [["~~", "~"]])
        FpS2.equal("~", "~~")
        with self.assertRaises(TypeError):
            FpS.equal(FpS, FpS)
        with self.assertRaises(ValueError):
            FpS.equal("abc", "abc")

    def test_eq_(self):
        FpS = FpSemigroup("ab", [["a^10", "a"], ["bbb", "b"], ["ba", "ab"]])
        a = "aba"
        b = a
        self.assertTrue(FpS.equal(a, b))
        a = "aaba"
        b = "ba^3"
        self.assertTrue(FpS.equal(a, b))
        a = ""
        self.assertEqual(a, a)

    def test_ne_(self):
        FpS = FpSemigroup("ab", [["a^10", "a"], ["bbb", "b"], ["ba", "ab"]])
        a = "aba"
        b = a + a
        self.assertFalse(FpS.equal(a, b))
        a = "aaba"
        b = "ba^4"
        self.assertFalse(FpS.equal(a, b))

    def test_identity(self):
        FpS = FpSemigroup("ab", [["a^10", "a"], ["bbb", "b"], ["ba", "ab"]])
        a = FpS[0].get_value()
        self.assertEqual(a.identity().word, "")
        FpS = FpMonoid("ab", [["a^10", "a"], ["bbb", "b"], ["ba", "ab"]])
        a = FpS[1].get_value()
        self.assertEqual(a.identity().word, "1")

    def test_mul(self):
        FpS = FpSemigroup("ab", [["aa", "a"], ["bbb", "b"], ["ba", "ab"]])
        other = "aa"
        a = FpS[1].get_value()
        a * a
        self.assertEqual(a.word + a.word, (a * a).word)
        with self.assertRaises(TypeError):
            a * other
        with self.assertRaises(TypeError):
            FpSemigroup("a", [["aa", "a"]])[0].get_value() * a

    def test_repr(self):
        FpS = FpSemigroup("ab", [["aa", "a"], ["bbb", "b"], ["ab", "ba"]])
        self.assertEqual(FpS[0].__repr__(), "'" + FpS[0].get_value().Repword + "'")


if __name__ == "__main__":
    unittest.main()
