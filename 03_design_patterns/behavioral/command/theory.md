# Command Pattern

## What is it?
The Command pattern wraps an action inside an object. The object stores everything needed to perform (and undo) the action. The caller just calls `execute()` without knowing the details.

## Analogy
A Zomato order. You (the invoker) place an order slip with the restaurant (receiver). The slip can be queued, cancelled, or replayed. You never walk into the kitchen yourself.

## Minimal code
```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...

class Document:
    def __init__(self): self.text = ""

class InsertCommand(Command):
    def __init__(self, doc: Document, text: str):
        self._doc, self._text = doc, text

    def execute(self) -> None:
        self._doc.text += self._text

    def undo(self) -> None:
        self._doc.text = self._doc.text[:-len(self._text)]

doc = Document()
history = []
cmd = InsertCommand(doc, "Hello")
cmd.execute(); history.append(cmd)
print(doc.text)   # Hello
history.pop().undo()
print(doc.text)   # (empty)
```

## Real-world uses
- Text editors — every keystroke is a command; Ctrl+Z pops the stack
- Razorpay payment gateway — each charge/refund is a logged command object
- Game engines — player actions are queued and replayed for netcode
- Smart home scenes — "Movie Mode" is a MacroCommand: one click runs Dim Lights + Start TV + Lower Blinds as a single undoable unit

## One mistake
Putting business logic inside the command class. The command should only delegate to the receiver, not do the work itself. If your `execute()` is longer than 5 lines, move the logic to the receiver.

## What to do next
See `examples/example1_text_editor.py` for a full undo/redo text editor.
See `examples/example2_smart_home.py` for macro commands (composite commands).
Then try `exercises/starter.py` — build a drawing canvas with undo/redo.
