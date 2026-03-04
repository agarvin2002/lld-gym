"""
Builder Pattern Exercise — Resume / CV Builder (Solution)
"""
from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data classes
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
        self._contact: ContactInfo | None = None
        self._summary: str = ""
        self._experiences: list[WorkExperience] = []
        self._skills: list[str] = []
        self._education: str = ""

    def contact(self, name: str, email: str, phone: str = "", linkedin: str = "") -> ResumeBuilder:
        self._contact = ContactInfo(name=name, email=email, phone=phone, linkedin=linkedin)
        return self

    def summary(self, text: str) -> ResumeBuilder:
        self._summary = text
        return self

    def add_experience(self, company: str, title: str, years: float) -> ResumeBuilder:
        self._experiences.append(WorkExperience(company=company, title=title, years=years))
        return self

    def add_skill(self, skill: str) -> ResumeBuilder:
        self._skills.append(skill)
        return self

    def education(self, text: str) -> ResumeBuilder:
        self._education = text
        return self

    def build(self) -> Resume:
        if self._contact is None:
            raise ValueError("Contact information (name and email) is required.")
        return Resume(
            contact=self._contact,
            summary=self._summary,
            experiences=list(self._experiences),  # snapshot — isolates built object
            skills=list(self._skills),            # snapshot — isolates built object
            education=self._education,
        )
