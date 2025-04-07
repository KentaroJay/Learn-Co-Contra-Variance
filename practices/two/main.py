# Hit mypy practices/one and you'll see an error:
# practices/two/main.py:32: error: "AnimalProcessor" expects no type arguments, but 1 given  [type-arg]
# practices/two/main.py:34: error: Argument 1 to "process_animal_processor" has incompatible type "AnimalProcessor"; expected "CatProcessor"  [arg-type]
# Found 2 errors in 1 file (checked 2 source files)
#
# Try to fix this error


class Animal:
    def __init__(self, name: str):
        self.name = name

class Cat(Animal):
    def meow(self):
        print("Meow!")

class AnimalProcessor():
    def process(self, animal: Animal) -> None:
        print(f"Processing animal: {animal.name}")

class CatProcessor():
    def process(self, animal: Animal) -> None:
        print(f"Processing animal: {animal.name}")

def process_animal_processor(processor: CatProcessor, cat: Cat) -> None:
    processor.process(cat)
    if isinstance(cat, Cat):
        cat.meow()

def main():
    animal_processor: AnimalProcessor[Animal] = AnimalProcessor()
    kitty = Cat("Kitty")
    process_animal_processor(animal_processor, kitty)

if __name__ == "__main__":
    main()