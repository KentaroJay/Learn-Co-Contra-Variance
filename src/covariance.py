from typing import TypeVar, Generic, List

from src.animals import Animal, Cat

T = TypeVar("T", covariant=True)

class ReadOnlyList(Generic[T]):
    def __init__(self, items: List[T]):
        self.items = items

    def get(self, index: int) -> T:
        return self.items[index]

def main():
    # Create a list of cats
    cat_list = ReadOnlyList([Cat("Kitty")])

    # Assign it to a variable expecting animals
    animal_list: ReadOnlyList[Animal] = cat_list

    # Access it
    print(animal_list.get(0).name)  # Output: Kitty
