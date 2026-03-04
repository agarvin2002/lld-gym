"""
Tests for the Builder Pattern exercise — Resume / CV Builder.

Run with:
    /tmp/lld_venv/bin/pytest 03_design_patterns/creational/builder/exercises/tests.py -v
"""
import sys
import os

import pytest

# Critical: insert the exercises/ directory so 'starter' resolves to starter.py
# and pop any cached 'starter' module to avoid cross-test-file collisions.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)

from starter import ContactInfo, WorkExperience, Resume, ResumeBuilder


# ---------------------------------------------------------------------------
# TestResumeBuilderBasic
# ---------------------------------------------------------------------------

class TestResumeBuilderBasic:
    """Happy-path construction with contact and summary."""

    def test_build_with_contact_and_summary_returns_resume(self):
        resume = (ResumeBuilder()
                  .contact("Alice", "alice@example.com")
                  .summary("Great engineer.")
                  .build())
        assert isinstance(resume, Resume)

    def test_contact_name_is_set(self):
        resume = ResumeBuilder().contact("Bob", "bob@example.com").build()
        assert resume.contact.name == "Bob"

    def test_contact_email_is_set(self):
        resume = ResumeBuilder().contact("Bob", "bob@example.com").build()
        assert resume.contact.email == "bob@example.com"

    def test_contact_optional_phone_defaults_to_empty(self):
        resume = ResumeBuilder().contact("Bob", "bob@example.com").build()
        assert resume.contact.phone == ""

    def test_contact_optional_phone_can_be_set(self):
        resume = ResumeBuilder().contact("Bob", "bob@example.com", phone="555-1234").build()
        assert resume.contact.phone == "555-1234"

    def test_contact_optional_linkedin_defaults_to_empty(self):
        resume = ResumeBuilder().contact("Bob", "bob@example.com").build()
        assert resume.contact.linkedin == ""

    def test_contact_optional_linkedin_can_be_set(self):
        resume = (ResumeBuilder()
                  .contact("Bob", "bob@example.com", linkedin="linkedin.com/in/bob")
                  .build())
        assert resume.contact.linkedin == "linkedin.com/in/bob"

    def test_summary_is_set(self):
        resume = (ResumeBuilder()
                  .contact("Carol", "carol@example.com")
                  .summary("Expert in distributed systems.")
                  .build())
        assert resume.summary == "Expert in distributed systems."

    def test_summary_defaults_to_empty_string_when_not_called(self):
        resume = ResumeBuilder().contact("Carol", "carol@example.com").build()
        assert resume.summary == ""

    def test_education_is_set(self):
        resume = (ResumeBuilder()
                  .contact("Dave", "dave@example.com")
                  .education("B.Sc. CS, MIT, 2020")
                  .build())
        assert resume.education == "B.Sc. CS, MIT, 2020"

    def test_education_defaults_to_empty_string_when_not_called(self):
        resume = ResumeBuilder().contact("Dave", "dave@example.com").build()
        assert resume.education == ""

    def test_contact_info_is_contactinfo_instance(self):
        resume = ResumeBuilder().contact("Eve", "eve@example.com").build()
        assert isinstance(resume.contact, ContactInfo)


# ---------------------------------------------------------------------------
# TestResumeBuilderExperiences
# ---------------------------------------------------------------------------

class TestResumeBuilderExperiences:
    """Tests for add_experience accumulation."""

    def test_add_experience_appends_one_entry(self):
        resume = (ResumeBuilder()
                  .contact("Frank", "frank@example.com")
                  .add_experience("Google", "SWE", 3.0)
                  .build())
        assert len(resume.experiences) == 1

    def test_add_experience_fields_are_correct(self):
        resume = (ResumeBuilder()
                  .contact("Frank", "frank@example.com")
                  .add_experience("Google", "Senior SWE", 4.5)
                  .build())
        exp = resume.experiences[0]
        assert exp.company == "Google"
        assert exp.title == "Senior SWE"
        assert exp.years == 4.5

    def test_multiple_add_experience_calls_accumulate(self):
        resume = (ResumeBuilder()
                  .contact("Grace", "grace@example.com")
                  .add_experience("Stripe", "SWE I", 2.0)
                  .add_experience("Meta", "SWE II", 3.0)
                  .add_experience("Amazon", "Senior SWE", 1.5)
                  .build())
        assert len(resume.experiences) == 3

    def test_experience_order_is_preserved(self):
        resume = (ResumeBuilder()
                  .contact("Grace", "grace@example.com")
                  .add_experience("First Corp", "Intern", 0.5)
                  .add_experience("Second Corp", "Engineer", 2.0)
                  .build())
        assert resume.experiences[0].company == "First Corp"
        assert resume.experiences[1].company == "Second Corp"

    def test_experiences_list_is_empty_when_none_added(self):
        resume = ResumeBuilder().contact("Heidi", "heidi@example.com").build()
        assert resume.experiences == []

    def test_experience_entries_are_workexperience_instances(self):
        resume = (ResumeBuilder()
                  .contact("Ivan", "ivan@example.com")
                  .add_experience("Corp", "Role", 1.0)
                  .build())
        assert isinstance(resume.experiences[0], WorkExperience)


# ---------------------------------------------------------------------------
# TestResumeBuilderSkills
# ---------------------------------------------------------------------------

