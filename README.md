# Comprehensive Guide to Python Type Covariance and Contravariance with Hands-on Examples

You’ve asked for a deep dive into Python’s type covariance and contravariance, complete with experimental code examples to get your hands dirty and fully grasp the motivation behind these concepts. This guide is designed to be comprehensive, self-contained, and practical, blending theory with exercises you can run yourself. We’ll explore what covariance and contravariance mean, why they matter, and how to implement them in Python using the `typing` module and the `mypy` type checker. Let’s roll up our sleeves and get started!

---

## Introduction: What Are Covariance and Contravariance?

Covariance and contravariance are concepts from type theory that describe how generic types (like `List[T]` or custom classes) behave when their type parameters are related by inheritance. They’re crucial in Python’s type hinting system, introduced with PEP 484, to ensure type safety while maintaining flexibility in generic programming.

- **Covariance**: If `Cat` is a subtype of `Animal`, a covariant generic type allows `Container[Cat]` to be treated as a subtype of `Container[Animal]`. This is perfect for read-only scenarios, where you’re retrieving values but not modifying them.
- **Contravariance**: Conversely, if `Cat` is a subtype of `Animal`, a contravariant generic type allows `Container[Animal]` to be used where `Container[Cat]` is expected. This fits write-only or consumer scenarios, like functions taking parameters.
- **Invariance**: By default, Python generic types are invariant, meaning `Container[Cat]` and `Container[Animal]` are unrelated unless explicitly specified otherwise.

These properties are controlled in Python using `TypeVar` from the `typing` module, with options like `covariant=True` or `contravariant=True`. To see why this matters, let’s set up our environment and dive into some hands-on experiments.

---

## Setting Up Your Environment

Before we begin, you’ll need:

1. **Python 3.7+**: Type hints work best in modern versions.
2. **`mypy`**: A static type checker to enforce our type rules.
Install it with:
    
    ```bash
    pip install mypy
    
    ```
    
3. **A Code Editor**: Any will do—VSCode, PyCharm, or even a text editor with a terminal.

We’ll also define some base classes for our experiments:

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

class Cat(Animal):
    def meow(self):
        print("Meow!")

class Dog(Animal):
    def bark(self):
        print("Bark!")

```

Save this in a file (e.g., `animals.py`)—we’ll import it later. Now, let’s explore covariance and contravariance through practical examples.

---

## Experiment 1: Covariance with Read-Only Collections

### Motivation

Imagine you have a list of `Cat` objects, and you want to pass it to a function expecting a list of `Animal` objects, since every `Cat` is an `Animal`. This should be safe if you’re only *reading* from the list (e.g., getting elements), because you won’t add a `Dog` to a list of cats. Covariance makes this possible.

<aside>
💡

The issue with 'adding a Dog to a list of cats' arises with *mutable* lists. If a list meant for `Cat` objects could have a `Dog` added (by having a method like `add` to add `Dog` object to `ReadOnlyList[Cat]` ), it would violate type safety, as the list would contain an unexpected type.

</aside>

### Code Example

Let’s create a `ReadOnlyList` that’s covariant in its type parameter `T`:

```python
from typing import TypeVar, Generic, List

T = TypeVar("T", covariant=True)

class ReadOnlyList(Generic[T]):
    def __init__(self, items: List[T]):
        self.items = items

    def get(self, index: int) -> T:
        return self.items[index]

# Create a list of cats
cat_list = ReadOnlyList([Cat("Kitty")])

# Assign it to a variable expecting animals
animal_list: ReadOnlyList[Animal] = cat_list

# Access it
print(animal_list.get(0).name)  # Output: Kitty

```

Save this as `covariance.py` and run:

```bash
mypy covariance.py

```

If all’s well, `mypy` reports no errors. Then execute:

```bash
python covariance.py

```

You’ll see "Kitty" printed.

### What’s Happening?

- `T` is marked `covariant=True`, so `ReadOnlyList[Cat]` is a subtype of `ReadOnlyList[Animal]`.
- Since we’re only reading (via `get`), it’s safe to treat a list of cats as a list of animals.

### Experiment: Remove Covariance

Change `T = TypeVar("T", covariant=True)` to `T = TypeVar("T")` and run `mypy` again:

```
error: Incompatible types in assignment (expression has type "ReadOnlyList[Cat]", variable has type "ReadOnlyList[Animal]")

```

Without covariance, Python’s type system is invariant by default, rejecting the assignment. This shows why covariance is necessary for read-only flexibility.

---

## Experiment 2: Contravariance with Consumers

### Motivation

Now suppose you have a function that feeds a `Cat` to a consumer. If you have a consumer that can handle any `Animal`, it should work for a `Cat` too, since cats are animals. Contravariance enables this by allowing a consumer of a supertype to substitute for a consumer of a subtype.

### Code Example

Let’s define a contravariant `Consumer`:

```python
from typing import TypeVar, Generic

