"""Unit tests for the maintained students.py module."""

import unittest

import students


class StudentMaintenanceTests(unittest.TestCase):
    def test_empty_list_average_is_zero(self):
        self.assertEqual(students.average_score([]), 0.0)

    def test_empty_list_highest_is_none(self):
        self.assertIsNone(students.highest_score([]))

    def test_median_is_calculated(self):
        records = [
            {"name": "A", "score": 20},
            {"name": "B", "score": 80},
            {"name": "C", "score": 60},
        ]
        self.assertEqual(students.median_score(records), 60.0)

    def test_invalid_score_is_rejected(self):
        with self.assertRaises(ValueError):
            students.validate_student("Test Student", 120)

    def test_invalid_name_is_rejected(self):
        with self.assertRaises(ValueError):
            students.validate_student("   ", 50)


if __name__ == "__main__":
    unittest.main()
