import unittest
from libsemigroups_cppyy import FroidurePin, Transformation, PartialPerm


class TestFroidurePin(unittest.TestCase):
    def test_init(self):
        FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))

        with self.assertRaises(KeyError):
            FroidurePin()

        with self.assertRaises(ValueError):
            FroidurePin(PartialPerm([1, 2], [0, 1], 3), Transformation([0, 1]))

        with self.assertRaises(TypeError):
            FroidurePin({2, 3})

    # def test_right_cayley_graph(self):
    #     #FroidurePin(-1).right_cayley_graph()
    #     #self.assertTrue(isinstance(FroidurePin(-1).right_cayley_graph(),
    #     #                           CayleyGraph))

    # def test_left_cayley_graph(self):
    #     FroidurePin(Transformation([0, 1])).right_cayley_graph()
    #     self.assertTrue(isinstance(FroidurePin(-1).left_cayley_graph(),
    #                               CayleyGraph))


# class TestOtherFunctions(unittest.TestCase):
#     def test_full_transformation_monoid(self):
#         self.assertEqual(full_transformation_monoid(3)[7],
#                          FroidurePin(Transformation([1, 0, 2]),
#                                    Transformation([0, 0, 2]),
#                                    Transformation([2, 0, 1]))[7])
#         self.assertEqual(full_transformation_monoid(2)[5],
#                          FroidurePin(Transformation([0, 0]),
#                                    Transformation([0, 1]))[5])
#         self.assertEqual(full_transformation_monoid(1)[0],
#                          FroidurePin(Transformation([0]))[0])
#
#         with self.assertRaises(TypeError):
#             full_transformation_monoid(2.5)
#
#         with self.assertRaises(ValueError):
#             full_transformation_monoid(-7)
