# Exercise: Resume / CV Builder

## Background

A resume is a perfect candidate for the Builder pattern: it has a handful of mandatory fields (name, email), several optional sections (summary, skills, education), and a repeating section (work experiences). Constructing it with a single giant constructor call is unreadable; a builder lets callers compose a resume naturally, step by step.

---

## Your Task

Implement `ResumeBuilder` in `starter.py`. The dataclasses (`ContactInfo`, `WorkExperience`, `Resume`) are already defined — do not change them.

---

## Data Classes (already provided)

```python
@dataclass
class ContactInfo:
    name: str
    email: str
    phone: str = ""
    linkedin: str = ""

@dataclass
class WorkExperience:
    company: str
    title: str
    years: float

@dataclass
class Resume:
    contact: ContactInfo
    summary: str
    experiences: list[WorkExperience]
    skills: list[str]
    education: str
```

---

## ResumeBuilder — Methods to Implement

| Method | Signature | Description |
|---|---|---|
| `contact` | `contact(name, email, phone="", linkedin="") -> ResumeBuilder` | Set contact info. Returns `self`. |
| `summary` | `summary(text) -> ResumeBuilder` | Set the professional summary. Returns `self`. |
| `add_experience` | `add_experience(company, title, years) -> ResumeBuilder` | Append a work experience entry. Returns `self`. |
| `add_skill` | `add_skill(skill) -> ResumeBuilder` | Append a skill. Returns `self`. |
| `education` | `education(text) -> ResumeBuilder` | Set the education section. Returns `self`. |
| `build` | `build() -> Resume` | Validate and construct the Resume. Raises `ValueError` if `contact()` was never called. |

---

## Rules

1. Every setter must return `self` to support method chaining.
2. `build()` raises `ValueError` if `contact()` was never called (name and email are required).
3. `build()` should return a **snapshot** — mutating the builder after `build()` must not affect the already-built `Resume`. (Copy lists before handing them to `Resume`.)
4. Two separate `ResumeBuilder` instances must not share state (no mutable class-level defaults).

---

## Example Usage

```python
resume = (ResumeBuilder()
          .contact("Alice Smith", "alice@example.com", linkedin="linkedin.com/in/alice")
          .summary("Experienced software engineer specialising in distributed systems.")
          .add_experience("Google", "Senior SWE", 4.5)
          .add_experience("Stripe", "SWE II", 2.0)
          .add_skill("Python")
          .add_skill("System Design")
          .education("B.Sc. Computer Science, MIT, 2018")
          .build())

print(resume.contact.name)        # "Alice Smith"
print(len(resume.experiences))    # 2
print(resume.skills)              # ["Python", "System Design"]
```

---

## Error Case

```python
builder = ResumeBuilder()
builder.build()   # raises ValueError — contact() was never called
```

---

## Hints

- Initialise `_contact` to `None` in `__init__` and check for `None` in `build()`.
- Initialise `_experiences` and `_skills` to `[]` in `__init__` (instance-level, not class-level).
- In `build()`, pass `list(self._experiences)` and `list(self._skills)` to avoid sharing references.
