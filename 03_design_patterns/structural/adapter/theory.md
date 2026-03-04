# Adapter Pattern

## 1. What Is It?

The Adapter pattern converts the interface of a class into another interface that clients expect. It allows classes to work together that otherwise couldn't because of incompatible interfaces.

In short: **wrap an incompatible object so it looks compatible to the caller.**

---

## 2. Analogy: Power Adapter

When you travel from the US to Europe, your US plug doesn't fit European sockets. A power adapter sits between your US device and the European socket — it doesn't change what your device does, it just makes the connection possible.

- **Client**: your laptop
- **Target Interface**: European socket (what the client expects)
- **Adaptee**: US plug / your device
- **Adapter**: the physical power adapter

---

## 3. Use Cases

- Integrating third-party libraries whose interface you can't change
- Working with legacy code that would be too risky to modify
- Unifying multiple APIs that serve the same purpose (e.g., multiple payment gateways)
- Connecting new code to old systems during a gradual migration

---

## 4. Object Adapter vs Class Adapter

### Object Adapter (Composition — Preferred)
The adapter holds a reference to the adaptee and delegates calls.

```python
class Adapter(Target):
    def __init__(self, adaptee: Adaptee):
        self._adaptee = adaptee

    def request(self) -> str:
        return self._adaptee.specific_request()
```

**Pros**: Works even if adaptee is not subclassable; can adapt multiple adaptees.

### Class Adapter (Multiple Inheritance)
The adapter inherits from both the target interface and the adaptee.

```python
class Adapter(Target, Adaptee):
    def request(self) -> str:
        return self.specific_request()
```

**Pros**: No additional object needed; can override adaptee behavior.
**Cons**: Tighter coupling; Python multiple inheritance can cause MRO issues; not available in languages without multiple inheritance.

**Python allows both**, but object adapter via composition is almost always preferred.

---

## 5. Quick Example: Payment API Adapter

```python
# Legacy payment system (cannot modify)
class LegacyPaymentAPI:
    def make_payment(self, card_num: str, amount_cents: int, cvv: str) -> bool:
        print(f"Legacy: charging {amount_cents} cents to card ending {card_num[-4:]}")
        return True

# New interface the rest of your app expects
class PaymentGateway:
    def charge(self, amount_usd: float, card_details: dict) -> bool:
        raise NotImplementedError

# Adapter bridges old to new
class LegacyPaymentAdapter(PaymentGateway):
    def __init__(self, legacy_api: LegacyPaymentAPI):
        self._api = legacy_api

    def charge(self, amount_usd: float, card_details: dict) -> bool:
        amount_cents = int(amount_usd * 100)
        return self._api.make_payment(
            card_details["number"],
            amount_cents,
            card_details["cvv"]
        )

# Client code only knows about PaymentGateway
gateway = LegacyPaymentAdapter(LegacyPaymentAPI())
gateway.charge(29.99, {"number": "4111111111111111", "cvv": "123"})
```

---

## 6. Structure (UML)

```
Client  -->  Target Interface
                   ^
                   |
              Adapter
                   |  (wraps)
              Adaptee
```

---

## 7. When NOT to Use

- When you control the adaptee and can simply change its interface
- When the two interfaces are so different that the adapter becomes a full re-implementation
- When you're adding adapters on top of adapters — this signals a deeper design problem
- When a simple function or lambda can bridge the gap without a full class
