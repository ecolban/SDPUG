from unittest import TestCase

from random import random

from ..src.finite_geometry import *


class TestSegment(TestCase):

    def one_test(self, args, expected):

        actual = get_segments(*args)
        self.assertTrue(len(set(actual)) == len(actual), msg="The segments are not distinct")
        self.assertEqual(len(expected), len(actual), msg="The number of segments is incorrect")
        for seg in actual:
            for coord in seg:
                self.assertTrue(round(coord, 2) == coord,
                                msg="Coordinates are not rounded to 2 digits after decimal period.")

        error_seg = next((seg for seg in actual if seg not in expected), None)
        self.assertTrue(error_seg is None, msg=f"Incorrect segment: {error_seg}")

    def test_examples(self):

        args_list = [(3, -1, -3.0, 7), (2, -3, -5.5, 7.0), (1, 2, -4.5, 7)]
        expected_list = \
            [[(0, 4.0, 1.0, 7), (1.0, 0, 3.33, 7), (3.33, 0, 5.67, 7), (5.67, 0, 7, 4.0)],
             [(0, 5.17, 2.75, 7), (2.75, 0, 7, 2.83), (0, 2.83, 6.25, 7), (6.25, 0, 7, 0.5), (0, 0.5, 7, 5.17)],
             [(0, 2.25, 4.5, 0.0), (4.5, 7.0, 7, 5.75), (0, 5.75, 7, 2.25)]]

        for a, e in zip(args_list, expected_list):
            self.one_test(a, e)
