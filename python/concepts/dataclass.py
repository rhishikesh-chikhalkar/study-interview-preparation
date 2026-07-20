"""
dataclass is nothing but a regular class which is used to store data.
"""

from dataclasses import dataclass


# Without dataclass
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"User(name={self.name!r}, age={self.age!r})"

    def __eq__(self, other):
        return (self.name, self.age) == (other.name, other.age)


@dataclass
class UserData:
    name: str
    age: int


u1 = User("A", 30)
