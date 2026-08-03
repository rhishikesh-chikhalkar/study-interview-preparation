import unittest
import pytest


class MyTests(unittest.TestCase):  # <- the clipboard
    def setUp(self):
        self.stack = []
        # This runs BEFORE every single test method

    def tearDown(self):
        self.stack = None
        # This runs AFTER every single test method

    def test_addition(self):  # <- one question (must start with test_)
        self.assertEqual(1 + 1, 2)  # <- checking the answer


class TestNumbers(unittest.TestCase):
    def test_even_numbers(self):
        for i in [2, 4, 5, 6, 8]:
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)


@pytest.mark.parametrize("i", [2, 4, 5, 6, 8])
def test_even_numbers(i):
    assert i % 2 == 0
