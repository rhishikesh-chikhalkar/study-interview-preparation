"""
Problem Statement:
Print even and odd numbers up to a given limit using two threads while maintaining the correct sequence.
For example, if limit = 10, the output should be: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.

We implement this classic multithreading problem in Python using two different synchronization mechanisms:
1. wait() & notify() (using threading.Condition)
2. Semaphores (using threading.Semaphore)
"""

import threading
from typing import List, Optional


class EvenOddCondition:
    """
    Solves the even/odd printing problem using threading.Condition,
    which implements the wait() / notify() pattern.
    """

    def __init__(self, limit: int, output_list: Optional[List[int]] = None):
        self.limit = limit
        self.output_list = output_list
        self.current = 1
        self.cond = threading.Condition()

    def print_odd(self) -> None:
        while True:
            with self.cond:
                # Wait while the current number is even
                while self.current <= self.limit and self.current % 2 == 0:
                    self.cond.wait()

                # If we have reached past the limit, notify any waiting thread and exit
                if self.current > self.limit:
                    self.cond.notify_all()
                    break

                # Print/collect the odd number
                if self.output_list is not None:
                    self.output_list.append(self.current)
                else:
                    print(f"Thread-Odd: {self.current}")

                self.current += 1
                # Notify the even thread that state has changed
                self.cond.notify_all()

    def print_even(self) -> None:
        while True:
            with self.cond:
                # Wait while the current number is odd
                while self.current <= self.limit and self.current % 2 != 0:
                    self.cond.wait()

                # If we have reached past the limit, notify any waiting thread and exit
                if self.current > self.limit:
                    self.cond.notify_all()
                    break

                # Print/collect the even number
                if self.output_list is not None:
                    self.output_list.append(self.current)
                else:
                    print(f"Thread-Even: {self.current}")

                self.current += 1
                # Notify the odd thread that state has changed
                self.cond.notify_all()

    def run(self) -> None:
        t1 = threading.Thread(target=self.print_odd)
        t2 = threading.Thread(target=self.print_even)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


class EvenOddSemaphore:
    """
    Solves the even/odd printing problem using two threading.Semaphore instances.
    We alternate control by releasing/acquiring the respective semaphores.
    """

    def __init__(self, limit: int, output_list: Optional[List[int]] = None):
        self.limit = limit
        self.output_list = output_list
        self.current = 1
        # The odd thread starts first, so its semaphore is initialized to 1 (available)
        self.sem_odd = threading.Semaphore(1)
        # The even thread waits, so its semaphore is initialized to 0 (locked)
        self.sem_even = threading.Semaphore(0)

    def print_odd(self) -> None:
        while True:
            self.sem_odd.acquire()
            if self.current > self.limit:
                # Release the even semaphore so the other thread can exit
                self.sem_even.release()
                break

            # Print/collect the odd number
            if self.output_list is not None:
                self.output_list.append(self.current)
            else:
                print(f"Thread-Odd: {self.current}")

            self.current += 1
            # Release the even semaphore to let the even thread run
            self.sem_even.release()

    def print_even(self) -> None:
        while True:
            self.sem_even.acquire()
            if self.current > self.limit:
                # Release the odd semaphore so the other thread can exit
                self.sem_odd.release()
                break

            # Print/collect the even number
            if self.output_list is not None:
                self.output_list.append(self.current)
            else:
                print(f"Thread-Even: {self.current}")

            self.current += 1
            # Release the odd semaphore to let the odd thread run
            self.sem_odd.release()

    def run(self) -> None:
        t1 = threading.Thread(target=self.print_odd)
        t2 = threading.Thread(target=self.print_even)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == "__main__":
    limit = 10
    print("--- 1. Testing wait() & notify() (threading.Condition) ---")
    cond_solver = EvenOddCondition(limit)
    cond_solver.run()

    print("\n--- 2. Testing Semaphores (threading.Semaphore) ---")
    sem_solver = EvenOddSemaphore(limit)
    sem_solver.run()
