"""Command Pattern — Example 1: Text Editor with Undo/Redo.

The Command pattern wraps each action as an object, enabling undo/redo,
queuing, and logging without the caller knowing the details of each action.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


# ── Command Interface ─────────────────────────────────────────────────────────

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


# ── Receiver ──────────────────────────────────────────────────────────────────

class Document:
    """The object being modified — knows nothing about commands."""
    def __init__(self) -> None:
        self._text = ""

    def insert(self, position: int, text: str) -> None:
        self._text = self._text[:position] + text + self._text[position:]

    def delete(self, position: int, length: int) -> None:
        self._text = self._text[:position] + self._text[position + length:]

    @property
    def text(self) -> str:
        return self._text

    def __repr__(self) -> str:
        return f"Document({self._text!r})"


# ── Concrete Commands ─────────────────────────────────────────────────────────

class InsertCommand(Command):
    def __init__(self, doc: Document, position: int, text: str) -> None:
        self._doc = doc
        self._position = position
        self._text = text

    def execute(self) -> None:
        self._doc.insert(self._position, self._text)

    def undo(self) -> None:
        # Undo insert = delete the same span
        self._doc.delete(self._position, len(self._text))


class DeleteCommand(Command):
    def __init__(self, doc: Document, position: int, length: int) -> None:
        self._doc = doc
        self._position = position
        self._length = length
        self._deleted: str = ""  # captured on execute() for undo

    def execute(self) -> None:
        # Capture the deleted text before removing it
        self._deleted = self._doc.text[self._position:self._position + self._length]
        self._doc.delete(self._position, self._length)

    def undo(self) -> None:
        # Undo delete = re-insert the captured text
        self._doc.insert(self._position, self._deleted)


# ── Invoker ───────────────────────────────────────────────────────────────────

class TextEditor:
    """Invoker: holds the undo/redo stacks and dispatches commands."""
    def __init__(self, doc: Document) -> None:
        self._doc = doc
        self._undo_stack: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()  # new action invalidates redo history

    def undo(self) -> None:
        if not self._undo_stack:
            print("Nothing to undo.")
            return
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self) -> None:
        if not self._redo_stack:
            print("Nothing to redo.")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)

    @property
    def text(self) -> str:
        return self._doc.text


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    doc = Document()
    editor = TextEditor(doc)

    editor.execute(InsertCommand(doc, 0, "Hello"))
    print(editor.text)          # Hello

    editor.execute(InsertCommand(doc, 5, ", World"))
    print(editor.text)          # Hello, World

    editor.execute(DeleteCommand(doc, 5, 7))
    print(editor.text)          # Hello

    editor.undo()
    print(editor.text)          # Hello, World  (delete undone)

    editor.undo()
    print(editor.text)          # Hello          (second insert undone)

    editor.redo()
    print(editor.text)          # Hello, World  (redo)
