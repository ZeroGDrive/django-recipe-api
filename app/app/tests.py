"""
Sample Tests
"""

from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module."""

    def test_add_numbers(self):
        """Test that two numbers are added together."""
        self.assertEqual(calc.add(3, 8), 11)
