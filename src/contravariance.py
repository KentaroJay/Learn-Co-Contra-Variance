from typing import TypeVar, Generic

from src.animals import Animal, Cat

T = TypeVar("T", contravariant=True)

class Consumer(Generic[T]):
    def consume(self, item: T) -> None:
        pass

class AnimalConsumer(Consumer[Animal]):
    def consume(self, item: Animal) -> None:
        print(f"Consuming {item.name}")

def feed_cat(consumer: Consumer[Cat]) -> None:
    consumer.consume(Cat("Kitty"))

def main():
    # Create an animal consumer
    animal_consumer = AnimalConsumer()

    # Use it where a cat consumer is expected
    feed_cat(animal_consumer)  # Output: Consuming Kitty
