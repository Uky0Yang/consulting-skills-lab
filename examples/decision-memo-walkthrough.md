# From brief to decision memo — 30-second walkthrough

![Three stages: decision brief, option analysis, accountable recommendation](../docs/assets/decision-memo-walkthrough.svg)

**Illustrative, fictional case.** This walkthrough explains the existing [warehouse automation example](executive-decision-memo.md). It is not a client deliverable, a timed agent run, or proof of realised savings.

## 0–10 seconds: frame the decision

Copy this prompt into a session with the `executive-decision-memo` skill installed:

```text
Use $executive-decision-memo to assess a warehouse automation renewal.
We can renew for three years now at a 7% discount or run a six-month competition.
Service is acceptable. First list the missing evidence; do not invent benchmarks.
For this fictional worked example only, assume the discount is worth GBP 0.8m,
alternative-provider benefits are an unvalidated GBP 1.5–2.3m range, and a
nine-month extension is negotiable. Label those assumptions in the output.
Compare renew now, compete with extension, and switch immediately.
Finish with the decision, conditions, owners, and a trigger for revisiting it.
```

## 10–20 seconds: compare like with like

| Option | Evidence status | Decision implication |
| --- | --- | --- |
| Renew now | Assumed GBP 0.8m saving; confirm contract baseline | Protects continuity but locks in the service gap |
| Compete with extension | Assumed GBP 1.5–2.3m potential; not bankable | Worth testing if a safe extension is available |
| Switch immediately | Transition cost and service risk unknown | Insufficient basis for approval before peak season |

The important step is distinguishing a quoted discount from an unvalidated alternative. The skill should request total-cost comparability, references and transition evidence, not simply pick the larger number.

## 20–30 seconds: deliver a conditional recommendation

**Decision:** authorise competition only once an extension protects continuity.

- Procurement: negotiate extension terms within two weeks.
- Operations: define service and transition gates within ten days.
- Finance: validate the total-cost model before issuing the RFP.
- Revisit: if no extension is available, reassess the renewal fallback before committing.

Before using a real memo, replace every assumed value, date and owner; verify source support; get the appropriate human decision-maker's approval. Installing a skill does not validate its generated answer.
