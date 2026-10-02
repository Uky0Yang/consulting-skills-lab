"""Recalculate fictional inputs and verify the rendered audit tables in examples."""
from __future__ import annotations

import json
import importlib.util
import sys
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALCULATION_CHECKS = {
    "market": ["examples/market-sizing-sanity-check.md", "skills/market-sizing-sanity-check/references/worked-example.md"],
    "value_plan": ["examples/value-creation-plan.md"],
    "pricing": ["examples/pricing-unit-economics.md"],
}


def inputs(root: Path = ROOT) -> dict:
    return json.loads((root / "data/example-calculations.json").read_text(encoding="utf-8"))


def calculate_market(data: dict | None = None) -> dict[str, Decimal | int]:
    data = inputs()["market"] if data is None else data
    result: dict[str, Decimal | int] = {}
    for scenario in ("low", "base", "high"):
        value = Decimal(1)
        for driver in data[scenario]:
            value *= Decimal(str(driver))
        result[scenario] = value
    result["supply"] = sum(Decimal(count) * Decimal(revenue) for count, revenue in data["supply_bands"])
    revenue_per_customer = Decimal(data["base"][3]) * Decimal(data["base"][4])
    result["required_customers"] = int((Decimal(data["entrant_target"]) / revenue_per_customer).to_integral_value(rounding=ROUND_CEILING))
    result["capacity_customers"] = data["wins_per_year"] * data["years"]
    result["capacity_revenue"] = result["capacity_customers"] * revenue_per_customer
    return result


def calculate_value_plan(data: dict | None = None) -> dict[str, Decimal]:
    data = inputs()["value_plan"] if data is None else data
    benefits = {
        name: (Decimal(item["gross"]) - Decimal(item["recurring_disbenefit"])) * Decimal(item["probability"])
        for name, item in data.items()
    }
    annual = sum(benefits.values(), Decimal(0))
    one_off = sum((Decimal(item["one_off"]) for item in data.values()), Decimal(0))
    return {**benefits, "annual": annual, "one_off": one_off, "full_year_cash": annual - one_off}


def money(value: Decimal | int) -> str:
    millions = format(Decimal(value) / Decimal(1000000), "f")
    if "." in millions:
        millions = millions.rstrip("0").rstrip(".")
    return f"£{millions or '0'}m"


def render_table(kind: str, result: dict) -> str:
    if kind == "pricing":
        rows = [
            ("Monthly variable cost per account", f"£{result['variable_cost']:,.2f}"),
            ("Monthly contribution per account", f"£{result['contribution_per_customer']:,.2f}"),
            ("Contribution margin", f"{result['contribution_margin'] * 100:.2f}%"),
            ("Matched CAC", f"£{result['cac']:,.2f}"),
            ("Simple contribution payback", f"{result['payback_months']:.2f} months"),
            ("Operating break-even accounts (rounded up)", str(result['break_even_customers'])),
            ("Monthly operating surplus at 200 accounts", f"£{result['operating_surplus']:,.2f}"),
            ("Constant-churn contribution LTV proxy", f"£{result['contribution_ltv_proxy']:,.2f}"),
            ("Contribution LTV/CAC proxy", f"{result['ltv_cac_proxy']:.2f}x"),
        ]
        return "\n".join(["<!-- calculations:pricing:start -->", "| Calculation | Exact result |", "| --- | ---: |",
                          *[f"| {label} | {value} |" for label, value in rows], "<!-- calculations:pricing:end -->"])
    labels = {
        "market": {
            "low": "Low year-three supplier revenue", "base": "Base year-three supplier revenue",
            "high": "High year-three supplier revenue", "supply": "Current supply-side revenue",
            "required_customers": "Customers required (rounded up)", "capacity_customers": "Customers supported before churn",
            "capacity_revenue": "Revenue supported before churn",
        },
        "value_plan": {
            "pricing": "Risk-weighted pricing annual value", "procurement": "Risk-weighted procurement annual value",
            "annual": "Combined annual run-rate", "one_off": "One-off implementation cash outflow",
            "full_year_cash": "Full-year-equivalent net cash (before ramp)",
        },
    }[kind]
    lines = [f"<!-- calculations:{kind}:start -->", "| Calculation | Exact result |", "| --- | ---: |"]
    for key, label in labels.items():
        value = str(result[key]) if key.endswith("customers") else money(result[key])
        lines.append(f"| {label} | {value} |")
    lines.append(f"<!-- calculations:{kind}:end -->")
    return "\n".join(lines)


def validate_examples(root: Path = ROOT) -> list[str]:
    data = inputs(root)
    calculator_path = root / "skills/pricing-unit-economics/scripts/calculate_unit_economics.py"
    spec = importlib.util.spec_from_file_location("pricing_calculator", calculator_path)
    calculator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(calculator)
    pricing = json.loads((root / "skills/pricing-unit-economics/assets/unit-economics-input.json").read_text(encoding="utf-8"))
    checks = {
        "market": calculate_market(data["market"]),
        "value_plan": calculate_value_plan(data["value_plan"]),
        "pricing": calculator.calculate(pricing),
    }
    errors = []
    for kind, result in checks.items():
        expected = render_table(kind, result)
        for relative in CALCULATION_CHECKS[kind]:
            if expected not in (root / relative).read_text(encoding="utf-8"):
                errors.append(f"{relative}: calculated {kind} audit table is missing or stale")
    rows = ["<!-- calculations:pricing-options:start -->", "| Monthly net price | Unit contribution | Simple payback | Break-even accounts | Accounts to preserve baseline contribution |",
            "| ---: | ---: | ---: | ---: | ---: |"]
    baseline = checks["pricing"]["contribution_per_customer"] * Decimal(pricing["customers"])
    for price in (Decimal(pricing["price"]), Decimal(150), Decimal(pricing["price"]) * Decimal("0.85")):
        result = calculator.calculate({**pricing, "price": price})
        customers = int((baseline / result["contribution_per_customer"]).to_integral_value(rounding=ROUND_CEILING))
        rows.append(f"| £{price:.2f} | £{result['contribution_per_customer']:.2f} | {result['payback_months']:.2f} months | {result['break_even_customers']} | {customers} |")
    rows.append("<!-- calculations:pricing-options:end -->")
    if "\n".join(rows) not in (root / "examples/pricing-unit-economics.md").read_text(encoding="utf-8"):
        errors.append("examples/pricing-unit-economics.md: pricing options audit table is missing or stale")
    return errors


def main() -> int:
    errors = validate_examples()
    print("\n".join(errors) if errors else "Example calculations passed (fictional inputs; not market evidence).")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
