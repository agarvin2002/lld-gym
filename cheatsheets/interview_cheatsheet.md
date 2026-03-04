# Interview Cheatsheet

## The 6-Step Framework

| Step | What to Do | Time |
|------|-----------|------|
| 1. Clarify | Ask 3-5 questions about scope, scale, constraints | 3-5 min |
| 2. Identify Entities | List nouns → classes | 2-3 min |
| 3. Define Relationships | is-a, has-a, uses | 2-3 min |
| 4. Design Interfaces | ABCs before implementations | 3-5 min |
| 5. Implement | Start simple, add complexity | 15-20 min |
| 6. Discuss Extensions | Patterns used, trade-offs, what you'd add | 3-5 min |

---

## Clarifying Questions Template

```
1. Scale: "How many X can there be at once?"
2. Operations: "What are the core operations?"
3. Constraints: "Any specific rules or edge cases?"
4. Scope: "Do we need [auth / persistence / UI]?"
5. Non-functional: "Any thread safety or performance requirements?"
```

---

## Entities Checklist

When reading the problem, underline **nouns**:
- Each significant noun = potential class
- Actions on nouns = methods
- Adjectives = properties

Example: "A **parking lot** with multiple **floors**. **Vehicles** of type **car**, **truck**, **motorcycle** can park in **spots**."

Classes: `ParkingLot`, `Floor`, `Vehicle`, `Car`, `Truck`, `Motorcycle`, `ParkingSpot`

---

## Relationships Cheatsheet

| Relationship | Meaning | Python |
|-------------|---------|--------|
| **is-a** | Inheritance | `class Car(Vehicle):` |
| **has-a** | Composition | `self.engine = Engine()` |
| **uses** | Dependency | Method parameter |
| **creates** | Factory | `VehicleFactory.create()` |
| **observes** | Observer | `stock.subscribe(display)` |

---

## Top 5 Patterns to Know Cold

1. **Strategy**: "I need to swap algorithms at runtime"
   → `class Context: def __init__(self, strategy: Strategy)`

2. **Observer**: "Multiple things need to react to state changes"
   → `subscribe(handler)`, `notify(event, data)`

3. **State**: "Behavior depends on current state"
   → Enum states + guard: `if state != EXPECTED: raise InvalidStateError`

4. **Factory**: "I create different objects based on a type/config"
   → `dict[type, class]` registry pattern

5. **Singleton**: "There should only be one instance"
   → Module-level or `__new__` with class variable

---

## Things to Say Out Loud

**During clarification:**
- "Before I start, I want to make sure I understand the scope..."
- "I'll assume X for now — is that correct?"

**During design:**
- "I'm going to identify the main entities first..."
- "This relationship is has-a because..."
- "I'll use [Pattern] here because..."

**During implementation:**
- "I'll start with the core functionality and we can extend it..."
- "I'm using [ABC / dataclass / enum] because..."
- "This could be a race condition — should I add thread safety?"

**During review:**
- "To extend this, we could..."
- "The trade-off here is..."
- "I'd also want to add error handling for..."

---

## Red Flags to Avoid

❌ Starting to code before clarifying requirements
❌ God class (one class doing everything)
❌ Hard-coding strings instead of Enums
❌ No separation between business logic and data storage
❌ Forgetting to mention thread safety when relevant
❌ Naming patterns without explaining why you chose them

---

## Green Flags Interviewers Love

✅ "Let me identify the main entities first"
✅ Clear, self-documenting names (`ParkingSpot` not `PS`)
✅ Enums for finite value sets
✅ ABC/interfaces before implementations
✅ Mentioning SOLID violations you're avoiding
✅ Asking follow-up questions before diving in
✅ "I'd make this thread-safe by adding a Lock here"
