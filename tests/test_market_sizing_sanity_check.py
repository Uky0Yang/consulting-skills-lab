import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "market-sizing-sanity-check"


class TestMarketSizingSanityCheck(unittest.TestCase):
    def test_should_require_an_independent_cross_check(self) -> None:
        """REQ-MSS-001: The estimate is triangulated rather than asserted."""
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("independent cross-check", skill_text.lower())

    def test_should_include_units_and_decision_sensitivity(self) -> None:
        """REQ-MSS-002: The workflow audits units and decision-changing assumptions."""
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("units", skill_text.lower())
        self.assertIn("## Decision Sensitivity", skill_text)

    def test_should_include_a_complete_worked_example(self) -> None:
        """REQ-MSS-003: A reusable example demonstrates calculation and reconciliation."""
        example = (SKILL_DIR / "references" / "worked-example.md").read_text(encoding="utf-8")

        self.assertIn("Unit check", example)
        self.assertIn("## Reconciliation", example)
        self.assertIn("## Executive Answer", example)

    def test_should_be_listed_in_the_machine_readable_catalog(self) -> None:
        """REQ-MSS-004: Tools can discover the skill from the repository catalog."""
        catalog = json.loads((ROOT / "data" / "skill-catalog.json").read_text(encoding="utf-8"))

        names = {skill["name"] for skill in catalog["skills"]}
        self.assertIn("market-sizing-sanity-check", names)

    def test_should_be_listed_in_the_repository_readme(self) -> None:
        """REQ-MSS-005: Visitors can discover the skill from the landing page."""
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("| `market-sizing-sanity-check` |", readme)
