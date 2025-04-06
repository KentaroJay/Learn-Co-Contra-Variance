from typing import Callable

from src.animals import Animal, Cat

def animal_to_str(animal: Animal) -> str:
    return animal.name

def use_cat_function(func: Callable[[Cat], object]) -> None:
    print(func(Cat("Kitty")))

def main():
    use_cat_function(animal_to_str)  # Output: Kitty
