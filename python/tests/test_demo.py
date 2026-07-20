import unittest


class MyTests(unittest.TestCase):  # <- the clipboard
    def setUp(self):
        self.stack = []
        # This runs BEFORE every single test method

    def tearDown(self):
        self.stack = None
        # This runs AFTER every single test method

    def test_addition(self):  # <- one question (must start with test_)
        self.assertEqual(1 + 1, 2)  # <- checking the answer
