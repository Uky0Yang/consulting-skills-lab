# Original Practice Cases

These cases were created for this repository. They do not reproduce any third-party casebook.

## Case 1: Northstar Claims

**Format:** candidate-led  
**Difficulty:** medium  
**Primary skills:** profitability, operations, AI investment, break-even math

### Opening prompt

Northstar is a regional property insurer processing 600,000 claims per year. Its claims-handling cost rose from $90 million to $108 million over two years while claim volume stayed flat. The COO is considering an AI-assisted triage system and wants to know whether to launch it.

### Clarifications

- Objective: restore annual claims-handling cost to $90 million or less within two years.
- Scope: handling expense only; claim payouts are out of scope.
- The system recommends routing and flags missing information. Human adjusters retain final authority.
- Up-front implementation cost is $12 million.

### Expected structure

Accept any tailored structure that covers:

1. Cost increase by activity, volume, and unit cost.
2. AI impact by eligible claims, adoption, productivity, and quality.
3. Economics, implementation risk, and operating-model requirements.

The best starting point is locating the $18 million cost increase.

### Data checkpoint 1

| Cost pool | Two years ago | Current |
| --- | ---: | ---: |
| Intake and document review | $24m | $39m |
| Adjuster investigation | $42m | $43m |
| Quality and appeals | $12m | $14m |
| Management and systems | $12m | $12m |

**Required insight:** Intake and document review explains $15 million, or 83%, of the increase.

If asked, intake headcount grew after new documentation rules; productivity fell from 30 to 20 claims per employee per day.

### Data checkpoint 2

The proposed tool applies to 70% of claims. In that eligible group, it can reduce intake labor hours by 45%. Current intake and document-review cost is $39 million, all labor. Ongoing software and model-oversight cost is $5 million per year.

**Calculation:** $39m x 70% x 45% = $12.285m gross savings. Net recurring savings = $7.285m.

**Payback:** $12m / $7.285m = about 1.65 years.

**Required insight:** The tool meets a two-year payback threshold, but recurring cost would fall only to about $100.7 million if nothing else changes. It does not by itself restore the $90 million target.

### Twist

The pilot increased appeal rates from 3% to 4% for eligible claims. Each incremental appeal costs $180 to handle.

**Calculation:** 600,000 x 70% x 1% x $180 = $756,000 additional annual cost.

Adjusted recurring savings are about $6.5 million and payback is about 1.84 years.

### Strong recommendation

Launch a controlled rollout because adjusted payback remains under two years, but do not present it as the full cost solution. Add appeal-rate guardrails, redesign intake rules, and identify a further roughly $11.5 million of savings to reach the $90 million goal.

### Hints

1. Which cost pool created most of the increase?
2. Separate eligible volume, productivity impact, and ongoing cost.
3. Reconcile the projected savings with the client's absolute cost target.

---

## Case 2: GridLoop Batteries

**Format:** candidate-led  
**Difficulty:** hard  
**Primary skills:** market entry, capacity economics, regulation, strategic judgment

### Opening prompt

GridLoop manufactures industrial batteries in Europe. Management is considering building a lithium-ion battery recycling plant in the United Kingdom. The CEO wants a recommendation on whether to enter and at what initial scale.

### Clarifications

- Decision horizon: five years.
- Objective: achieve at least a 15% return on invested capital by year five while securing recycled material for GridLoop's factories.
- GridLoop has no recycling operations today.
- Assume all figures are real and ignore tax.

### Expected structure

1. Available feedstock and customer demand.
2. Competitive capacity and regulation.
3. Unit economics, plant scale, and investment return.
4. Capabilities, partnerships, and execution risks.

### Data checkpoint 1

UK recyclable battery feedstock is 80,000 tonnes today and is expected to grow 20% annually. Existing recyclers can process 70,000 tonnes. One competitor has announced a 20,000-tonne plant opening in year three.

**Calculation:** Year-five feedstock = 80,000 x 1.2^4, approximately 166,000 tonnes.

**Required insight:** After announced capacity, the apparent year-five gap is about 76,000 tonnes, but feedstock availability is not the same as contracted supply.

### Data checkpoint 2

| Plant option | Capacity | Investment | Fixed operating cost | Variable cost |
| --- | ---: | ---: | ---: | ---: |
| Modular | 25,000 t | £45m | £6m/year | £1,050/t |
| Full scale | 60,000 t | £90m | £10m/year | £900/t |

Recovered material and recycling fees provide combined revenue of £1,450 per tonne. Assume 80% utilization in year five.

**Calculations:**

- Modular operating profit: 25,000 x 80% x (£1,450 - £1,050) - £6m = £2m; ROIC = 4.4%.
- Full-scale operating profit: 60,000 x 80% x (£1,450 - £900) - £10m = £16.4m; ROIC = 18.2%.

**Required insight:** Only full scale clears the financial hurdle, but it requires 48,000 tonnes of secured annual input at 80% utilization.

