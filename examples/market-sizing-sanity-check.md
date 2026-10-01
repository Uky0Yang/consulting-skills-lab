# Market Sizing Sanity Check — Worked Example

## User prompt

> Use $market-sizing-sanity-check to audit our claim that the UK mid-market compliance workflow software market will be worth £50m in year three. Show an independent cross-check and tell us whether a £4m revenue target is credible.

## Sample output

All inputs are fictional. The calculation fixture is [example-calculations.json](../data/example-calculations.json); the full method is in the [worked example](../skills/market-sizing-sanity-check/references/worked-example.md).

### Executive answer

The model gives a £31.8m year-three base and a £13.5–52.4m scenario range. £50m is near the upside case, not a supported base. The £20m entry threshold fails in the downside, and the £4m entrant target requires 397 active customers versus 240 supported by current sales capacity.

### Primary estimate

```text
7,500 eligible firms
x 70% workflow fit
x 60% paid adoption
x 14 seats per firm
x £720 annual realized price
= £31.752m annual supplier revenue (approximately £31.8m)
```

The units reconcile to pounds per year. Paid adoption and seats per firm are the least certain drivers.

### Independent cross-check

```text
4 scaled providers x £5.0m UK revenue
+ 8 specialists x £1.2m UK revenue
= £29.6m current supplier revenue
```

The cross-check uses provider revenue bands rather than customer and seat assumptions. The base is 7.27% above it, but the figures describe different periods. No growth or scope bridge has been supplied, so retain the wide scenario range rather than manufacturing convergence.

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

### Decision sensitivity

| Assumption | Decision threshold | Current evidence | Implication |
| --- | ---: | --- | --- |
| Serviceable market | £20m | £13.5–52.4m; £31.8m base | Base passes; downside fails |
| Customers required | About 397 | 240 supported by current capacity | Revenue plan fails |
| Paid adoption at other base inputs | 37.79% | 60% fictional base | Validate adoption and seats before investment |

### Next evidence

Run 15–20 buyer interviews, verify bundled-module revenue, and rebuild the channel plan around a credible path to 400 active customers before approving full entry investment.

## Why this is a strong response

- It defines supplier revenue, geography, customer, and period.
- Its cross-check is causally independent.
- It separates a large-enough market from an obtainable revenue plan.
