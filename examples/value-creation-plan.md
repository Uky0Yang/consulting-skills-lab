# Value Creation Plan — Worked Example

## User prompt

> Use $value-creation-plan to turn a diligence thesis for a £40m-EBITDA industrial distributor into a 100-day plan. The thesis includes £3m pricing, £2m procurement, and £4m cross-sell potential.

## Sample output

This is a fictional planning exercise, not validated finance data. The additional probability and cost assumptions are explicit in [example-calculations.json](../data/example-calculations.json).

### Executive answer

Use £3.42m risk-weighted annual run-rate as an illustrative planning hypothesis, not an underwritten or realized first-year result. The £9m headline is gross potential. Validate pricing and procurement through day-30 gates; keep cross-sell out of the base until account overlap, capacity, margin, and conversion evidence exist.

### Value bridge

| Initiative | Gross annual potential | Recurring disbenefit | Realization probability | Risk-weighted annual value | One-off cash cost | Finance status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pricing discipline | £3.0m | £0.4m churn/mix | 70% assumed | (£3.0m − £0.4m) × 70% = £1.82m | £0.0m assumed | Unreviewed |
| Procurement waves | £2.0m | £0.0m assumed | 80% assumed | £2.0m × 80% = £1.60m | £0.3m implementation | Unreviewed |
| Cross-sell | £4.0m | Unknown | Not estimated | £0.0m included | Unknown | Untested |

The £0.4m is a conditional recurring pricing disbenefit, not another probability haircut. The £0.3m implementation cost is paid regardless of whether procurement succeeds; it is not a recurring run-rate deduction. £3.42m − £0.3m = £3.12m is a **full-year-equivalent cash illustration before ramp**, not a forecast of actual first-year cash or EBITDA. Actual year-one benefit requires monthly rollout, recurring-cost, accounting, and attribution schedules agreed with finance.

<!-- calculations:value_plan:start -->
| Calculation | Exact result |
| --- | ---: |
| Risk-weighted pricing annual value | £1.82m |
| Risk-weighted procurement annual value | £1.6m |
| Combined annual run-rate | £3.42m |
| One-off implementation cash outflow | £0.3m |
| Full-year-equivalent net cash (before ramp) | £3.12m |
<!-- calculations:value_plan:end -->

### Initiative cards

| Initiative | Accountable owner | Day-30 outcome | Day-100 outcome | Red flag |
| --- | --- | --- | --- | --- |
| Pricing discipline | Chief Commercial Officer | Elasticity and exception baseline | New rules live in two segments | Volume loss exceeds 4% |
| Procurement waves | COO | Spend cube and supplier priorities validated | First two categories contracted | Quality or continuity breach |
| Cross-sell validation | Sales Director | Account overlap and buyer interviews complete | Pilot conversion economics approved or stopped | Payback exceeds 18 months |

### Governance

- Weekly initiative review: milestones, blockers, and decisions.
- Monthly finance review: baseline, attribution, forecast, and realized value.
- Sponsor escalation: more than 10% value erosion, missed critical milestone, or red-flag trigger.

### First decision gate

At day 30, approve pricing rollout only if elasticity evidence supports at least £1.5m net value; approve procurement waves only after finance reconciles the spend baseline; fund cross-sell execution only after the pilot clears its acquisition and margin thresholds.

## Why this is a strong response

- It separates gross potential, an unreviewed planning hypothesis, and realized value; no benefit is committed yet.
- Every initiative has one accountable owner and a red flag.
- It prevents untested cross-sell upside from entering the base plan.
