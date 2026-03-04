"""
State Pattern — Example 2: Document Approval Workflow (State objects)
=====================================================================
Each state is a class. State-specific behaviour is encapsulated per state.
Use this approach when states have complex, diverging behaviour.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class DocumentState(ABC):
    @abstractmethod
    def submit(self, doc: "Document") -> None: ...
    @abstractmethod
    def approve(self, doc: "Document") -> None: ...
    @abstractmethod
    def reject(self, doc: "Document") -> None: ...
    @abstractmethod
    def name(self) -> str: ...


class DraftState(DocumentState):
    def submit(self, doc: "Document") -> None:
        print("Document submitted for review.")
        doc.state = PendingReviewState()

    def approve(self, doc: "Document") -> None:
        print("ERROR: Cannot approve a draft — submit it first.")

    def reject(self, doc: "Document") -> None:
        print("ERROR: Cannot reject a draft — submit it first.")

    def name(self) -> str:
        return "DRAFT"


class PendingReviewState(DocumentState):
    def submit(self, doc: "Document") -> None:
        print("ERROR: Already under review.")

    def approve(self, doc: "Document") -> None:
        print("Document approved and published.")
        doc.state = PublishedState()

    def reject(self, doc: "Document") -> None:
        print("Document rejected. Returned to author.")
        doc.state = RejectedState()

    def name(self) -> str:
        return "PENDING_REVIEW"


class PublishedState(DocumentState):
    def submit(self, doc: "Document") -> None:
        print("ERROR: Document is already published.")

    def approve(self, doc: "Document") -> None:
        print("ERROR: Already published.")

    def reject(self, doc: "Document") -> None:
        print("ERROR: Cannot reject a published document.")

    def name(self) -> str:
        return "PUBLISHED"


class RejectedState(DocumentState):
    def submit(self, doc: "Document") -> None:
        print("Re-submitting rejected document for review.")
        doc.state = PendingReviewState()

    def approve(self, doc: "Document") -> None:
        print("ERROR: Cannot approve a rejected document.")

    def reject(self, doc: "Document") -> None:
        print("ERROR: Already rejected.")

    def name(self) -> str:
        return "REJECTED"


class Document:
    def __init__(self, title: str) -> None:
        self.title = title
        self.state: DocumentState = DraftState()

    def submit(self) -> None:
        self.state.submit(self)

    def approve(self) -> None:
        self.state.approve(self)

    def reject(self) -> None:
        self.state.reject(self)

    def status(self) -> str:
        return self.state.name()


if __name__ == "__main__":
    doc = Document("Q4 Report")
    print(f"Status: {doc.status()}")
    doc.approve()          # Error — can't approve a draft
    doc.submit()
    print(f"Status: {doc.status()}")
    doc.reject()
    print(f"Status: {doc.status()}")
    doc.submit()           # Re-submit after rejection
    doc.approve()
    print(f"Status: {doc.status()}")
