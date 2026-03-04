# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Setup
```bash
python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest pytest-cov -q
```
`pytest` is not installed system-wide; always use the venv. The venv at `/tmp/lld_venv` is ephemeral — recreate it if missing.

### Running Tests

```bash
# Full module
/tmp/lld_venv/bin/pytest 01_oop_foundations/ -q
/tmp/lld_venv/bin/pytest 04_lld_problems/ -q

# Single exercise test file
/tmp/lld_venv/bin/pytest 01_oop_foundations/02_encapsulation/exercises/tests.py -v

# Single LLD problem (level by level — this is the intended learner flow)
/tmp/lld_venv/bin/pytest 04_lld_problems/01_parking_lot/tests/test_basic.py -v
/tmp/lld_venv/bin/pytest 04_lld_problems/01_parking_lot/tests/test_extended.py -v
/tmp/lld_venv/bin/pytest 04_lld_problems/01_parking_lot/tests/test_edge.py -v

# Single test by name
/tmp/lld_venv/bin/pytest 04_lld_problems/03_atm_system/tests/test_basic.py::TestATMStates::test_atm_starts_in_idle_state -v
```

`pytest.ini` (root-level) configures `--import-mode=importlib` and discovers both `tests.py` and `test_*.py` filenames.

### Running Examples
```bash
python 01_oop_foundations/01_classes_and_objects/examples/example1_basic_class.py
```

### Verifying a solution passes all tests
Temporarily copy the solution over starter, run tests, restore:
```bash
cp 04_lld_problems/01_parking_lot/solution/solution.py 04_lld_problems/01_parking_lot/starter.py.bak
cp 04_lld_problems/01_parking_lot/solution/solution.py 04_lld_problems/01_parking_lot/starter.py
/tmp/lld_venv/bin/pytest 04_lld_problems/01_parking_lot/ -q
mv 04_lld_problems/01_parking_lot/starter.py.bak 04_lld_problems/01_parking_lot/starter.py
```

---

## Architecture

### Project Purpose
A stub-based, test-driven LLD learning resource. Learners edit `starter.py`, run tests to get pass/fail feedback, and only look at `solution/` after attempting the problem.

### Module Layout
```
01_oop_foundations/     — 5 OOP topics (complete)
02_solid_principles/    — 5 SOLID principles (complete)
03_design_patterns/     — 13 patterns in creational/structural/behavioral/ (partially complete)
04_lld_problems/        — 15 FAANG problems (7 complete with solutions, 8 stubs only)
05_concurrency/         — threading theory + examples (exercises incomplete)
cheatsheets/            — 4 quick-reference markdown files
interview_guide/        — 3-file interview strategy guide
```

### Per-Topic File Convention (OOP / SOLID / Patterns)
```
topic/
├── theory.md
├── examples/example1_*.py, example2_*.py
└── exercises/
    ├── starter.py      ← learner edits this
    ├── tests.py        ← pytest tests (auto-discovered via pytest.ini)
    └── solution/
        ├── solution.py
        └── explanation.md
```

### Per-LLD-Problem File Convention
```
problem_name/
├── problem.md
├── design.md           (not always present)
├── starter.py          ← learner edits this
├── tests/
│   ├── test_basic.py   ← happy path
│   ├── test_extended.py← additional features
│   └── test_edge.py    ← edge cases + concurrency
└── solution/
    ├── solution.py
    └── explanation.md
```

### Critical: Test Import Pattern
All `tests.py` / `test_*.py` files share the module name `starter`, which causes `sys.modules` cache collisions when pytest collects tests across directories. The fix, required in **every** test file, is:

**For OOP/SOLID/Pattern exercises** (tests.py next to starter.py):
```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import Foo, Bar
```

**For LLD problems** (tests/ one level below starter.py):
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import Foo, Bar
```

**Never** add `from starter import X` inside a test function — always at module level, so the path setup runs at collection time.

### Completion Status

**Modules 01–02** (OOP + SOLID): Fully complete. 212 tests pass against solutions.

**Module 03** (Design Patterns): 4 patterns fully built (singleton, adapter, decorator, observer); only `theory.md` exists for the rest (factory); exercises directories exist but are empty for all others.

**Module 04** (LLD Problems): 7 problems have full solutions + 3-tier tests:
- `01_parking_lot`, `02_elevator_system`, `03_atm_system`, `04_library_management`, `05_hotel_booking` (basic tests only), `08_food_delivery`, `12_lru_cache`

Problems that exist as stubs only (no tests, no solution):
- `06_movie_ticket_booking`, `07_ride_sharing`, `09_chess`, `10_snake_and_ladders`, `11_rate_limiter`, `13_pub_sub_system`, `14_logging_framework`, `15_vending_machine`

**Module 05** (Concurrency): Theory + examples for threading basics only; all exercises incomplete.

### Solution Quality Standard
Solutions use: `ABC` + `@abstractmethod`, `@dataclass`/`@property`, `threading.Lock` for concurrency, `uuid.uuid4()` for IDs, `Enum` for state/category, Strategy pattern for swappable algorithms. See `04_lld_problems/01_parking_lot/solution/solution.py` or `03_atm_system/solution/solution.py` as reference examples.

### Contribution Standards
- **Python 3.10+** required; type hints on all function signatures, docstrings on all public classes/methods.
- **No external dependencies** — stdlib + pytest only.
- `starter.py` must have class stubs with clear `# TODO:` comments.
- `theory.md` template: What → Analogy → Why → Python notes → When to use → Example → Common mistakes.
- `problem.md` must include clarifying questions; `design.md` must include an ASCII class diagram.
- Test names must be descriptive (e.g. `test_park_returns_ticket_when_spot_available`).
