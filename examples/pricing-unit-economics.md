# Pricing and Unit Economics: a support-software offer

Fictional training inputs, not market research, observed willingness to pay or a verified customer outcome. This is a worked example, not a recorded behavioral evaluation.

## Request and raw inputs

> Use $pricing-unit-economics to compare our £120/month account plan with £150/month and a 15% discount. Do not assume that customers will accept the increase.

All revenue is net of tax, refunds and discounts. Monthly recurring cost per account: hosting £18, included service £12 and payments £3. These are cost assumptions held constant across scenarios; actual payment charges may change with price. Other fixed monthly costs: £12,000, excluding the included service allocation. Current accounts: 200. Matched acquisition spend £24,000 and acquired accounts 40, with no lag adjustment needed in this fictional brief. Monthly logo churn 2.5%, supplied as an assumption rather than a validated cohort estimate.

Machine-readable inputs: [unit-economics-input.json](../skills/pricing-unit-economics/assets/unit-economics-input.json). From the repository root:

```bash
python skills/pricing-unit-economics/scripts/calculate_unit_economics.py
```

## Baseline audit

Contribution includes the three named recurring costs. It is not an accounting gross-margin assertion. Operating surplus excludes acquisition spend, tax, onboarding cash and working capital.

<!-- calculations:pricing:start -->
| Calculation | Exact result |
| --- | ---: |
| Monthly variable cost per account | £33.00 |
| Monthly contribution per account | £87.00 |
| Contribution margin | 72.50% |
| Matched CAC | £600.00 |
| Simple contribution payback | 6.90 months |
| Operating break-even accounts (rounded up) | 138 |
| Monthly operating surplus at 200 accounts | £5,400.00 |
| Constant-churn contribution LTV proxy | £3,480.00 |
| Contribution LTV/CAC proxy | 5.80x |
<!-- calculations:pricing:end -->

The payback calculation is `£600 / £87`, not `£600 / £120`. The LTV proxy assumes unchanged contribution and constant monthly loss probability; it is not a cohort forecast. At missing/zero churn the helper omits LTV rather than reporting infinity.

## Alternatives and volume sensitivity

<!-- calculations:pricing-options:start -->
| Monthly net price | Unit contribution | Simple payback | Break-even accounts | Accounts to preserve baseline contribution |
| ---: | ---: | ---: | ---: | ---: |
| £120.00 | £87.00 | 6.90 months | 138 | 200 |
| £150.00 | £117.00 | 5.13 months | 103 | 149 |
| £102.00 | £69.00 | 8.70 months | 174 | 253 |
<!-- calculations:pricing-options:end -->

At £150, retaining 149 of the baseline 200 accounts preserves the baseline £17,400 monthly aggregate contribution under fixed cost/mix assumptions. Losing more than 51 accounts would fail that integer-volume threshold. This is a scenario threshold, not a forecast of price-related churn.

A 15% price discount requires at least 253 accounts versus 200 to preserve contribution: 26.5% more accounts, not merely 15%. Additional volume could increase service costs or exceed capacity, making this threshold optimistic.

## Recommendation and validation

Do not roll out an immediate blanket increase or discount. Test packaging and price with comparable new-customer cohorts, subject to commercial approval. Track realized price, paid conversion, included usage/cost, contribution and early cancellation; do not interpret favorable interviews as purchases.

Finance owns cost classification and CAC matching; the commercial lead owns cohort design; the product lead checks capacity and bill predictability. The sponsor must agree exposure limits and retention/quality guardrails before a live test. Hold the tested offer if cohort contribution falls below the agreed baseline or delivery quality deteriorates; a short test cannot establish annual renewal effects.

Handoff the input file, cost definitions, thresholds and unvalidated demand/churn assumptions into a decision memo or value-creation plan. Do not count the modeled price benefit as realized value.

Editable file: [pricing experiment register](../skills/pricing-unit-economics/assets/pricing-experiment.csv).
