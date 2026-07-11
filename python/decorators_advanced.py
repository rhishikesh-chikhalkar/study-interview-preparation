from functools import wraps
import math


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Running function")
        return func(*args, **kwargs)

    return wrapper


@logger
def greet(name):
    print(f"Hello {name}")


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return math.pi * self.radius ** 2

    @classmethod
    def from_diameter(cls, diameter):
        return cls(diameter / 2)

    @staticmethod
    def pi_value():
        return 3.14159


class CallCounter:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call #{self.count}")
        return self.func(*args, **kwargs)


@CallCounter
def say_hi():
    print("Hi")
