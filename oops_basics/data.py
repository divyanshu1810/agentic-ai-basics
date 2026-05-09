class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Student(name={self.name}, age={self.age})"

from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int

s1 = Student("Divyanshu", 22)
print(s1)

s2 = Student("Aman", 20)
print(s2)