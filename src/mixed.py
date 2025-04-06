from typing import TypeVar, Generic

from src.animals import Animal, Cat

T = TypeVar("T")

class Processor(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    def set(self, value: T) -> None:
        self.value = value

cat_processor = Processor(Cat("Kitty"))
animal_processor: Processor[Animal] = cat_processor  # mypy error
