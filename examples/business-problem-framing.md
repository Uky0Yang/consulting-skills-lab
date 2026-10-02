# Business Problem Framing: do we need a new CRM?

All organizations, figures and source excerpts are fictional training inputs. This is a worked illustration, not a recorded behavioral evaluation.

## Raw request and evidence

> Use $business-problem-framing to assess our director's request for an £80,000 CRM replacement. We have ten business days before the budget meeting. The director thinks falling sales conversion caused our margin decline.

- F1, finance summary, year ended 2025: revenue £3.0m, included variable costs £1.2m, fixed costs £1.2m, operating profit £0.6m.
- F2, same definitions, year ended 2026: revenue £3.0m, included variable costs £1.5m, fixed costs £1.2m, operating profit £0.3m.
- F3, sales operations note: the lead definition changed midway through 2026; conversion rates have not been restated. Sales volume and realized-price/mix data are not supplied.
- The CFO owns the budget decision. The director proposes a CRM; neither a recovery target nor permission to change the system has been agreed.

## Decision brief

**Status:** provisional. By the budget meeting in ten business days, the CFO must choose whether to fund the CRM now, defer it for targeted diagnosis, or pursue a lower-cost operational response. The objective is to select a credible margin-recovery action, not to prove that a CRM is necessary. Target magnitude and investment hurdle require CFO agreement.

The supplied accounting bridge shows a £0.3m profit decline entirely reconciled by the £0.3m rise in included variable costs. Operating margin fell from 20% to 10%. This does not prove that a CRM cannot help; it means conversion is not yet an evidenced explanation for the observed bridge. Constant total revenue also does not prove stable price, volume or mix.

**Boundary:** the same business and two full financial years, using F1/F2 cost definitions. In scope: revenue/mix, delivery-cost bridge, metric-definition change and whether a CRM addresses a verified mechanism. Out of scope without approval: live migration, procurement commitments and a company-wide restructuring.

## Issue tree and competing hypotheses

```text
Operating profit change = revenue change − variable-cost change − fixed-cost change
├─ Revenue: volume × realized price, with product/customer mix reconciliation
├─ Variable costs: delivered activity × unit cost, with rework and service mix
└─ Fixed costs: comparable classification and any exceptional items
```

This identity reconciles the supplied totals. It does not guarantee complete operational causality; misclassification or unmatched periods must still be checked.

| Hypothesis | Evidence for / against | Falsification test | Owner and deadline | Decision consequence |
| --- | --- | --- | --- | --- |
| Higher delivery cost or service mix caused the decline | F2 cost bridge supports; no unit/mix detail | Match product/customer cohort and reconcile volume, rates, rework and allocations to the £0.3m change | Finance analyst + operations lead, day 4 | Prioritize cost/mix response if bridge is supported |
| Conversion deterioration is material and CRM-related | Director's claim only; F3 breaks comparability | Restate funnel denominator; inspect lost-deal reasons and CRM-related failures in comparable cohorts | Sales operations lead, day 5 | CRM remains an option only if a mechanism and benefit path emerge |
| The decline is a classification or one-off effect | No evidence yet | Check accounting policy, cost transfers and exceptions across F1/F2 | Finance controller, day 3 | Restate baseline before investing against an artificial gap |

## Recommendation and handoff

Defer an unconditional CRM commitment while running the bounded diagnosis. This is a provisional recommendation, not CFO approval. Ask the CFO to agree the recovery objective, investment threshold and who can validate benefits on day 1.

Stop expanding the analysis once the material bridge is reconciled and the CRM mechanism can be accepted or rejected against the agreed hurdle. If data remains incomparable by day 5, disclose the unresolved exposure and take a staged funding option to the meeting; do not fill the gap with a savings claim.

Handoff: F1–F3, comparable metric definitions, reconciled bridge, rival hypotheses, unverified CRM benefits and remaining scope choices. Use these fields to prepare interviews or an executive decision memo.

Editable starting files: [decision brief](../skills/business-problem-framing/assets/decision-brief.md) and [hypothesis plan](../skills/business-problem-framing/assets/hypothesis-plan.csv).
