import os
import sys
import pytest

# Append the python directory to sys.path so we can import from solutions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.print_even_odd_threads import EvenOddCondition, EvenOddSemaphore


@pytest.mark.parametrize("limit", [0, 1, 2, 5, 10, 15])
def test_even_odd_condition(limit):
    output = []
    solver = EvenOddCondition(limit, output)
    solver.run()
    # Expected output is numbers from 1 to limit
    expected = list(range(1, limit + 1))
    assert output == expected


@pytest.mark.parametrize("limit", [0, 1, 2, 5, 10, 15])
def test_even_odd_semaphore(limit):
    output = []
    solver = EvenOddSemaphore(limit, output)
    solver.run()
    # Expected output is numbers from 1 to limit
    expected = list(range(1, limit + 1))
    assert output == expected
