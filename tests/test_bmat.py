import unittest, libsemigroups_cppyy
from libsemigroups_cppyy import BooleanMat, Degree, One


class TestBooleanMat(unittest.TestCase):
    def test_init(self):
        BooleanMat([[True, True], [False, False]])
        BooleanMat([[False, True, True], [True, True, False], [False, False, False]])
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
        with self.assertRaises(ValueError):
            BooleanMat([[1.0, 0.0], [0.0, 1.0]])
        with self.assertRaises(ValueError):
            BooleanMat([[True, False], ["i", range(10)]])

        with self.assertRaises(TypeError):
            BooleanMat([[True], [False]])
        with self.assertRaises(TypeError):
            BooleanMat([[True, False], [False, False], [True, True]])
        with self.assertRaises(TypeError):
            BooleanMat([[True, True, False], [False, False]])
        with self.assertRaises(TypeError):
            BooleanMat()

    def test_richcmp(self):
        self.assertEqual(
            BooleanMat([[True, False], [False, True]]),
            BooleanMat([[True, False], [False, True]]),
        )
        self.assertFalse(
            BooleanMat([[True, False], [False, True]])
            != BooleanMat([[True, False], [False, True]])
        )
        self.assertFalse(
            BooleanMat([[True, False], [False, True]])
            == BooleanMat([[False, False], [False, True]])
        )
        self.assertLess(BooleanMat([[False]]), BooleanMat([[True]]))
        self.assertFalse(
            BooleanMat(
                [[False, True, True], [True, True, False], [False, False, False]]
            )
            < BooleanMat(
                [[False, True, False], [True, False, False], [False, False, True]]
            )
        )
        # self.assertLessEqual(BooleanMat([[False]]), BooleanMat([[False]]))
        self.assertGreater(
            BooleanMat([[True, False], [False, True]]),
            BooleanMat([[True, False], [False, False]]),
        )
        self.assertFalse(
            BooleanMat([[True, False], [False, True]])
            > BooleanMat([[True, False], [False, True]])
        )
        # self.assertGreaterEqual(BooleanMat([[False]]), BooleanMat([[False]]))

        # with self.assertRaises(TypeError):
        #     (
        #         Bipartition([1, -2], [-1, 2])
        #         >= BooleanMat([False, False], [True, False])
        #     )
        # with self.assertRaises(TypeError):
        #     BooleanMat([False, False], [True, False]) < Transformation([0, 1])
        # with self.assertRaises(TypeError):
        #     (
        #         BooleanMat([True, False], [False, True])
        #         == PartialPerm([0], [1], 2)
        #     )

    # def test_getitem(self):
    #     self.assertEqual(BooleanMat([[1, 0], [0, 0]])[0], [1, 0])
    #     self.assertEqual(BooleanMat([[1, 0], [0, 0]])[1], [0, 0])

    #     with self.assertRaises(IndexError):
    #         BooleanMat([[1, 0, 1], [1, 0, 0], [0, 1, 1]])[3]

    def test_mul(self):
        (
            self.assertEqual(
                BooleanMat([[True, False], [False, True]])
                * BooleanMat([[False, False], [False, True]]),
                BooleanMat([[False, False], [False, True]]),
            )
        )
        self.assertEqual(
            BooleanMat([[False]]) * BooleanMat([[True]]), BooleanMat([[False]])
        )
        (
            self.assertEqual(
                BooleanMat(
                    [[False, True, True], [True, True, False], [False, False, False]]
                )
                * BooleanMat(
                    [[False, True, False], [True, False, False], [False, False, True]]
                ),
                BooleanMat(
                    [[True, False, True], [True, True, False], [False, False, False]]
                ),
            )
        )

        # with self.assertRaises(TypeError):
        #     BooleanMat([[True, True], [False, False]])
        #     * Transformation([1, 1])
        # with self.assertRaises(TypeError):
        #     BooleanMat(
        #         [
        #             [False, True, True],
        #             [True, True, False],
        #             [False, False, False],
        #         ]
        #     ) * PartialPerm([0, 1], [1, 2], 3)
        # with self.assertRaises(TypeError):
        #     BooleanMat([[True]]) * [[True]]
        # with self.assertRaises(TypeError):
        #     BooleanMat([[True, False], [False, True]]) * Bipartition(
        #         [1, 2], [-1], [-2]
        #     )

        # with self.assertRaises(ValueError):
        #     (
        #         BooleanMat(
        #             [
        #                 [False, True, True],
        #                 [True, True, False],
        #                 [False, False, False],
        #             ]
        #         )
        #         * BooleanMat([[True, False], [False, True]])
        #     )

    def test_pow(self):
        self.assertEqual(
            BooleanMat([[True, False], [False, True]]) ** 30,
            BooleanMat([[True, False], [False, True]]),
        )
        self.assertEqual(BooleanMat([[True]]) ** 26, BooleanMat([[True]]))

        self.assertEqual(
            BooleanMat([[True, False], [True, True]]) ** 7,
            BooleanMat([[True, False], [True, True]]),
        )

        with self.assertRaises(TypeError):
            BooleanMat([[True, False], [True, True]]) ** "i"
        with self.assertRaises(TypeError):
            BooleanMat([[True]]) ** range(10)
        with self.assertRaises(TypeError):
            BooleanMat([[True]]) ** BooleanMat([[True]])

        self.assertEqual(
            BooleanMat([[True, False], [True, True]]) ** 0,
            One(BooleanMat([[True, False], [True, True]])),
        )
        with self.assertRaises(ValueError):
            BooleanMat(
                [[False, True, True], [True, True, False], [False, False, False]]
            ) ** -7

    def test_dealloc(self):
        A = BooleanMat([[True, False], [True, True]])
        B = BooleanMat([[False, False], [False, True]])
        del A, B
        assert "A" not in globals()
        assert "B" not in globals()

    def test_degree(self):
        self.assertEqual(Degree(BooleanMat([[True, True], [False, False]])), 8)
        self.assertEqual(
            Degree(
                BooleanMat(
                    [[False, True, True], [True, True, False], [False, False, False]]
                )
            ),
            8,
        )
        self.assertEqual(Degree(BooleanMat([[True]])), 8)

    def test_identity(self):
        A = BooleanMat([[True, True], [False, False]])
        BM = type(A)
        self.assertEqual(One(A), BM.one())
        self.assertEqual(
            One(
                BooleanMat(
                    [[False, True, True], [True, True, False], [False, False, False]]
                )
            ),
            BM.one(8),
        )
        self.assertEqual(One(BooleanMat([[False]])), BM.one(8))

    def test_rows(self):
        self.assertEqual(
            BooleanMat([[True, True], [False, False]]).rows(),
            [
                [1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
        )
        self.assertEqual(
            BooleanMat(
                [[False, True, True], [True, True, False], [False, False, False]]
            ).rows(),
            [
                [0, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
        )
        self.assertEqual(
            BooleanMat([[False]]).rows(),
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
        )
        self.assertEqual(
            One(BooleanMat([[0, 0], [0, 0]])).rows(),
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
            ],
        )

    def test_repr(self):
        self.assertEqual(
            BooleanMat([[True, True], [False, False]]).__repr__(),
            "11000000\n"
            + "00000000\n"
            + "00000000\n"
            + "00000000\n"
            + "00000000\n"
            + "00000000\n"
            + "00000000\n"
            + "00000000\n",
        )
        self.assertEqual(
            BooleanMat(
                [[False, True, True], [True, True, False], [False, False, False]]
            ).__repr__(),
            "01100000\n"
            + "11000000\n"
            + "00000000\n"
            + "00000000\n"
            + "00000000\n"
            + "00000000\n"
            + "00000000\n"
            + "00000000\n",
        )
