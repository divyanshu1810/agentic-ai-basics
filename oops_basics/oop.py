# Encapsulation
class Animal:
    def __init__(self, name):
        self.name = name

    # Polymorphism
    def sound(self):
        pass


# Inheritance
class Dog(Animal):

    # Abstraction + Polymorphism
    def sound(self):
        return "Bark"


class Cat(Animal):

    def sound(self):
        return "Meow"


dog = Dog("Tommy")
cat = Cat("Kitty")

print(dog.sound())  # Bark
print(cat.sound())  # Meow