### Twist

Proposed regulation may require 20% of recovered material to be sold through a government allocation mechanism at £250 per tonne below the assumed value.

**Calculation:** 48,000 x 20% x £250 = £2.4 million annual downside. Adjusted operating profit is £14 million and ROIC is 15.6%.

### Strong recommendation

Proceed conditionally with the full-scale plant because it remains slightly above the return hurdle under the regulatory downside. Make final investment contingent on long-term feedstock contracts for at least 48,000 tonnes, technology-performance guarantees, and clarity on allocation rules.

### Hints

1. Estimate the year-five supply-demand gap before choosing capacity.
2. Use year-five utilization to calculate operating profit and ROIC.
3. Identify the commercial commitment needed to make the scale economics real.

---

## Case 3: Harbor City Heat

**Format:** interviewer-led  
**Difficulty:** medium  
**Primary skills:** public sector, climate adaptation, prioritization, cost-effectiveness

### Opening prompt

Harbor City experienced a record heatwave that caused an estimated 240 excess hospital admissions in its most vulnerable districts. The mayor has £18 million for a two-year heat-adaptation program and wants to minimize future heat-related admissions.

### Question 1: Structure

Ask the candidate to structure the decision.

Strong answers cover vulnerable populations and locations, intervention effectiveness, reach and implementation speed, economics, and delivery risks.

### Question 2: Portfolio math

| Intervention | Maximum scale | Cost per unit | Admissions avoided per unit |
| --- | ---: | ---: | ---: |
| Cool roofs for social housing | 12,000 homes | £1,000/home | 1 per 200 homes |
| Cooling centers | 30 centers | £200,000/center | 3 per center |
| Home outreach for high-risk residents | 20,000 residents | £300/resident | 1 per 250 residents |

Ask for cost per admission avoided:

- Cool roofs: 200 x £1,000 = £200,000.
- Cooling centers: £200,000 / 3 = about £66,700.
- Outreach: 250 x £300 = £75,000.

### Question 3: Allocate the budget

A cost-effectiveness-only allocation funds all 30 cooling centers for £6 million, all outreach for £6 million, and 6,000 cool roofs for £6 million.

Expected avoided admissions:

- Cooling centers: 90.
- Outreach: 80.
- Cool roofs: 30.
- Total: 200.

Accept alternative portfolios if the candidate quantifies the trade-off and considers access.

### Twist

Attendance data show that residents more than three kilometers from a cooling center are 60% less likely to use one. Half of vulnerable residents live more than three kilometers from the proposed sites.

**Required insight:** Raw cost-effectiveness overstates cooling-center impact. The city should adjust expected utilization, change site selection, add transport, or rebalance toward household interventions.

### Strong recommendation

Do not approve the initial portfolio unchanged. Preserve cooling centers as the most cost-effective intervention, but optimize their locations and reserve funding for transport or mobile access. Use outreach for high-risk residents and cool roofs as durable coverage for neighborhoods that centers cannot serve.

### Hints

1. Compare interventions on a common outcome.
2. Maximize impact subject to the scale limits.
3. Test whether modeled reach translates into real utilization.

---

## Case 4: Meridian Cloud ERP

**Format:** interviewer-led  
**Difficulty:** hard  
**Primary skills:** digital transformation, NPV, risk, sequencing

### Opening prompt

Meridian Foods operates 18 factories across Europe on fragmented legacy ERP systems. The board is deciding between a single big-bang cloud migration and a phased rollout. Recommend an approach.

### Question 1: Decision criteria

Strong answers cover business value, total cost, implementation risk, operational disruption, data readiness, organizational capacity, and time to benefit.

### Question 2: Economics

| Option | Up-front program cost | Annual benefit from completion | Time to completion | Probability of successful completion |
| --- | ---: | ---: | ---: | ---: |
| Big bang | €72m | €28m | 2 years | 65% |
| Phased | €84m | €25m | 3 years | 85% |

Use a simplified five-year view from today. Ignore discounting. Benefits begin after completion and continue through year five.

**Expected values:**

- Big bang: -€72m + 65% x (3 x €28m) = -€17.4m.
- Phased: -€84m + 85% x (2 x €25m) = -€41.5m.

**Required insight:** Neither option pays back within five years on risk-adjusted direct benefits. Big bang is financially less negative, but the decision requires considering downside severity and benefits beyond year five.

### Twist

A failed big-bang cutover could halt production for two weeks, with €9 million contribution loss per week. A failed phase affects only one factory, with €1.5 million contribution loss.

### Strong recommendation

Choose a phased rollout unless Meridian can materially improve big-bang readiness. The five-year direct economics are weak for both, and the concentrated operational downside makes big bang unattractive. Start with two representative factories, set data and adoption gates, and revisit the remaining sequence after measured benefits.

### Hints

1. Adjust benefits for both timing and success probability.
2. Compare not only expected value but also the shape of failure.
3. Name the evidence a pilot must produce before scaling.
