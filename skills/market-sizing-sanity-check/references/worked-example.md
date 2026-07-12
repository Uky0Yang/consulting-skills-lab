# Worked Example: UK Compliance Workflow Software

This fictional example demonstrates method independence, unit checks, reconciliation, and decision sensitivity. It is not a claim about an actual market.

## Decision and Definition

A software company is deciding whether to invest £6 million to enter the UK market for compliance workflow software used by mid-sized regulated firms.

- Customer: UK regulated firms with 100-999 employees.
- Product: paid workflow seats for compliance teams.
- Metric: annual supplier recurring revenue in year three.
- Exclusions: implementation services, firms outside the employee range, and general document-management tools.
- Decision threshold: at least £20 million serviceable annual revenue and a credible path to £4 million annual revenue for the entrant.

## Primary Bottom-Up Estimate

```text
7,500 eligible firms
x 70% workflow fit
x 60% paid-category adoption in year three
x 14 seats per adopting firm
x £720 realized annual revenue per seat
= £33.3m serviceable annual revenue
```

Unit check:

```text
firms x % x % x seats/firm x £/seat/year = £/year
```

| Driver | Low | Base | High | Evidence status |
| --- | ---: | ---: | ---: | --- |
| Eligible firms | 7,000 | 7,500 | 8,000 | Corroborated |
| Workflow fit | 60% | 70% | 75% | Directional |
| Paid adoption | 45% | 60% | 70% | Assumed |
| Seats per adopter | 11 | 14 | 16 | Directional |
| Realized annual price | £650 | £720 | £780 | Corroborated |

The coherent scenarios produce an approximate range of £13.5 million to £52.4 million. The range is wide because paid adoption and seats per adopter are not yet directly observed.

## Independent Supply-Side Cross-Check

Interviews and public pricing checks identify 12 relevant suppliers. Estimated UK recurring revenue is:

```text
4 scaled providers x £5.0m
+ 8 specialist providers x £1.2m
= £29.6m annual supplier revenue
```

This method uses provider counts and estimated revenue bands rather than customer adoption and seat assumptions.

## Reconciliation

The £33.3 million bottom-up base is 13% above the £29.6 million supply-side estimate. Three adjustments explain most of the gap:

1. The bottom-up estimate includes firms still using bundled modules, while the supply-side scan may exclude some bundled revenue.
2. The bottom-up price is an assumed year-three realized price; current supplier revenue reflects today's discounts and mix.
3. Both methods may miss small vendors, but only the bottom-up method assumes year-three adoption growth.

The estimates are close enough to support a £27-35 million year-three serviceable range, with medium confidence. They should not be averaged mechanically.

## Obtainable Market and Decision Gate

The entrant needs £4 million revenue, equivalent to roughly 12-15% of the serviceable range. At the base price and 14 seats per customer:

```text
£4.0m / (£720 x 14) = about 397 adopting customers
```

If the entrant can win 80 customers per year after launch, it reaches only about 240 customers by year three before churn. The market is large enough, but the current go-to-market capacity does not support the revenue case.

## Executive Answer

The year-three serviceable market is plausibly £27-35 million, above the £20 million threshold, but the £4 million entrant target requires about 397 customers and is not supported by the present sales-capacity plan. Proceed only to a validation stage: test paid adoption and seats through 15-20 buyer interviews, confirm bundled-module revenue, and redesign the channel plan to show a credible route to at least 400 active customers. The market-size test passes; the obtainable-market test does not yet pass.
