"""Audit monthly steady-state unit economics; no network or model calls."""
from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from pathlib import Path


def number(value, field: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"{field} must be a finite nonnegative number")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f"{field} must be finite and nonnegative")
    return result


def calculate(data: dict) -> dict:
    if not isinstance(data, dict) or data.get("period") != "month":
        raise ValueError("inputs must be an object with period=month; normalize other periods explicitly")
    currency = data.get("currency")
    if not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency):
        raise ValueError("currency must be a three-letter uppercase label")
    required = ("price", "fixed_costs", "acquisition_spend", "new_customers", "customers")
    if any(field not in data for field in required):
        raise ValueError("missing price, cost or acquisition/customer inputs")
    values = {field: number(data[field], field) for field in required}
    for field in ("new_customers", "customers"):
        if values[field] != values[field].to_integral_value():
            raise ValueError(f"{field} must be an integer count")
    costs = data.get("variable_costs")
    if not isinstance(costs, dict) or not costs or not all(isinstance(k, str) and k.strip() for k in costs):
        raise ValueError("variable_costs must be a non-empty named cost mapping")
    variable = sum((number(v, f"variable_costs.{k}") for k, v in costs.items()), Decimal(0))
    price = values["price"]
    contribution = price - variable
    cac = values["acquisition_spend"] / values["new_customers"] if values["new_customers"] else None
    churn = number(data["logo_churn"], "logo_churn") if data.get("logo_churn") is not None else None
    if churn is not None and churn > 1:
        raise ValueError("monthly logo_churn must be between zero and one")
    warnings = ["Steady-state scenario; contribution is not accounting gross margin or cash flow.",
                "Operating surplus excludes acquisition spend, tax, onboarding and working capital."]
    if cac is None:
        warnings.append("CAC undefined: no new customers in the matched acquisition period.")
    if contribution <= 0:
        warnings.append("Nonpositive contribution: finite payback, break-even and contribution LTV are not reported.")
    if churn is None or churn == 0:
        warnings.append("LTV proxy unavailable: missing or zero churn does not establish an infinite lifetime.")
    else:
        warnings.append("LTV is a constant-churn contribution proxy, not a cohort forecast.")
    ltv = contribution / churn if contribution > 0 and churn else None
    return {
        "currency": currency, "period": "month", "fictional": data.get("fictional") is True,
        "variable_cost": variable, "contribution_per_customer": contribution,
        "contribution_margin": contribution / price if price else None,
        "cac": cac, "payback_months": cac / contribution if cac is not None and contribution > 0 else None,
        "break_even_customers": int((values["fixed_costs"] / contribution).to_integral_value(rounding=ROUND_CEILING)) if contribution > 0 else None,
        "operating_surplus": values["customers"] * contribution - values["fixed_costs"],
        "contribution_ltv_proxy": ltv, "ltv_cac_proxy": ltv / cac if ltv is not None and cac else None,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).resolve().parents[1] / "assets/unit-economics-input.json")
    args = parser.parse_args(argv)
    try:
        result = calculate(json.loads(args.input.read_text(encoding="utf-8")))
        encoded = {k: format(v, ".6f") if isinstance(v, Decimal) else v for k, v in result.items()}
        print(json.dumps(encoded, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, InvalidOperation) as exc:
        print(f"Calculation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
