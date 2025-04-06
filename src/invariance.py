from typing import List

from src.animals import Animal, Cat

def print_animals(animals: List[Animal]) -> None:
    for animal in animals:
        print(animal.name)

def main():
    cat_list: List[Cat] = [Cat("Kitty")]
    print_animals(cat_list)  # mypy will complain
