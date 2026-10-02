# Warehouse automation: provisional decision brief

**Decision required:** By day 14, the COO must decide whether the evidence supports the proposed £500,000 robot investment, a narrower feasibility/pilot step, a least-change response, or no investment yet. The present brief does not establish that robots will eliminate late orders. It also does not establish that robots are unsuitable.

Status: provisional; no sponsor agreement, service target, ROI hurdle or investment approval is evidenced. This is a fictional scenario. Day 0 means the agreed kickoff date; calendar dates and role acceptance remain to be confirmed.

## 1. Mandate, objective and boundaries

The stated assignment is to assess the robot proposal within 14 days, not to prove the operations director's preferred solution. The objective is fewer late customer orders; purchasing robots is one possible intervention. Retain the robot evaluation and test alternative delay mechanisms only insofar as they affect that investment decision. Any broader warehouse redesign requires separate scope approval.

The COO owns the investment decision. The operations director sponsors the robot proposal and is the proposed accountable evidence-plan lead. Finance should own the economic definitions and appraisal; the COO must confirm these assignments.

In scope: the same warehouse, the supplied comparable weeks A and B, and a representative recent order-level sample sufficient to distinguish receipt/stock availability, picking, packing/handoff and carrier timing. Include staffing, SKU mix and exception/rework effects on effective throughput. Assess robot suitability, implementation constraints and whole-life costs using already authorized internal information. Separate any assumptions requiring later vendor verification.

Out of scope: vendor contact, procurement, system or operational changes, wider-site rollout, or claims that a two-week diagnostic establishes long-run causal benefits. The proposed £500,000 is requested investment, not an approved budget or proven total cost of ownership.

The service metric must be agreed before judging success. Clarify whether the existing on-time measure means dispatched by a cutoff or delivered by the customer promise, its denominator, exclusions and reporting window. Until then, preserve the existing published measure; do not replace it with an easier dispatch measure or exclude difficult orders to manufacture an improvement. If customer delivery is the promise, track on-time delivery as the outcome and stage adherence as diagnostics. Baseline and target for approval are **to agree**, not invented.

## 2. What is known—and what it does not prove

| Item | Supplied evidence / calculation | Interpretation limit |
| --- | --- | --- |
| Orders received | A: 800; B: 850; increase 50, or 6.25% | Timing, eligible demand and work content are unknown |
| Orders shipped | A: 760; B: 780; increase 20, or 2.63% | Not necessarily the same order cohorts as receipts |
| On time | A: 90%; B: 86%; decline 4 percentage points | Denominator, promise definition and cohort alignment are missing; do not infer exact late-order counts |
| Receipts minus shipments | A: 40; B: 70 | Potential pressure on backlog, not verified backlog growth: reconcile opening/closing backlog, cancellations and other flows |
| Scheduled picking capacity | 1,000 orders/week | Not verified effective capacity or measured utilization; actual staffed hours and work mix are absent |
| Delay explanations | Supervisor: picking; customer service: carrier cutoffs | Rival attributed claims, not proven causes |

Source IDs for handoff: W-A and W-B = supplied weekly reports; C-CAP = scheduled capacity claim; H-PICK = supervisor attribution; H-CARRIER = customer-service attribution. Underlying records have not been inspected. SKU mix, arrival times, stockouts and actual cycle times remain unknown.

## 3. Decision-relevant issue tree

Start with the accounting bridge: closing backlog = opening backlog + eligible receipts − shipped orders − cancellations/other exits ± reconciled adjustments. Then locate where an order loses the time needed to meet its unchanged customer promise.

1. **Demand and work entering the flow:** order arrival versus promise/cutoff; SKU/line-count complexity; stock availability; exceptional orders. These change the required work and available time.
2. **Effective internal capacity and flow:** actual productive staffing × demonstrated processing rate, adjusted for work mix; queues and waiting across picking/packing; interruptions, exceptions and rework. Scheduled capacity is only a planning reference.
3. **Outbound handoff and external fulfillment:** packing-ready timestamp versus carrier cutoff, pickup reliability and carrier transit/service performance where the customer promise includes delivery.

Use these branches to test mechanisms, not as a claim of perfect MECE coverage. Assign each late order one **first missed checkpoint** for a non-double-counted stage count; retain secondary contributing causes separately. Arrival timing can interact with staffing and carrier cutoff, so do not add overlapping cause counts. Keep an unexplained/residual category visible and inspect it rather than forcing it into picking. Robots belong in the option comparison, not as a sibling cause in this tree.

## 4. Rival hypotheses and tests

