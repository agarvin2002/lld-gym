# Abstraction

## What is it?

Abstraction means: **define what a class must do, but not how it does it.**

Think of an electric socket:
- Any device can plug in — phone charger, laptop, fan.
- The socket does not care which device. It just provides power.
- Each device uses that power differently.

The socket is the abstract interface. The devices are the concrete implementations.

---

## How to do it in Python

Use `ABC` (Abstract Base Class) and `@abstractmethod`:

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):   # abstract class — cannot be used directly
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass   # no code here — subclasses must write it

class RazorpayGateway(PaymentGateway):
    def pay(self, amount: float) -> str:
        return f"Paid ₹{amount} via Razorpay"

class PaytmGateway(PaymentGateway):
    def pay(self, amount: float) -> str:
        return f"Paid ₹{amount} via Paytm"

# this function works with ANY payment gateway
def checkout(gateway: PaymentGateway, amount: float) -> None:
    result = gateway.pay(amount)
    print(result)

checkout(RazorpayGateway(), 599)  # Paid ₹599 via Razorpay
checkout(PaytmGateway(), 599)     # Paid ₹599 via Paytm
```

**`ABC`** — your class inherits from this to become abstract.

**`@abstractmethod`** — marks a method that subclasses MUST implement. If they don't, Python throws an error when you try to create an object.

**Cannot create an abstract class directly:**
```python
gateway = PaymentGateway()  # TypeError! Cannot instantiate abstract class
```

---

## Real-world applications

- ABC is the foundation of clean system design in Python — used in almost every multi-class project.
- Parking lot: `abstract class ParkingSpot` → `CarSpot`, `BikeSpot`
- ATM: `abstract class ATMState` → `IdleState`, `CardInsertedState`
- `@abstractmethod` forces each subclass to implement the method — Python raises an error if they don't.

---

## The one mistake beginners make

**Creating an abstract class for only one use.**

```python
class Animal(ABC):
    @abstractmethod
    def speak(self): pass

class Dog(Animal):
    def speak(self): return "Woof"

# if you only ever have Dog, you don't need Animal at all
```

Create an ABC only when you have **two or more different implementations**.
If there is only one, just write the class directly.

---

## What to do next

1. Open `examples/example1_abc_module.py` — see a full payment gateway with two implementations
2. (Optional, advanced) `examples/example2_protocol_typing.py` — another way to define interfaces
3. Do `exercises/starter.py` — build a pluggable storage system using ABC
