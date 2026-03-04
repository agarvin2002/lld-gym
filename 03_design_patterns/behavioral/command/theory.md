# Command Pattern

## What is it?
Encapsulate a request as an object, letting you parameterise clients with different requests, queue or log requests, and support undoable operations.

## Real-world analogy
A restaurant order slip. The waiter (invoker) doesn't cook — they take an order slip (command) to the kitchen (receiver). The slip can be queued, cancelled, or reordered. The waiter doesn't need to know how to cook.

## Why does it matter?
Without Command, the caller directly invokes the receiver's methods — tightly coupling who asks to who does. With Command, you can: decouple senders from receivers, add undo/redo, queue operations for later execution, and log all actions.

## Python-specific notes
- Simple commands can be plain callables (lambdas or functions) — no ABC needed
- Use an ABC when you need undo/redo (`execute` + `undo` methods)
- `functools.partial` is a lightweight alternative for simple command queuing

## When to use
- You need undo/redo functionality
- You need to queue, schedule, or log operations
- You want to decouple the object that invokes an operation from the one that knows how to perform it
- Implementing macro recording or transaction logs

## When to avoid
- Simple one-off operation calls with no need for queuing or undoing
- The "command" is trivial enough that a callback/lambda suffices

## Quick example
```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...

class TextEditor:
    def __init__(self) -> None:
        self.text = ""

class InsertTextCommand(Command):
    def __init__(self, editor: TextEditor, text: str) -> None:
        self._editor = editor
        self._text = text

    def execute(self) -> None:
        self._editor.text += self._text

    def undo(self) -> None:
        self._editor.text = self._editor.text[:-len(self._text)]

class CommandHistory:
    def __init__(self) -> None:
        self._history: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo(self) -> None:
        if self._history:
            self._history.pop().undo()

# Usage
editor = TextEditor()
history = CommandHistory()

history.execute(InsertTextCommand(editor, "Hello"))
history.execute(InsertTextCommand(editor, " World"))
print(editor.text)   # Hello World

history.undo()
print(editor.text)   # Hello

history.undo()
print(editor.text)   # (empty)
```

## Common mistakes
- Putting business logic inside the command (it should just delegate to the receiver)
- Not storing enough state in the command to support undo
- Creating a Command class for trivial one-time operations (use a lambda instead)

## Links
- Exercise: `exercises/starter.py` — implement a smart home controller with undoable device commands
