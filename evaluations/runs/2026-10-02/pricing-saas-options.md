# SaaS pricing options: unit economics and bounded validation plan

**Decision recommendation:** retain £180/month as the live offer until an authorized test supplies demand and retention evidence. The £216 option has stronger modeled contribution if accounts and costs are unchanged; the £162 option needs a material increase in paying accounts merely to preserve current contribution. Neither result establishes willingness to pay or a causal price benefit.

This is a fictional, monthly steady-state comparison—not a valuation, accounting opinion, demand forecast or authorization to change prices. Buyer segment, perceived value, competing offers, sales-cycle length and approval authority have not been supplied.

## 1. Definitions and normalized inputs

The pricing unit remains one SaaS account per month, with the same offer/packaging. All money is GBP. Prices are realized **net** monthly account revenue; no annual-to-monthly conversion or tax uplift is applied. Confirm the commercial tax/contract presentation before any live test.

Included recurring contribution costs are £40 infrastructure + £20 support = **£60/account/month**. These are the full included costs and are held constant as the supplied scenario requires. Contribution is net revenue less these named costs; it is not automatically accounting gross profit or cash flow. Fixed costs are £18,000/month and exclude these allocated costs, so do not deduct the £60 again below contribution.

There are 220 current accounts. The matched monthly fully loaded acquisition spend is £30,000 for 50 newly acquired accounts, with no lag mismatch: **CAC = £30,000 / 50 = £600**. The 220-account installed base is not the CAC denominator. For the comparison, CAC remains £600 under each option; that is a scenario hold, not evidence that the price change leaves acquisition unchanged.

Monthly logo churn is 2%, supplied as a stable **assumption**, not verified cohort behavior. Hold it fixed across options only for the proxy calculation. No annual churn figure is used and no churn rate is divided by 12.

## 2. Auditable option comparison

| Monthly metric | Current £180 | Increase to £216 | 10% discount to £162 |
| --- | ---: | ---: | ---: |
| Net price/account | £180 | £216 | £162 |
| Included recurring cost/account | £60 | £60 | £60 |
| **Contribution/account** | **£120** | **£156** | **£102** |
| Contribution margin | 66.67% | 72.22% | 62.96% |
| CAC, held constant | £600 | £600 | £600 |
| **Simple contribution-adjusted CAC recovery** | **5.00 months** | **3.85 months** | **5.88 months** |
| Operating break-even against supplied £18,000 fixed costs | 150 accounts | 116 accounts | 177 accounts |
| Monthly contribution at 220 accounts | £26,400 | £34,320 | £22,440 |
| Contribution less supplied fixed costs at 220 | £8,400 | £16,320 | £4,440 |
| Constant-monthly-churn contribution LTV proxy | £6,000 | £7,800 | £5,100 |
| **Accounts needed to preserve baseline £26,400 monthly contribution** | **220** | **170** | **259** |

Calculations:

- Contribution = price − £60.
- Contribution margin = contribution / net price.
- Simple recovery = £600 / positive monthly contribution. This uses £120/£156/£102, **not revenue-only recovery**. It ignores exits before recovery, billing timing and working capital; actual cohort cash recovery needs those data.
- Operating break-even = ceiling(£18,000 / positive monthly contribution). This assumes stable costs/mix and feasible service capacity.
- LTV proxy = monthly contribution / 0.02. It assumes constant contribution and monthly logo-loss probability, no expansion/contraction dynamics and stable retention; it is not a cohort forecast. The 2% assumption is unverified, so use the proxy as sensitivity information, not a lifetime-value promise or universal investment gate.
- Preservation accounts = ceiling(£26,400 / new contribution): ceiling(169.2308) = 170 at £216; ceiling(258.8235) = 259 at £162.

The surplus line covers only the **supplied fixed-cost definition**. The brief does not specify whether matched acquisition spend is already included in that £18,000 cost base. Reconcile this with finance before calling any remainder fully loaded operating profit; do not silently double count or omit acquisition expense. CAC recovery separately describes recovery of acquisition investment. These calculations are not a cash-flow statement.

The standard-library calculator was run on three explicit inputs saved alongside this memo: pricing-input-current.json, pricing-input-increase.json and pricing-input-discount.json. They use period=month, currency=GBP, prices 180/216/162, named costs 40+20, fixed costs 18000, matched acquisition spend 30000, new customers 50, customers 220 and logo churn 0.02. All three runs completed successfully. Preservation thresholds were independently checked from the baseline contribution.

## 3. What could reverse the modeled preference?

At £216, 170 accounts contribute £26,520; 169 contribute £26,364, below the baseline. Thus this static comparison allows 50 fewer accounts than 220 while still preserving aggregate contribution. The exact unrounded break-even volume fraction is £120/£156 = 76.92% of baseline. **This is an active-volume threshold for one comparable month, not an observed retention result or permission to accept churn.**