| Hypothesis | Evidence now | What would challenge it? | Test / required definition | Decision consequence |
| --- | --- | --- | --- | --- |
| H1: picking is the binding constraint on late orders | Supervisor attribution; shipments lag receipt growth | Many late orders were picked in time, or pick queues are small after controlling for staffing/mix | Trace order timestamps and pick queues; compare work-weighted demand with actual staffed productive hours by shift | Only a demonstrated, robot-addressable picking constraint supports advancing robot feasibility |
| H2: orders are ready but miss outbound cutoffs / carrier service | Customer-service attribution | Late orders mostly missed their internal pick/pack checkpoint before a timely carrier pickup | Match ready, handoff, cutoff, pickup and relevant delivery timestamps to the promise | An outbound constraint reduces the case that picking robots solve the service symptom |
| H3: labor coverage, not equipment, explains effective capacity loss | Staffed hours absent; scheduled capacity does not resolve this | Adequate productive staffing is present during demand peaks, but picking remains constrained | Reconcile scheduled versus actual hours, absences, skill coverage and arrival peaks; adjust for mix | Compare a staffing/process response as a least-change candidate; do not implement it in this diagnostic |
| H4: stockouts, mix or exception/rework drive the deterioration | These data are missing; no positive evidence yet | Stock is available and complexity/exception rates do not explain late-order patterns | Stratify traced orders by availability, SKU/line complexity and exception type; compare weeks/shifts | May change automation design or redirect the initial intervention; no data is not evidence of no issue |

These are observational tests. Differences across shifts or order cohorts are not automatically causal effects; retain confounders and data-quality limits. No leading cause can yet be chosen reliably.

## 5. Owned two-week evidence plan

Assignments below are proposed, not accepted. Do not contact anyone or access new private material without the necessary permission.

| Due | Proposed accountable role | Deliverable / verification | Stop or escalation rule |
| --- | --- | --- | --- |
| D1–D2 | COO with operations and finance leads | Confirm decision options, original service definition, target, economic hurdle, scope, data permission and calendar; reconcile W-A/W-B definitions | If targets or metric remain unresolved on D2, escalate to COO. Continue factual diagnosis, but do not declare a pass/fail investment result |
| D3–D4 | Operations analyst; warehouse supervisor accountable | Receipt/shipment/backlog bridge; actual staffing; time-stamped order sample with both on-time and late cases across relevant shifts/mix; document completeness and exclusions | Missing timestamps or irreconcilable counts by D4 trigger a narrower measurement/feasibility decision, not an assumed cause |
| D5–D7 | Operations director; customer-service/logistics lead for outbound records | First-missed-checkpoint analysis, rival-hypothesis tests, exceptions and counterexamples; reconcile counts to the original denominator | If multiple constraints or unexplained residuals remain material, retain mixed/unknown attribution and do not allocate all benefit to robots |
| D8–D10 | Operations engineering role with finance lead | Robot-addressable work, feasibility/capacity limits, implementation downtime and provisional whole-life cost range using authorized sources; compare no-change and least-change options | If suitability or total costs require unavailable vendor data, label the investment appraisal incomplete and propose a later authorized feasibility step |
| D11–D12 | Finance lead | Auditable option comparison: service mechanism, time horizon, costs, benefit scenarios, downside, dependencies and sensitivity to volume/staffing/mix; distinguish released time from cash savings | Do not book hypothetical labor hours as savings. If the required ROI hurdle or cost/benefit basis is absent, do not present a fabricated ROI |
| D13–D14 | COO; operations director prepares pack | Decide approve / narrower study or pilot / alternative investigation / defer; record evidence, uncertainty and conditions | Approve only against agreed criteria and sufficient option-specific evidence. Otherwise narrow or defer the decision and state remaining exposure |

## 6. Gate for the day-14 decision

Advance the robot investment only if the packet connects a material late-order mechanism to work robots can address, shows feasible implementation and credible economics against the COO's agreed criteria, and exposes counterevidence and downside. A targeted pilot may still be justified where feasibility is promising but service/economic effects are unverified; its spend, measures and authorization would be a separate decision.

If the evidence instead shows timely picking with late carrier handoff, or a staffing/stock/mix constraint that robots do not address, that would reverse a picking-led investment hypothesis. If evidence is simply missing, the conclusion is **insufficient basis to approve**, not **robots have been disproven**. No approval or operational change is implied by this draft.

---

Generation provenance: 2026-10-02 04:12:08 UTC. Model ID: not_exposed. Produced from the raw fictional brief and critical guardrails, the complete business-problem-framing SKILL.md, its framing-methods reference and blank output templates. No examples, tests, intended answers or existing evaluation outputs were inspected.
