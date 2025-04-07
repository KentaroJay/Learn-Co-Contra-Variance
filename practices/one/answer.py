from typing import List, TypeVar, Generic

T_co = TypeVar('T_co', covariant=True)

class Animal:
    def __init__(self, name: str):
        self.name = name

class Cat(Animal):
    def __init__(self, name: str):
        self.name = name

class Shelter(Generic[T_co]):
    def __init__(self, animals: List[T_co]):
        self.animals = animals

    def get_animals(self) -> List[T_co]:
        return self.animals

def process_animals(shelter: Shelter[Animal]):
    animals = shelter.get_animals()
    for animal in animals:
        print(animal.name)

def main():
    cat_shelter = Shelter([Cat("Whiskers"), Cat("Mittens")])
    animal_shelter = cat_shelter
    process_animals(animal_shelter)

if __name__ == "__main__":
    main()
