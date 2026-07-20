import unittest

class MyTests(unittest.TestCase):      # <- the clipboard

    def setUp(self):
        self.stack = [] 
        # This runs BEFORE every single test method

    def tearDown(self):
        self.stack = None
        # This runs AFTER every single test method

    def test_addition(self):           # <- one question (must start with test_)
        self.assertEqual(1 + 1, 2)    # <- checking the answer

self.assertEqual(result, 42)        # "is result exactly 42?"
self.assertIn('hello', my_list)     # "is 'hello' in the list?"
self.assertRaises(ValueError, fn)   # "does fn() blow up with ValueError?"
self.assertFalse(x)                 # "is x False?"

