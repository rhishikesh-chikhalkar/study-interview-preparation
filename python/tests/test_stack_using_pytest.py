import pytest


class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        return self._data.append(item)

    def is_empty(self):
        return len(self._data) == 0

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty list")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek on empty list")
        return self._data[-1]

    def size(self):
        return len(self._data)


@pytest.fixture
def stack():
    return Stack()


def test_new_stack_is_empty(stack):
    assert stack.is_empty()


def test_push_increases_size(stack):
    stack.push(10)
    assert stack.size() == 1


def test_pop_returns_last_item(stack):
    stack.push("a")
    stack.push("b")
    assert stack.pop() == "b"


def test_pop_removes_item(stack):
    stack.push(42)
    stack.pop()
    assert stack.is_empty()


def test_pop_empty_raises(stack):
    with pytest.raises(IndexError):
        stack.pop()


def test_peek_does_not_remove(stack):
    stack.push(99)
    stack.peek()
    assert stack.size() == 1


def test_heper_use(stack):
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.size() == 3