At £162, 259 accounts contribute £26,418; 258 contribute £26,316. The discount needs 39 additional accounts, about 17.73% more after integer rounding. The continuous threshold is £120/£102 = 117.65% of baseline. More discounted conversions are not sufficient evidence unless they produce comparable realized, retained contribution after acquisition and service costs.

Unknown demand response can reverse the £216 preference. Additional discounts/refunds, heavier usage, support work or different acquisition costs can also erase its modeled benefit. The discount could be preferable only if observed acquisition/retention economics compensate for its £18/account lower contribution. Both alternatives require service-capacity checks. Holding £60 costs and 2% churn fixed is not a claim that pricing has no effect on either.

There is no willingness-to-pay or elasticity evidence in the brief. Ask what buyer value the monthly account price captures, whether usage varies materially by segment, what buyers compare it against, and how predictable the bill must be. Do not introduce a usage or hybrid package without a separate billing-meter and allowance decision.

## 4. Proposed validation plan—not an approved live test

**Before launch:** the pricing lead should obtain sponsor approval, finance review of cost/acquisition definitions, and contractual/tax review. Use permitted, minimized historical cohort data to check sales-cycle length, segments, realized discounts, usage/support and monthly logo retention. If the sales cycle cannot fit the proposed enrollment window, amend the design before approval; do not assume a short test can capture purchase behavior.

Proposed design:

| Element | Bounded proposal |
| --- | --- |
| Eligible cohort | Comparable new, non-enterprise monthly-account prospects in one preselected segment/channel; same package and service. Exclude existing accounts, renewals, custom contracts and annual billing. Confirm eligibility and randomization feasibility before launch |
| Alternatives | Random assignment to £180 control, £216 or £162; no differential features/service. Quotes and billing occur only after explicit authorization and transparent terms |
| Exposure cap | At most 120 eligible prospect offers: 40 per arm, 80 exposed to alternatives. This is an exposure limit, not a power calculation; insufficient precision may require an inconclusive decision |
| Cost cap | Proposed additional test/implementation spend no more than £2,500, subject to approval. At most 40 discounted paying accounts would concede £2,160 versus baseline over three monthly bills (£18 × 40 × 3), before any demand offset. Conversion opportunity loss for the higher price is unquantified; the offer-count cap limits exposure, not all monetary risk |
| Outcome window | Up to six weeks of enrollment, subject to the sales-cycle check, then observe each paid account for three full monthly billing periods. Set a final calendar review date before launch. This cannot validate lifetime or annual renewal behavior |
| Primary outcome | Cumulative realized contribution **less matched acquisition spend per randomized eligible prospect**, including non-buyers, refunds and actual recurring service costs. Match cohort/window/channel definitions; also report paid-account contribution separately |
| Secondary measures | Paid conversion, activation, realized net price, actual CAC, monthly logo retention, usage/support cost and complaints. Stated willingness to pay is hypothesis evidence, not paid conversion |
| Owners | Pricing lead: experiment execution/design; finance: contribution and CAC reconciliation; customer-success/product lead: service and retention monitoring; accountable sponsor: approve test and later decision. Names and authority remain to confirm |

Proposed decision gates, to be approved in advance:

- Do not recommend broad rollout unless the candidate improves observed acquisition-adjusted cumulative contribution per eligible prospect versus control on comparable exposure and its retention/service outcomes meet pre-agreed limits. Set the uncertainty standard and numerical retention/complaint tolerances before enrolling anyone; they are not supplied here.
- Use the 76.92%/117.65% active-volume ratios as a static economic check under equal costs, not as observed conversion or churn forecasts. Recalculate thresholds from realized costs and discounts if they differ from the scenario.
- If cohorts are too small, the sales cycle incomplete, costs unreconciled or results unstable at review, retain the current offer and report inconclusive evidence; do not turn a directional pattern into a causal claim.

Pause enrollment in an alternative arm if its realized contribution becomes nonpositive, a contractual/billing problem appears, or a pre-agreed contribution/retention/service limit is breached. Revert **future uncommitted offers** to the approved baseline while investigating; honor already accepted test terms and do not unilaterally reprice enrolled customers. Any rollout beyond the approved cohort requires a new decision.

Handoff: provide the normalized inputs, calculation definitions, explicit constant-volume/cost/churn assumptions, measured cohort outcomes and unresolved acquisition-cost classification. This memo does not authorize outreach, billing or a blanket price change.

---

Generation provenance: 2026-10-02 04:17:11 UTC. Model ID: not_exposed. Produced from the raw fictional brief and critical guardrails, the complete pricing-unit-economics SKILL.md, its economics-methods reference, blank experiment template and portable calculator. No fictional training input, examples, tests, intended answers or existing evaluation outputs were inspected.
