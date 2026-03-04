"""
LSP Example 2: Correct Animal Hierarchy

Shows how to design a hierarchy where every subtype is truly substitutable.
Avoids the classic "Penguin can't fly" trap.
"""
from abc import ABC, abstractmethod


class Animal(ABC):
    """Every animal can eat and breathe. Only these in the base."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def eat(self) -> str: ...

    def breathe(self) -> str:
        return f"{self.name} breathes air"


class FlyingAnimal(Animal, ABC):
    """Only for animals that actually fly."""

    @abstractmethod
    def fly(self) -> str: ...


class SwimmingAnimal(Animal, ABC):
    """Only for animals that actually swim."""

    @abstractmethod
    def swim(self) -> str: ...


# ─── Concrete Animals ─────────────────────────────────────────────

class Dog(Animal):
    def eat(self) -> str:
        return f"{self.name} eats dog food"

    def run(self) -> str:
        return f"{self.name} runs"
    # No fly(), no swim() forced — Dog doesn't need them ✅


class Eagle(FlyingAnimal):
    def eat(self) -> str:
        return f"{self.name} catches prey"

    def fly(self) -> str:
        return f"{self.name} soars at 150km/h"


class Fish(SwimmingAnimal):
    def eat(self) -> str:
        return f"{self.name} eats plankton"

    def swim(self) -> str:
        return f"{self.name} swims upstream"
    # No fly() forced — Fish doesn't need it ✅


class Duck(FlyingAnimal, SwimmingAnimal):
    """Duck can both fly and swim — correctly implements both interfaces."""

    def eat(self) -> str:
        return f"{self.name} eats bread"

    def fly(self) -> str:
        return f"{self.name} flies south for winter"

    def swim(self) -> str:
        return f"{self.name} paddles on the pond"


# ─── Functions that use correct interface ─────────────────────────

def make_animal_eat(animal: Animal) -> None:
    """Works with ANY Animal — Dog, Eagle, Fish, Duck."""
    print(animal.eat())


def make_fly(flyer: FlyingAnimal) -> None:
    """Only called with things that actually fly."""
    print(flyer.fly())


def make_swim(swimmer: SwimmingAnimal) -> None:
    """Only called with things that actually swim."""
    print(swimmer.swim())


if __name__ == "__main__":
    dog = Dog("Rex")
    eagle = Eagle("Sam")
    fish = Fish("Nemo")
    duck = Duck("Donald")

    print("=== All animals eat (substitution works) ===")
    for animal in [dog, eagle, fish, duck]:
        make_animal_eat(animal)

    print("\n=== Flying animals ===")
    for flyer in [eagle, duck]:
        make_fly(flyer)

    print("\n=== Swimming animals ===")
    for swimmer in [fish, duck]:
        make_swim(swimmer)

    print("\n=== No forced empty methods ===")
    print("Dog doesn't have fly() or swim() — no NotImplementedError traps ✅")
