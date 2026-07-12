# Sizing Methods and Reconciliation

Use the smallest set of methods that provides one primary estimate and one independent cross-check.

## Method Selection

| Method | Core equation | Best use | Common failure |
| --- | --- | --- | --- |
| Bottom-up demand | eligible entities x penetration x usage x price | Customer, product, or transaction data exist | Overstated eligibility or adoption |
| Top-down allocation | broad pool x relevant share x scoped share | Rapid boundary check | Inherited definitions and arbitrary shares |
| Supply-side | providers x capacity x utilization x realized price | Capacity-limited markets | Announced capacity treated as active supply |
| Value-based | customer value created x acceptable capture rate | New categories with weak price history | Capture rate chosen to justify a target |
| Analogue | comparable market x normalized adoption or spend ratio | Emerging markets | Weak comparability hidden by neat ratios |
| Constraint-based | minimum of demand, supply, channel, and adoption limits | Realistic serviceable or obtainable market | Constraints omitted from headline TAM |

## Driver Tree Patterns

### Recurring software revenue

```text
Annual supplier revenue
= eligible organizations
x reachable share
x paid adoption
x seats per customer
x annual realized price per seat
```

Keep list price, realized price, and end-customer spend distinct. If channel partners retain margin, state whether the output is billings or supplier revenue.

### Transaction market

```text
Annual gross transaction value
= active buyers
x transactions per buyer per year
x average transaction value
```

```text
Supplier revenue
= gross transaction value
x take rate
```

Do not compare gross transaction value directly with supplier revenue.

### Capacity-constrained market

```text
Serviceable annual volume
= min(qualified demand, operational capacity, accessible input, channel throughput)
```

Use operational capacity, yield, uptime, and utilization rather than nameplate capacity alone.

## Scenario Design

Vary assumptions because evidence differs, not because every input needs three arbitrary values.

1. Hold observed inputs constant unless the scenario changes their period or scope.
2. Use ranges for adoption, utilization, price, conversion, frequency, and growth when evidence is limited.
3. Preserve logical relationships. For example, higher volume may require lower realized price or additional capacity.
4. Name coherent cases such as conservative adoption, base execution, and accelerated adoption.
5. Avoid combining every favorable assumption into a high case unless that joint outcome is plausible.

## Growth Checks

For a base value `B`, annual growth `g`, and `n` periods:

```text
Forecast = B x (1 + g)^n
```

Check the forecast against physical or commercial drivers:

- customer or site growth;
- adoption ceiling and replacement cycle;
- capacity additions and utilization;
- price/mix change versus volume growth;
- regulation or reimbursement timing;
- sales-cycle and implementation constraints.

If the forecast requires share, adoption, or capacity beyond a credible ceiling, revise the growth path rather than merely lowering confidence.

## Reconciliation Protocol

When estimates differ materially:

1. Normalize the year, geography, currency, and inflation basis.
2. Align the metric: customer spend, provider revenue, gross value, units, or profit pool.
3. Align product, customer, use-case, and channel boundaries.
4. Identify whether adoption, utilization, price, or conversion explains the remaining gap.
5. Check for double counting, bundled revenue, channel markups, and inactive capacity.
6. Prefer the estimate with the more decision-relevant boundary and stronger auditable inputs.
7. Keep a wider range if the remaining difference reflects real uncertainty.

Do not average incompatible figures. Reconciliation is an explanation exercise before it is a mathematical one.

## Sensitivity and Break-Even

Rank assumptions by decision impact and evidence weakness. For each critical assumption, calculate the value at which the decision changes.

Examples:

- minimum paid adoption required to recover fixed investment;
- maximum customer acquisition cost consistent with target returns;
- minimum utilization needed for a new facility;
- price floor that maintains target contribution;
- reachable accounts required to support the revenue plan.

A useful conclusion is not only "the market is 200-300 million." It is "the investment clears its threshold above 14% paid adoption; available evidence supports 11-18%, so adoption validation is the next decision gate."