class TestResumeBuilderSkills:
    """Tests for add_skill accumulation."""

    def test_add_skill_appends_one_skill(self):
        resume = (ResumeBuilder()
                  .contact("Judy", "judy@example.com")
                  .add_skill("Python")
                  .build())
        assert len(resume.skills) == 1
        assert resume.skills[0] == "Python"

    def test_multiple_add_skill_calls_accumulate(self):
        resume = (ResumeBuilder()
                  .contact("Judy", "judy@example.com")
                  .add_skill("Python")
                  .add_skill("System Design")
                  .add_skill("SQL")
                  .build())
        assert len(resume.skills) == 3

    def test_skill_order_is_preserved(self):
        resume = (ResumeBuilder()
                  .contact("Karl", "karl@example.com")
                  .add_skill("A")
                  .add_skill("B")
                  .add_skill("C")
                  .build())
        assert resume.skills == ["A", "B", "C"]

    def test_skills_list_is_empty_when_none_added(self):
        resume = ResumeBuilder().contact("Laura", "laura@example.com").build()
        assert resume.skills == []


# ---------------------------------------------------------------------------
# TestResumeBuilderValidation
# ---------------------------------------------------------------------------

class TestResumeBuilderValidation:
    """build() must raise ValueError when contact() was never called."""

    def test_build_without_contact_raises_value_error(self):
        with pytest.raises(ValueError):
            ResumeBuilder().build()

    def test_build_without_contact_but_with_summary_still_raises(self):
        with pytest.raises(ValueError):
            ResumeBuilder().summary("Some text").build()

    def test_build_without_contact_but_with_skill_still_raises(self):
        with pytest.raises(ValueError):
            ResumeBuilder().add_skill("Python").build()

    def test_build_without_contact_but_with_experience_still_raises(self):
        with pytest.raises(ValueError):
            ResumeBuilder().add_experience("Corp", "Role", 1.0).build()

    def test_build_succeeds_after_contact_is_called(self):
        # Should not raise
        resume = ResumeBuilder().contact("Mike", "mike@example.com").build()
        assert resume.contact.name == "Mike"


# ---------------------------------------------------------------------------
# TestResumeBuilderChaining
# ---------------------------------------------------------------------------

class TestResumeBuilderChaining:
    """All setter methods must return the same builder instance (self)."""

    def test_contact_returns_builder(self):
        builder = ResumeBuilder()
        result = builder.contact("Nina", "nina@example.com")
        assert result is builder

    def test_summary_returns_builder(self):
        builder = ResumeBuilder()
        builder.contact("Nina", "nina@example.com")
        result = builder.summary("Great engineer.")
        assert result is builder

    def test_add_experience_returns_builder(self):
        builder = ResumeBuilder()
        builder.contact("Nina", "nina@example.com")
        result = builder.add_experience("Corp", "Role", 1.0)
        assert result is builder

    def test_add_skill_returns_builder(self):
        builder = ResumeBuilder()
        builder.contact("Nina", "nina@example.com")
        result = builder.add_skill("Python")
        assert result is builder

    def test_education_returns_builder(self):
        builder = ResumeBuilder()
        builder.contact("Nina", "nina@example.com")
        result = builder.education("B.Sc. CS")
        assert result is builder

    def test_full_chain_produces_correct_resume(self):
        resume = (ResumeBuilder()
                  .contact("Oscar", "oscar@example.com",
                            phone="555-9999", linkedin="linkedin.com/in/oscar")
                  .summary("Full-stack developer.")
                  .add_experience("Startup A", "CTO", 2.0)
                  .add_experience("BigCo", "Staff Engineer", 5.0)
                  .add_skill("Python")
                  .add_skill("Go")
                  .education("M.Sc. CS, Stanford, 2015")
                  .build())

        assert resume.contact.name == "Oscar"
        assert resume.contact.phone == "555-9999"
        assert resume.contact.linkedin == "linkedin.com/in/oscar"
        assert resume.summary == "Full-stack developer."
        assert len(resume.experiences) == 2
        assert resume.experiences[1].company == "BigCo"
        assert resume.skills == ["Python", "Go"]
        assert resume.education == "M.Sc. CS, Stanford, 2015"


# ---------------------------------------------------------------------------
# TestResumeBuilderIsolation
# ---------------------------------------------------------------------------

class TestResumeBuilderIsolation:
    """Two builder instances must not share state."""

    def test_separate_builders_have_independent_skills(self):
        builder1 = ResumeBuilder().contact("Pam", "pam@example.com")
        builder2 = ResumeBuilder().contact("Quinn", "quinn@example.com")

        builder1.add_skill("Python")
        builder2.add_skill("Java")

        resume1 = builder1.build()
        resume2 = builder2.build()

        assert resume1.skills == ["Python"]
        assert resume2.skills == ["Java"]

    def test_separate_builders_have_independent_experiences(self):
        builder1 = ResumeBuilder().contact("Rex", "rex@example.com")
        builder2 = ResumeBuilder().contact("Sue", "sue@example.com")

        builder1.add_experience("Corp A", "Engineer", 2.0)
        # builder2 intentionally gets no experience

        resume1 = builder1.build()
        resume2 = builder2.build()

        assert len(resume1.experiences) == 1
        assert len(resume2.experiences) == 0

    def test_mutating_builder_after_build_does_not_affect_resume(self):
        """
        build() must snapshot the lists.
        Adding a skill after build() must NOT mutate the previously built Resume.
        """
        builder = ResumeBuilder().contact("Tom", "tom@example.com").add_skill("Python")
        resume = builder.build()

        # Mutate the builder after build()
        builder.add_skill("Java")

        # The built resume must still have only the original skill
        assert resume.skills == ["Python"]

    def test_mutating_builder_experiences_after_build_does_not_affect_resume(self):
        builder = (ResumeBuilder()
                   .contact("Uma", "uma@example.com")
                   .add_experience("OldCorp", "Junior Dev", 1.0))
        resume = builder.build()

        # Add another experience after build
        builder.add_experience("NewCorp", "Senior Dev", 3.0)

        assert len(resume.experiences) == 1
