from typing import TypeVar, Generic

class Animal:
    def __init__(self, name: str):
        self.name = name

class Cat(Animal):
    def meow(self):
        print("Meow!")

T_contra = TypeVar('T_contra', bound=Animal, contravariant=True)

class AnimalProcessor(Generic[T_contra]):
    def process(self, animal: T_contra) -> None:
        print(f"Processing animal: {animal.name}")

def process_animal_processor(processor: AnimalProcessor[Cat], cat: Cat) -> None:
    processor.process(cat)
    if isinstance(cat, Cat):
        cat.meow()

def main():
    animal_processor: AnimalProcessor[Animal] = AnimalProcessor()
    kitty = Cat("Kitty")
    process_animal_processor(animal_processor, kitty)

if __name__ == "__main__":
    main()
