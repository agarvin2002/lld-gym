# Solution Explanation: Product and ShoppingCart

## Design Decisions

### 1. Why SKU is the Identity for Product

The most important design decision in this exercise is: **what makes two `Product` instances "the same"?**

We chose SKU (Stock Keeping Unit) over name or price, and this choice matters:

- **Name can change**: A product renamed from "Laptop Pro v1" to "Laptop Pro v2" is still the same product. Using name for equality would break things when products are renamed.
- **Price can change**: Discounts, promotions, and repricing happen constantly. A product with a different price tag is still the same product.
- **SKU is the stable, unique identifier**: This is how real e-commerce systems work. The SKU is chosen precisely because it is permanent and unique.

This choice directly affects `__eq__` and `__hash__`. Both are implemented using `sku` only:

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, Product):
        return NotImplemented
    return self.sku == other.sku

def __hash__(self) -> int:
    return hash(self.sku)
```

**Practical consequence**: If you add a product to the cart, then apply a discount to it, the product is still in the cart and the cart's `get_total()` correctly picks up the new price:

```python
laptop = Product("Laptop", 1000.0, 5, "SKU-001")
cart.add_item(laptop)
laptop.apply_discount(10)  # price is now 900.0
print(cart.get_total())    # 900.0 — correct, because cart holds a reference to the object
```

### 2. Why `__repr__` Matters for Debugging

Consider what happens when a test fails and you get output like this:

```
AssertionError: assert <starter.Product object at 0x10a2f3c10> == <starter.Product object at 0x10a2f4d20>
```

That tells you nothing. Compare with:

```
AssertionError: assert Product(name='Laptop Pro', price=999.99, quantity=10, sku='SKU-001') == Product(name='Mouse', price=29.99, quantity=5, sku='SKU-002')
```

Now you immediately see the problem. This is why `__repr__` is the single most important dunder to define. Make it show everything needed to understand the object's current state.

The convention is: `repr` output should ideally be valid Python that reconstructs the object. When that's not practical, at minimum show all significant fields.

### 3. Why `dict` for the Cart's Internal Storage

The `ShoppingCart` uses `dict[Product, int]` to track items. The alternatives were:

- **`list[tuple[Product, int]]`**: Adding the same product again requires a linear scan to find it (O(n)). Removing requires finding and rebuilding the list.
- **`dict[str, tuple[Product, int]]` (keyed by SKU)**: Works, but redundant — we already have the product as a hashable key.
- **`dict[Product, int]`**: O(1) lookup, add, and remove. Clean and simple.

The dict approach works *because* `Product` defines `__hash__` and `__eq__`. Without those, you couldn't use a `Product` as a dict key.

```python
# This line in add_item is elegant precisely because of __hash__ and __eq__:
self._items[product] = self._items.get(product, 0) + quantity
```

### 4. Defensive Copying in `get_items()`

```python
def get_items(self) -> dict[Product, int]:
    return dict(self._items)  # return a copy, not the internal dict
```

If `get_items()` returned `self._items` directly, a caller could do:

```python
items = cart.get_items()
items.clear()  # oops — this would empty the actual cart!
```

By returning a copy, we ensure the cart's internal state can only be modified through the cart's own methods. This is **encapsulation** at work: the cart controls how its state changes.

Note: this is a shallow copy — the `Product` objects in the dict are the same objects (same references). That's fine here because we want changes to a `Product` (like a discount) to be reflected when the cart recalculates totals.

### 5. `fail_fast` Validation Pattern

Every public method validates its inputs at the very top, before doing anything else:

```python
def add_item(self, product: Product, quantity: int = 1) -> None:
    if quantity < 1:
        raise ValueError(f"Quantity must be at least 1, got {quantity}.")
    # ... rest of the method
```

This pattern ensures:
- The error is raised with a helpful message at the point of the mistake
- The object's state is never partially modified before an error
- Callers get immediate feedback instead of confusing errors downstream

### 6. Patterns Applied (Even Implicitly)

Even though this exercise doesn't explicitly introduce design patterns, you applied several:

**Value Object (implicit)**: `Product` could be considered a value object — its identity is based on its data (SKU), not its memory address. This is why `__eq__` is based on SKU and two different `Product` instances with the same SKU are considered equal.

**Immutable Identity Fields**: The SKU should never change after creation. In a production system, you might enforce this with a property that has no setter. For this exercise, we trust callers not to change `sku` directly.

**Aggregate Root**: The `ShoppingCart` is an "aggregate" in Domain-Driven Design terms — it controls access to the `Product` items it contains. You can only add or remove whole products through the cart's methods, not by directly mutating `_items`.

## Summary of Key Takeaways

| Concept | Where Applied |
|---------|--------------|
| `__repr__` for debugging | Both `Product` and `ShoppingCart` |
| `__eq__` on stable identity | `Product.__eq__` uses `sku` |
| `__hash__` consistency | `Product.__hash__` uses `sku` to match `__eq__` |
| `__len__` and `__contains__` | Make `ShoppingCart` feel like a Python collection |
| Input validation in `__init__` | `Product.__init__` — fail fast, fail clearly |
| Defensive copying | `ShoppingCart.get_items()` returns a copy |
| `dict.get(key, default)` | Elegant accumulation in `add_item` |
