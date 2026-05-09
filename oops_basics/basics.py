class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.email = None

    @classmethod
    def show(cls):
        print("I am from User class")

    @staticmethod
    def demo():
        print("I am from User class")

User.show()
User.demo()
