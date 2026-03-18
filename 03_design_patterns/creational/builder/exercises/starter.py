"""
WHAT YOU'RE BUILDING
=====================
A Resume builder that constructs a Resume object step by step.

A resume has:
  - contact info (name, email; optionally phone and LinkedIn)
  - a summary paragraph
  - a list of work experiences (company, title, years)
  - a list of skills
  - an education line

You'll implement ResumeBuilder — a fluent builder where every setter returns
self so calls can be chained. build() is the only place where the Resume is
created, and it must raise ValueError if contact info was never set.

Data classes (ContactInfo, WorkExperience, Resume) are provided — do not modify them.
"""

from __future__ import annotations
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data classes — do not modify
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class ResumeBuilder:
    """
    Fluent builder that assembles a Resume step by step.

    All setter methods return self to support method chaining.
    build() is the single validation + construction point.
    """

    def __init__(self) -> None:
        # TODO: Initialise all private fields.
        # _contact starts as None — build() checks for it.
        # _experiences and _skills start as empty lists.
        self._contact: ContactInfo | None = None
        self._summary: str = ""
        self._experiences: list[WorkExperience] = []
        self._skills: list[str] = []
        self._education: str = ""

    def contact(self, name: str, email: str, phone: str = "", linkedin: str = "") -> ResumeBuilder:
        # TODO: Create a ContactInfo from the arguments and store it in self._contact.
        # Then return self so the caller can keep chaining.
        # HINT: ContactInfo(name=name, email=email, phone=phone, linkedin=linkedin)
        pass

    def summary(self, text: str) -> ResumeBuilder:
        # TODO: Store the summary text and return self.
        pass

    def add_experience(self, company: str, title: str, years: float) -> ResumeBuilder:
        # TODO: Append a new WorkExperience to self._experiences and return self.
        # HINT: WorkExperience(company=company, title=title, years=years)
        pass

    def add_skill(self, skill: str) -> ResumeBuilder:
        # TODO: Append the skill string to self._skills and return self.
        pass

    def education(self, text: str) -> ResumeBuilder:
        # TODO: Store the education text and return self.
        pass

    def build(self) -> Resume:
        # TODO: If self._contact is None, raise ValueError("Contact information (name and email) is required.")
        # HINT: After validation, return Resume(...) with all fields.
        # Use list(self._experiences) and list(self._skills) — snapshots so the
        # builder's lists can't affect the built Resume if the builder is reused.
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/creational/builder/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
