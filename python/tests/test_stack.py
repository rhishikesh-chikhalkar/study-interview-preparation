import unittest


class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def is_empty(self):
        return len(self._data) == 0

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._data[-1]

    def size(self):
        return len(self._data)


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_new_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty())

    def test_push_increses_size(self):
        self.stack.push(10)
        self.assertEqual(self.stack.size(), 1)

    def test_pop_returns_last_item(self):
        self.stack.push("a")
        self.stack.push("b")
        result = self.stack.pop()
        self.assertEqual(result, "b")

    def test_pop_remove_item(self):
        self.stack.push(42)
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())

    def test_pop_empty_raises(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek_does_not_remove(self):
        self.stack.push(99)
        self.stack.peek()
        self.assertEqual(self.stack.size(), 1)

    def _push_three_items(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)

    def test_user_helper(self):
        self._push_three_items()
        self.assertEqual(self.stack.size(), 3)


if __name__ == "__main__":
    unittest.main()
