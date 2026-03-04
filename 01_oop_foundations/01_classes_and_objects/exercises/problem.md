# Exercise 01: Product and ShoppingCart

## Overview

You will build two classes — `Product` and `ShoppingCart` — that model a simple e-commerce shopping system. This exercise reinforces all the core class concepts from the theory: `__init__` with validation, instance methods, `__repr__`, `__eq__`, and `__hash__`.

---

## What You'll Practice

- Defining classes with multiple attributes and type hints
- Validating inputs in `__init__` to ensure objects are always in a valid state
- Writing instance methods that read and modify object state
- Implementing `__repr__` so objects are easy to inspect in a debugger or REPL
- Implementing `__eq__` and `__hash__` so objects behave correctly in sets and dicts
- Designing a container class (`ShoppingCart`) that manages a collection of other objects

---

## The Task

### Class 1: `Product`

A `Product` represents an item available for purchase.

**Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Human-readable product name. Must be a non-empty string. |
| `price` | `float` | Unit price in dollars. Must be strictly positive (`> 0`). |
| `quantity` | `int` | Number of units in stock. Must be `>= 0`. |
| `sku` | `str` | Stock Keeping Unit — unique identifier. Must be a non-empty string. |

**Methods to implement:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(name, price, quantity, sku)` | Initialize and validate all attributes. |
| `__repr__` | `() -> str` | Return a developer-friendly string. |
| `__str__` | `() -> str` | Return a human-readable string. |
| `__eq__` | `(other) -> bool` | Two products are equal if they share the same `sku`. |
| `__hash__` | `() -> int` | Hash based on `sku`. |
| `is_in_stock` | `() -> bool` | Return `True` if `quantity > 0`. |
| `apply_discount` | `(percent: float) -> None` | Reduce price by `percent`%. E.g., `apply_discount(10)` makes a $100 item $90. Must raise `ValueError` if percent is not in range (0, 100]. |

**Constraints:**
- `price` must be `> 0` — raise `ValueError` with a descriptive message if not
- `quantity` must be `>= 0` — raise `ValueError` if not
- `name` and `sku` must be non-empty strings — raise `ValueError` if not
- `__eq__` must use `sku` as the identity (not name or price, which can change)

---

### Class 2: `ShoppingCart`

A `ShoppingCart` holds a collection of `Product` objects and provides operations to manage them.

**Attributes (internal):**
- `_items`: a dict mapping `Product` → quantity added to cart (not the product's stock quantity, but how many the customer wants to buy)

**Methods to implement:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `()` | Initialize an empty cart. |
| `add_item` | `(product: Product, quantity: int = 1) -> None` | Add `quantity` units of `product` to the cart. If the product is already in the cart, increase its cart quantity. `quantity` must be `>= 1`. |
| `remove_item` | `(product: Product) -> None` | Remove the product entirely from the cart. Raise `ValueError` if the product is not in the cart. |
| `get_total` | `() -> float` | Return the total price of all items in the cart (`sum of price * cart_quantity for each product`). |
| `get_item_count` | `() -> int` | Return the total number of individual units in the cart (sum of cart quantities). |
| `is_empty` | `() -> bool` | Return `True` if the cart has no items. |
| `get_items` | `() -> dict` | Return a copy of the internal items dict (Product → quantity). |
| `__repr__` | `() -> str` | Show number of distinct products and total. |
| `__len__` | `() -> int` | Return `get_item_count()` (enables `len(cart)`). |
| `__contains__` | `(product: Product) -> bool` | Return `True` if the product is in the cart (enables `product in cart`). |

**Constraints:**
- `quantity` in `add_item` must be `>= 1` — raise `ValueError` if not
- `remove_item` must raise `ValueError` if the product is not found
- The internal `_items` dict must not be exposed directly — `get_items()` returns a copy

---

## Example Usage

```python
laptop = Product("Laptop Pro", 999.99, 10, "SKU-LAPTOP-001")
mouse = Product("Wireless Mouse", 29.99, 50, "SKU-MOUSE-001")
keyboard = Product("Mechanical Keyboard", 79.99, 25, "SKU-KB-001")

cart = ShoppingCart()
print(cart.is_empty())     # True

cart.add_item(laptop, 1)
cart.add_item(mouse, 2)
cart.add_item(keyboard, 1)

print(len(cart))           # 4 (1 laptop + 2 mice + 1 keyboard)
print(cart.get_total())    # 1139.96 (999.99 + 59.98 + 79.99)
print(laptop in cart)      # True

cart.remove_item(mouse)
print(cart.get_item_count())  # 2

laptop.apply_discount(10)
print(laptop.price)        # 899.991 (or rounded — your choice)
```

---

## Hints

1. **Use a `dict` for `_items`**: `{product: quantity}`. Products are hashable because you'll implement `__hash__`, so they can be dict keys.

2. **`get_total` is a simple loop**: iterate over `self._items.items()`, multiply `product.price * quantity`, and sum them up.

3. **`__contains__` is just a key lookup**: `return product in self._items`.

4. **For `apply_discount`**: calculate the discount amount and subtract. Check that percent is in `(0, 100]` first.

5. **`get_items()` should return a copy**: `return dict(self._items)` — this prevents callers from mutating the internal state.

6. **Remember**: `_items` uses `Product` objects as keys. This works because `Product.__hash__` is defined. If you forget `__hash__`, you'll get a `TypeError`.

7. **`add_item` with existing product**: use `self._items.get(product, 0)` to get the current quantity, then add to it.

---

## Files

| File | Purpose |
|------|---------|
| `starter.py` | Skeleton code with TODOs — fill this in |
| `tests.py` | Run with `pytest tests.py -v` to check your work |
| `solution/solution.py` | Reference implementation (read AFTER attempting) |
| `solution/explanation.md` | Design reasoning (read after solution) |

---

## Running the Tests

```bash
# From the exercises directory
pytest tests.py -v

# Run a single test
pytest tests.py::test_product_creation_with_valid_data -v

# Run with short traceback on failure
pytest tests.py -v --tb=short
```

All 9 tests should pass when your implementation is complete.
