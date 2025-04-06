class Animal:
    def __init__(self, name: str):
        self.name = name

class Cat(Animal):
    def meow(self):
        print("Meow!")

class Dog(Animal):
    def bark(self):
        print("Bark!")
