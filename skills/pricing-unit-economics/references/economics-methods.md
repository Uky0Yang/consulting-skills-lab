# Economics and pricing methods

## Define before calculating

Fix the unit (account, seat, order, hour) and period. Use realized net revenue after discounts/refunds, excluding pass-through tax. Classify costs once: a recurring support allocation belongs in contribution only under a named allocation rule; a fixed support team may instead belong below contribution. Never deduct the same cost twice.

Acquisition spend should include the costs agreed in the definition and be matched to acquired—not total—customers. Disclose mismatched acquisition lag. CAC is not the incremental cost of a one-week ad test if the numerator includes a quarter's salaries.

## Equations and limits

| Metric | Equation | Limit |
| --- | --- | --- |
| Unit contribution | Net unit revenue − included variable/unit costs | Not automatically accounting gross profit |
| Contribution margin | Unit contribution / net unit revenue | Undefined at zero revenue |
| Operating break-even units | Ceiling(fixed period costs / positive unit contribution) | Requires stable mix, costs and feasible capacity |
| CAC | Matched acquisition spend / newly acquired customers | Undefined with no acquired customers |
| Simple CAC payback | CAC / positive monthly unit contribution | Ignores timing, churn and working capital unless modeled separately |
| Contribution LTV proxy | Monthly unit contribution / monthly logo churn | Assumes stable contribution and constant loss probability; not a cohort forecast |
| Volume to preserve contribution | Ceiling(baseline aggregate contribution / new positive unit contribution) | Holding costs, retention and mix fixed is a scenario assumption |

Annual churn conversion, if a constant monthly loss probability is justified, is `1 − (1 − annual churn)^(1/12)`, not annual churn divided by 12. Do not mix logo churn and revenue churn. A cohort table is preferable when expansion, changing usage, contraction or retention differ across segments.

At zero or missing churn, omit the simplified LTV. At nonpositive contribution, an unlimited number of customers does not solve fixed costs; repair price/cost/mix before proposing scale. Report actual cash timing separately for annual prepayment and onboarding outflows.

## Choose a pricing metric

Compare alignment with buyer value, cost behavior, predictability and measurement reliability. A per-seat offer may be easy to understand but poorly cover a heavy-usage AI workload. Usage pricing may track costs but create unpredictable bills. Hybrid or tiered offers need an explicit allowance, overage rule and caps—not just a label.

Treat interview-based willingness to pay as a hypothesis. Validate paid conversion, discounts, activation, retention and contribution against a comparable cohort. Predefine the test duration using the purchase/renewal cycle; a short test cannot establish annual renewal effects.

## Decision output

Show baseline and alternatives with the same definitions. Include threshold volume/retention, downside cost cases, capacity and unpriced risks. Name who can approve a test and the stop/rollback criteria. Do not claim a causal effect from an uncontrolled before/after comparison.