T = TypeVar("T", contravariant=True)

class Consumer(Generic[T]):
    def consume(self, item: T) -> None:
        pass

class AnimalConsumer(Consumer[Animal]):
    def consume(self, item: Animal) -> None:
        print(f"Consuming {item.name}")

def feed_cat(consumer: Consumer[Cat]) -> None:
    consumer.consume(Cat("Kitty"))

# Create an animal consumer
animal_consumer = AnimalConsumer()

# Use it where a cat consumer is expected
feed_cat(animal_consumer)  # Output: Consuming Kitty

```

Save as `contravariance.py`, then:

```bash
mypy contravariance.py  # No errors
python contravariance.py  # Runs fine

```

### What’s Happening?

- `T` is `contravariant=True`, so `Consumer[Animal]` can be used as a `Consumer[Cat]`.
- An `AnimalConsumer` can consume any animal, including cats, making this substitution safe.

### Experiment: Remove Contravariance

Set `T = TypeVar("T")` and re-run `mypy`:

```
error: Argument 1 to "feed_cat" has incompatible type "AnimalConsumer"; expected "Consumer[Cat]"

```

Without contravariance, the type system forbids this, showing its role in enabling flexible parameter handling.

---

## Experiment 3: Invariance with Mutable Collections

### Motivation

Python’s built-in `list` is invariant—`List[Cat]` isn’t a `List[Animal]`—because it’s mutable. Why? If it were covariant, you could add a `Dog` to a `List[Cat]`, breaking type safety. Let’s see this in action.

### Code Example

```python
from typing import List

def print_animals(animals: List[Animal]) -> None:
    for animal in animals:
        print(animal.name)

cat_list: List[Cat] = [Cat("Kitty")]
print_animals(cat_list)  # mypy will complain

```

Save as `invariance.py` and run:

```bash
mypy invariance.py

```

Output:

```
error: Argument 1 to "print_animals" has incompatible type "List[Cat]"; expected "List[Animal]"

```

### Why Invariance?

If `List` were covariant, this would be allowed:

```python
def add_dog(animals: List[Animal]) -> None:
    animals.append(Dog("Fido"))

cat_list: List[Cat] = [Cat("Kitty")]
add_dog(cat_list)  # Adds a Dog to a Cat list—disaster!

```

Invariance prevents this, ensuring type safety for mutable structures.

---

## Experiment 4: Combining Variance with Callables

### Motivation

Functions often involve both inputs (contravariant) and outputs (covariant). Let’s explore this with `Callable`.

### Code Example

```python
from typing import Callable

def animal_to_str(animal: Animal) -> str:
    return animal.name

def use_cat_function(func: Callable[[Cat], str]) -> None:
    print(func(Cat("Kitty")))

use_cat_function(animal_to_str)  # Output: Kitty

```

Save as `callable.py`:

```bash
mypy callable.py  # No errors
python callable.py  # Works

```

### What’s Happening?

- `Callable[[T], R]` is contravariant in `T` (parameters) and covariant in `R` (return type).
- A function taking `Animal` works where one taking `Cat` is expected, due to contravariance.

---

## Experiment 5: Mixing Covariance and Contravariance

### Motivation

What if a class both reads and writes? Let’s test a `Processor` and see why it’s invariant by default.

### Code Example

```python
from typing import TypeVar, Generic

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

```

Save as `mixed.py`

Run `mypy`:

```
error: Incompatible types in assignment (expression has type "Processor[Cat]", variable has type "Processor[Animal]")

```

### Fix with Separation

Separate reading and writing:

```python
R = TypeVar("R", covariant=True)
W = TypeVar("W", contravariant=True)

class Reader(Generic[R]):
    def get(self) -> R:
        pass

class Writer(Generic[W]):
    def set(self, value: W) -> None:
        pass

```

Now you can use variance appropriately for each role.

---

## When to Use Each

- **Covariance**: Read-only collections (`List[Cat]` as `List[Animal]`).
- **Contravariance**: Consumers or functions taking parameters (`Consumer[Animal]` for `Consumer[Cat]`).
- **Invariance**: Mutable types or when both reading and writing occur.

| Scenario | Variance | Example |
| --- | --- | --- |
| Read-only | Covariant | `ReadOnlyList[Cat]` to `Animal` |
| Write-only | Contravariant | `Consumer[Animal]` for `Cat` |
| Read and Write | Invariant | `List[Cat]` not related to `Animal` |

---

## Conclusion

Through these experiments, you’ve seen:

- **Covariance** enables subtype flexibility for outputs.
- **Contravariance** allows supertype flexibility for inputs.
- **Invariance** protects mutable types.

Run these examples, tweak them (e.g., add methods, change variance), and check with `mypy` to deepen your understanding. For more, explore:

- [PEP 484](https://www.python.org/dev/peps/pep-0484/)
- [mypy Documentation](https://mypy.readthedocs.io/)

Happy coding, and enjoy mastering Python’s type system!
