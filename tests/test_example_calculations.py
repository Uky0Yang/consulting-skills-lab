import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestExampleCalculations(unittest.TestCase):
    """FIX-001: Recalculate published examples from explicit fictional inputs."""

    def test_should_recalculate_market_sizing_and_capacity(self):
        from scripts import check_example_calculations
        result = check_example_calculations.calculate_market()
        self.assertEqual(
            (13513500, 31752000, 52416000, 29600000, 397, 240, 2419200),
            tuple(result[key] for key in ("low", "base", "high", "supply", "required_customers", "capacity_customers", "capacity_revenue")),
        )

    def test_should_separate_annual_value_and_one_off_cost(self):
        from scripts import check_example_calculations
        result = check_example_calculations.calculate_value_plan()
        self.assertEqual((1820000, 1600000, 3420000, 300000, 3120000), tuple(result.values()))

    def test_should_keep_documented_values_in_sync(self):
        from scripts import check_example_calculations
        self.assertEqual([], check_example_calculations.validate_examples(ROOT))

    def test_should_preserve_integer_millions_when_formatting(self):
        from scripts import check_example_calculations
        self.assertEqual("£10m", check_example_calculations.money(10000000))
