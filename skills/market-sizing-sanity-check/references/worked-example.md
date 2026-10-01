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
= £31.752m serviceable annual revenue (approximately £31.8m)
```

Unit check:

```text
firms x % x % x seats/firm x £/seat/year = £/year
```

| Driver | Low | Base | High | Evidence status |
| --- | ---: | ---: | ---: | --- |
| Eligible firms | 7,000 | 7,500 | 8,000 | Fictional input |
| Workflow fit | 60% | 70% | 75% | Fictional input |
| Paid adoption | 45% | 60% | 70% | Fictional input |
| Seats per adopter | 11 | 14 | 16 | Fictional input |
| Realized annual price | £650 | £720 | £780 | Fictional input |

The coherent scenarios produce an approximate range of £13.5 million to £52.4 million. The range is wide because paid adoption and seats per adopter are not yet directly observed.

## Independent Supply-Side Cross-Check

The fictional supply-side inputs assume 12 relevant suppliers. No real interviews or pricing research were performed. Estimated current UK recurring revenue is:

```text
4 scaled providers x £5.0m
+ 8 specialist providers x £1.2m
= £29.6m annual supplier revenue
```

This method uses provider counts and estimated revenue bands rather than customer adoption and seat assumptions.

## Reconciliation

The £31.752 million year-three bottom-up base is 7.27% above the £29.6 million current supply-side estimate. This is an arithmetic comparison, not a like-for-like reconciliation. Three hypotheses could explain the difference:

1. The bottom-up estimate includes firms still using bundled modules, while the supply-side scan may exclude some bundled revenue.
2. The bottom-up price is an assumed year-three realized price; current supplier revenue reflects today's discounts and mix.
3. Both methods may miss small vendors, but only the bottom-up method assumes year-three adoption growth.

No quantified adjustment or current-to-year-three growth bridge has been supplied. Retain the £13.5-52.4 million scenario range with a £31.8 million base; do not narrow it to £27-35 million or average the two methods. The supply-side figure is a useful independent current-period check, not confirmation of the forecast.

## Obtainable Market and Decision Gate

The entrant needs £4 million revenue, equivalent to 12.6% of the base case. At the base price and 14 seats per customer:

```text
£4.0m / (£720 x 14) = about 397 adopting customers
```

If the entrant can win 80 customers per year after launch, it reaches only 240 customers by year three before churn, supporting £2.4192 million annual revenue. At the other base inputs, paid adoption must exceed 37.79% to clear the £20 million market-size threshold. The low scenario remains below that threshold, so market-size robustness and sales capacity both need validation.

### Recalculated audit table

<!-- calculations:market:start -->
| Calculation | Exact result |
| --- | ---: |
| Low year-three supplier revenue | £13.5135m |
| Base year-three supplier revenue | £31.752m |
| High year-three supplier revenue | £52.416m |
| Current supply-side revenue | £29.6m |
| Customers required (rounded up) | 397 |
| Customers supported before churn | 240 |
| Revenue supported before churn | £2.4192m |
<!-- calculations:market:end -->

## Executive Answer

The year-three model produces £13.5-52.4 million, with a £31.8 million base. The base clears £20 million, but the downside does not. The £4 million entrant target requires 397 active customers and is not supported by the present sales-capacity plan. Proceed only to validation: test paid adoption and seats through 15-20 buyer interviews, quantify the supply-side period/scope bridge, and redesign the channel plan. The base market-size case passes conditionally; neither downside robustness nor the obtainable-market case is proven.
