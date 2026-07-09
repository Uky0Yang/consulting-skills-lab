import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "value-creation-plan"


class TestValueCreationPlan(unittest.TestCase):
    def test_should_include_a_100_day_workflow(self) -> None:
        """REQ-VCP-001: The skill turns diligence into a sequenced 100-day plan."""
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("100-day", skill_text)

    def test_should_include_a_benefits_tracker_template(self) -> None:
        """REQ-VCP-002: The skill provides an accountable value-tracking artifact."""
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("Benefits Tracker", skill_text)

    def test_should_include_the_value_plan_reference(self) -> None:
        """REQ-VCP-003: The skill links to its reusable execution reference."""
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("`references/value-plan-artifacts.md`", skill_text)

    def test_should_include_agent_metadata(self) -> None:
        """REQ-VCP-004: The skill can be surfaced by the Codex skill interface."""
        metadata = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn("$value-creation-plan", metadata)

    def test_should_list_the_skill_in_the_repository_readme(self) -> None:
        """REQ-VCP-005: Visitors can discover the new skill from the repository landing page."""
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("| `value-creation-plan` |", readme)
