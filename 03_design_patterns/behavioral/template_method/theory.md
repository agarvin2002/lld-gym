# Template Method Pattern

## What is it?
A base class defines the skeleton of an algorithm — the fixed sequence of steps.
Subclasses fill in what each step does, but they never change the order.
The base class calls the subclass methods ("don't call us, we'll call you").

## Analogy
A Zomato restaurant onboarding checklist: verify_documents → upload_menu →
set_delivery_radius → activate_listing. Every restaurant follows the same
steps in the same order. Only the content of each step differs per restaurant.

## Minimal code
```python
from abc import ABC, abstractmethod

class ReportGenerator(ABC):
    def generate(self, data: list) -> str:   # template method — fixed order
        parts = [self.format_header()]
        for row in data:
            parts.append(self.format_row(row))
        parts.append(self.format_footer(len(data)))
        return "".join(parts)

    @abstractmethod
    def format_header(self) -> str: ...

    @abstractmethod
    def format_row(self, row) -> str: ...

    @abstractmethod
    def format_footer(self, total: int) -> str: ...

class CSVReport(ReportGenerator):
    def format_header(self) -> str:      return "Name,Price\n"
    def format_row(self, row) -> str:    return f"{row['name']},{row['price']}\n"
    def format_footer(self, n) -> str:   return f"Total: {n}\n"
```

## Real-world uses
- ETL pipelines: connect → extract → validate → transform → load (steps vary per data source)
- Logging frameworks: every handler runs filter → format → emit (only `emit` differs)
- Game engines: every turn runs validate_move → execute → check_end (rules differ per game)

## One mistake
Overriding the template method itself in a subclass. `generate()` is the part
that must not change. If a subclass redefines it, the fixed ordering guarantee
is lost and the pattern breaks.

## What to do next
See `examples/example1_data_pipeline.py` for an ETL pipeline and
`examples/example2_game_turn.py` for a turn-based game engine.
Then try `exercises/starter.py` — build CSV, HTML, and Markdown report generators.
