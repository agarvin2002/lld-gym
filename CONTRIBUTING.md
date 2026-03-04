# Contributing to Python LLD Masterclass

Thank you for your interest in contributing! This project aims to be the best free LLD learning resource for Python developers.

## Ways to Contribute

- Fix typos or improve explanations in `theory.md` files
- Add or improve code examples
- Submit new exercises
- Add new LLD problems
- Improve test coverage
- Report bugs or unclear content

## How to Contribute

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/improve-parking-lot`
3. **Make your changes**
4. **Run tests**: `pytest` — all tests must pass
5. **Open a Pull Request** with a clear description

## Standards

### Code
- Python 3.10+
- Type hints on all function signatures
- Docstrings on all public classes and methods
- No external dependencies (only stdlib + pytest)

### theory.md
- Follow the template: What / Analogy / Why / Python notes / When to use / Example / Mistakes
- Keep it concise — learners should finish a topic in under 15 minutes

### Exercises
- `starter.py` must have class stubs with clear TODOs
- Tests must be descriptive (`test_park_returns_ticket_when_spot_available`)
- Solutions must include `explanation.md`

### LLD Problems
- `problem.md` must include clarifying questions
- `design.md` must include ASCII class diagram
- Tests must cover: basic → extended → edge cases

## Code of Conduct

Be respectful and constructive. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
