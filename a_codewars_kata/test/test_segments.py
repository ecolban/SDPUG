from unittest import TestCase

from finite_geometry import *


class TestSegment(TestCase):

    def one_test(self, args, expected):
        actual = segments(*args)
        print(actual)
        self.assertTrue(len(set(actual)) == len(actual), msg="The segments are not distinct")
        self.assertEqual(len(expected), len(actual), msg="The number of segments is incorrect")
        error_seg = next((seg for seg in actual if seg not in expected), None)
        self.assertTrue(error_seg is None, msg=f"Incorrect segment: {error_seg}")

    def test_examples(self):
        args_list = [(3, -1, "-3", "7"), (2, -3, "-5.5", "7"), (1, 2, "-4.5", "7"), (315, 378, "12247.2", "64.8")]
        expected_list = \
            [[("0", "4", "1", "7"), ("1", "0", "10/3", "7"), ("10/3", "0", "17/3", "7"), ("17/3", "0", "7", "4")],
             [("0", "31/6", "11/4", "7"), ("11/4", "0", "7", "17/6"), ("0", "17/6", "25/4", "7"),
              ("25/4", "0", "7", "1/2"), ("0", "1/2", "7", "31/6")],
             [("0", "9/4", "9/2", "0"), ("9/2", "7", "7", "23/4"), ("0", "23/4", "7", "9/4")],
             [("0", "324/5", "324/5", "54/5"), ("0", "54/5", "324/25", "0"), ("324/25", "324/5", "324/5", "108/5"),
              ("0", "108/5", "648/25", "0"), ("648/25", "324/5", "324/5", "162/5"), ("0", "162/5", "972/25", "0"),
              ("972/25", "324/5", "324/5", "216/5"), ("0", "216/5", "1296/25", "0"),
              ("1296/25", "324/5", "324/5", "54"), ("0", "54", "324/5", "0")]
             ]

        for a, e in zip(args_list, expected_list):
            self.one_test(a, e)
            for coords in e:
                print(tuple(float(Fraction(x)) for x in coords))
