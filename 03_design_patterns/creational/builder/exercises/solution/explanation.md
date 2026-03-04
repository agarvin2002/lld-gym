# Builder Pattern — Solution Explanation

## The Problem Being Solved: Telescoping Constructors

A resume has many fields — some required, most optional, two that grow as lists. Without a builder, your options are ugly:

**Telescoping constructor** (positional madness):
```python
Resume(contact, summary, experiences, skills, education)
# Which arg is which? Easy to swap two strings silently.
```

**Giant keyword-arg call** (one-liner that wraps around the screen):
```python
Resume(
    contact=ContactInfo("Alice", "alice@example.com"),
    summary="...",
    experiences=[WorkExperience("Google", "SWE", 3.0)],
    skills=["Python"],
    education="B.Sc. CS"
)
```

This works for small objects but breaks when:
- Fields are mandatory at a semantic level but can't be enforced in `__init__` because the object is assembled over several steps.
- You want reusable preset configurations (Director pattern).
- The construction process is shared across multiple call sites.

---

## Why Each Design Decision Was Made

### 1. `_contact` starts as `None`

```python
def __init__(self) -> None:
    self._contact: ContactInfo | None = None
    ...
```

`None` is a sentinel that signals "caller never provided this required field." It lets `build()` enforce the invariant cleanly:

```python
def build(self) -> Resume:
    if self._contact is None:
        raise ValueError("Contact information (name and email) is required.")
```

`build()` is the **single validation point**. Individual setters don't need to know which other setters were called. All cross-field invariants live here.

### 2. Every setter returns `self`

```python
def add_skill(self, skill: str) -> ResumeBuilder:
    self._skills.append(skill)
    return self          # <-- fluent interface
```

Returning `self` enables method chaining:
```python
resume = (ResumeBuilder()
          .contact("Alice", "alice@example.com")
          .add_skill("Python")
          .add_skill("Go")
          .build())
```

Without `return self`, every step would need its own variable assignment — noisier and harder to read.

### 3. Lists are copied in `build()` (snapshot semantics)

```python
return Resume(
    experiences=list(self._experiences),  # copy, not reference
    skills=list(self._skills),
    ...
)
```

Without copying, the caller could mutate the builder after `build()` and silently corrupt an already-built `Resume`:

```python
builder = ResumeBuilder().contact("Bob", "bob@example.com").add_skill("Python")
resume = builder.build()
builder.add_skill("Java")      # mutation after build
print(resume.skills)           # ["Python", "Java"] -- BUG without copying
```

`list(...)` creates a shallow copy, which is sufficient here because `str` is immutable and `WorkExperience` is a dataclass (value object by convention).

### 4. Instance-level list initialisation in `__init__`

```python
def __init__(self) -> None:
    self._experiences: list[WorkExperience] = []   # safe
    self._skills: list[str] = []                   # safe
```

The classic Python mutable default argument trap:
```python
# WRONG — all instances share the same list object
class ResumeBuilder:
    _skills = []          # class attribute — dangerous

# ALSO WRONG — default arg is evaluated once at function definition time
def __init__(self, skills=[]):
    self._skills = skills
```

Assigning in `__init__` creates a **new list per instance**, so two `ResumeBuilder` objects never share state.

---

## Builder vs `@dataclass` with Defaults

| Criterion | `@dataclass` | Builder |
|---|---|---|
| All fields known at call site | Good fit | Overkill |
| Optional fields with sensible defaults | Good fit | Acceptable |
| **Mandatory fields validated at build time** | Awkward | Natural fit |
| **Object assembled over multiple steps** | Awkward | Natural fit |
| **Multiple preset configurations** | Awkward | Director pattern |
| Immutable after construction | `frozen=True` | `build()` returns frozen product |

Use `@dataclass` when construction is simple and immediate. Reach for Builder when:
- Some fields are required and should be caught only at `build()` time (not at each setter call).
- The object is composed incrementally (e.g., read from a stream, form wizard, config accumulation).
- You want reusable presets without subclassing.

---

## The Director (Optional Extension)

A **Director** class wraps the builder and provides named presets:

```python
class ResumeDirector:
    def __init__(self, builder: ResumeBuilder) -> None:
        self._builder = builder

    def junior_template(self, name: str, email: str) -> Resume:
        return (self._builder
                .contact(name, email)
                .summary("Motivated junior engineer seeking first role.")
                .add_skill("Python")
                .add_skill("Git")
                .build())
```

The Director is optional — it does not change the builder's API, it just encodes common configurations so call sites don't have to repeat them.

---

## Key Takeaways

1. **Builder = separate construction from representation.** The `ResumeBuilder` knows *how* to build; `Resume` is just the result.
2. **`build()` is the single validation gate.** Never validate across fields in individual setters.
3. **Copy mutable fields in `build()`** to achieve snapshot semantics and isolation.
4. **Return `self` from every setter** to unlock fluent method chaining.
5. **Initialise lists in `__init__`**, never as class attributes or default arguments.
