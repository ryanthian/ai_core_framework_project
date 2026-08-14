import unittest

from skill_math import add_points


class SkillMathTest(unittest.TestCase):
    def test_add_points_adds_positive_delta(self):
        self.assertEqual(add_points(7, 5), 12)

    def test_add_points_preserves_negative_adjustments(self):
        self.assertEqual(add_points(7, -2), 5)


if __name__ == "__main__":
    unittest.main()
