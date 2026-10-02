import importlib.util
import csv
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from decimal import Decimal
from pathlib import Path

from scripts import evaluate_results, package_release


ROOT = Path(__file__).resolve().parents[1]
NEW_SKILLS = {"business-problem-framing", "expert-interview-synthesis", "pricing-unit-economics"}
CALCULATOR = ROOT / "skills/pricing-unit-economics/scripts/calculate_unit_economics.py"
BASE = {
    "currency": "GBP", "period": "month", "price": 120,
    "variable_costs": {"hosting": 18, "service": 12, "payments": 3},
    "fixed_costs": 12000, "acquisition_spend": 24000,
    "new_customers": 40, "customers": 200, "logo_churn": 0.025,
}


def calculator():
    spec = importlib.util.spec_from_file_location("unit_economics", CALCULATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestBusinessResearchSkills(unittest.TestCase):
    """ADD-001/002: Discoverable skills, usable resources and complete briefs."""

    def test_should_catalogue_all_three_skills(self):
        catalog = json.loads((ROOT / "data/skill-catalog.json").read_text(encoding="utf-8"))
        self.assertTrue(NEW_SKILLS <= {entry["name"] for entry in catalog["skills"]})

    def test_should_supply_two_raw_scenarios_per_new_skill(self):
        scenarios = evaluate_results.load_scenarios(ROOT)
        counts = {name: sum(s["skill"] == name for s in scenarios.values()) for name in NEW_SKILLS}
        self.assertEqual({name: 2 for name in NEW_SKILLS}, counts)

    def test_should_ship_editable_templates_and_calculator_inputs(self):
        paths = [
            "business-problem-framing/assets/decision-brief.md",
            "business-problem-framing/assets/hypothesis-plan.csv",
            "expert-interview-synthesis/assets/interview-evidence.csv",
            "expert-interview-synthesis/assets/interview-guide.md",
            "pricing-unit-economics/assets/unit-economics-input.json",
            "pricing-unit-economics/assets/pricing-experiment.csv",
        ]
        self.assertEqual([], [p for p in paths if not (ROOT / "skills" / p).is_file()])

    def test_should_keep_csv_template_rows_aligned_with_headers(self):
        mismatches = []
        for name in NEW_SKILLS:
            for path in (ROOT / "skills" / name / "assets").glob("*.csv"):
                rows = list(csv.reader(path.read_text(encoding="utf-8").splitlines()))
                mismatches.extend((path.name, index) for index, row in enumerate(rows[1:], 2) if len(row) != len(rows[0]))
        self.assertEqual([], mismatches)

    def test_should_normalize_csv_line_endings_in_evaluation_fingerprints(self):
        with tempfile.TemporaryDirectory() as destination:
            root = Path(destination)
            skill = root / "skills" / "sample-skill"
            skill.mkdir(parents=True)
            path = skill / "evidence.csv"
            path.write_bytes(b"id,text\nE1,fact\n")
            first = evaluate_results.skill_digest("sample-skill", root)
            path.write_bytes(b"id,text\r\nE1,fact\r\n")
            second = evaluate_results.skill_digest("sample-skill", root)
        self.assertEqual(first, second)

    def test_should_install_the_three_new_skills_together(self):
        with tempfile.TemporaryDirectory() as destination:
            run = subprocess.run([sys.executable, str(ROOT / "scripts/install_skills.py"),
                                  "--skills", *sorted(NEW_SKILLS), "--destination", destination],
                                 capture_output=True, text=True)
            installed = {p.name for p in Path(destination).iterdir()}
        self.assertEqual((0, NEW_SKILLS), (run.returncode, installed))

    def test_should_package_a_runnable_pricing_skill(self):
        with tempfile.TemporaryDirectory() as destination:
            archives = package_release.build_release(Path(destination))
            pricing = next((p for p in archives if p.name.startswith("pricing-unit-economics-")), None)
            self.assertIsNotNone(pricing)
            with zipfile.ZipFile(pricing) as archive:
                archive.extractall(Path(destination) / "unpacked")
            run = subprocess.run([sys.executable, str(Path(destination) / "unpacked/pricing-unit-economics/scripts/calculate_unit_economics.py")],
                                 capture_output=True, text=True)
        self.assertEqual((0, "87.000000"), (run.returncode, json.loads(run.stdout)["contribution_per_customer"]))


class TestUnitEconomics(unittest.TestCase):
    """ADD-003: Same-period calculation and honest undefined cases."""

    def test_should_calculate_contribution_and_profit(self):
        result = calculator().calculate(BASE)
        self.assertEqual((Decimal(33), Decimal(87), Decimal("0.725"), Decimal(5400)),
                         tuple(result[k] for k in ("variable_cost", "contribution_per_customer", "contribution_margin", "operating_surplus")))

    def test_should_calculate_margin_adjusted_payback(self):
        result = calculator().calculate(BASE)
        self.assertEqual(Decimal(600) / Decimal(87), result["payback_months"])

    def test_should_round_break_even_up(self):
        self.assertEqual(138, calculator().calculate(BASE)["break_even_customers"])

    def test_should_label_ltv_as_a_contribution_proxy(self):
        self.assertEqual(Decimal(3480), calculator().calculate(BASE)["contribution_ltv_proxy"])

    def test_should_not_invent_infinite_ltv_at_zero_churn(self):
        self.assertIsNone(calculator().calculate({**BASE, "logo_churn": 0})["contribution_ltv_proxy"])

    def test_should_leave_ltv_unknown_when_churn_is_missing(self):
        data = {k: v for k, v in BASE.items() if k != "logo_churn"}
        self.assertIsNone(calculator().calculate(data)["contribution_ltv_proxy"])

    def test_should_leave_cac_unknown_without_new_customers(self):
        self.assertIsNone(calculator().calculate({**BASE, "new_customers": 0})["cac"])

    def test_should_not_report_finite_payback_for_negative_contribution(self):
        result = calculator().calculate({**BASE, "price": 20})
        self.assertEqual((None, None, None), tuple(result[k] for k in ("payback_months", "break_even_customers", "contribution_ltv_proxy")))

    def test_should_support_free_plans_without_division_by_zero(self):
        self.assertIsNone(calculator().calculate({**BASE, "price": 0})["contribution_margin"])

    def test_should_reject_wrong_period_invalid_numbers_and_negative_costs(self):
        for field, value in (("period", "year"), ("price", True), ("price", "NaN"),
                             ("price", "Infinity"), ("fixed_costs", -1), ("customers", 1.5),
                             ("logo_churn", 1.1), ("variable_costs", {"hosting": -1})):
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                calculator().calculate({**BASE, field: value})

    def test_should_reject_missing_required_inputs(self):
        with self.assertRaises(ValueError):
            calculator().calculate({"price": 120})

    def test_should_fail_cleanly_on_malformed_json(self):
        with tempfile.TemporaryDirectory() as destination:
            path = Path(destination) / "bad.json"
            path.write_text("{", encoding="utf-8")
            run = subprocess.run([sys.executable, str(CALCULATOR), "--input", str(path)], capture_output=True, text=True)
        self.assertEqual((1, False), (run.returncode, "Traceback" in run.stderr))

    def test_should_keep_pricing_example_audit_table_in_sync(self):
        from scripts import check_example_calculations
        self.assertIn("pricing", check_example_calculations.CALCULATION_CHECKS)
        self.assertEqual([], check_example_calculations.validate_examples(ROOT))
