# Skill evaluation evidence

This directory separates scenario coverage from observed behavior. [manifest.json](manifest.json) defines the tasks and rubrics; [inputs.json](inputs.json) supplies complete fictional raw briefs and critical guardrails. No client data, private casebooks, live submissions or paid model API calls are needed.

## What is recorded now

The four responses below were produced in the current Codex session on 2026-10-01 and reviewed by the same session. They are non-blind self-reviews, not independent forward-tests or evidence that every skill is reliable. The precise model ID was not exposed, so `model` is `not_exposed`. The 12 other scenarios are explicitly unrun.

| Scenario | Saved output | Review record | Score | Mode |
| --- | --- | --- | ---: | --- |
| Compliance software sizing | [Response](runs/2026-10-01/size-compliance-software.md) | [Record](runs/2026-10-01/size-compliance-software.json) | 6/6 | Self-review |
| Recycling capacity | [Response](runs/2026-10-01/size-recycling-capacity.md) | [Record](runs/2026-10-01/size-recycling-capacity.json) | 6/6 | Self-review |
| Distributor value plan | [Response](runs/2026-10-01/vcp-distributor.md) | [Record](runs/2026-10-01/vcp-distributor.json) | 5/6 | Self-review |
| Conflicting merger synergy claims | [Response](runs/2026-10-01/vcp-synergy.md) | [Record](runs/2026-10-01/vcp-synergy.json) | 6/6 | Self-review |

The distributor response loses one point because a stop trigger is not quantified and delivery leads are not assigned. The missing-data synergy case must withhold a committed net total; a confident invented figure would violate its critical guardrails.

## Run and record a scenario

1. Give the assistant the named skill, the scenario prompt and only the raw brief/guardrails. Do not show example answers or existing review conclusions. Use an isolated workspace and do not authorize live external actions as part of a training case.
2. Save the actual response as UTF-8 Markdown. Record its actual generation time and exact model ID if available.
3. Create an unreviewed record; this command does not run a model and will not overwrite an existing record:

```bash
python scripts/evaluate_results.py --prepare size-compliance-software --response build/response.md --record build/run.json --model not_exposed --run-at 2026-10-01T22:22:36+00:00
```

Use your actual run timestamp, not the example timestamp. The record snapshots prompt, raw input, output, rubric, guardrails, project version and a content fingerprint of the skill. Text fingerprints normalize CRLF/LF; the fingerprint is not a Git commit or proof of independent execution.

4. Review the saved output. Set `review` to an object containing `reviewer`, `mode` (`self_review`, `independent_human`, or `independent_model`), `guardrails_reviewed: true`, one `scores` entry per rubric item and an explicit `critical_failures` list. Each score entry uses a zero-based `criterion`, integer `score` (0 absent/incorrect, 1 partial, 2 meets criterion), verbatim `evidence` from the output, and an explanatory `rationale`. A zero score can use empty evidence to explain an omission.
5. Validate the record and inspect its returned status:

```bash
python scripts/evaluate_results.py --check build/run.json
python scripts/evaluate_results.py --summary
```

The pass rule is at least 75% of available points **and no critical violation**; with three criteria, at least 5/6 is needed. `--check` checks record integrity, not whether the reviewer is correct: it can successfully validate a record whose behavioral status is `failed`. It rejects missing metadata, invalid scores and invented evidence quotes. `--summary` reports unrun scenarios and flags historical records whose skill/scenario snapshots no longer match the current files.

For an independent review, give the reviewer raw inputs, skill and actual output but no intended score. Self-review is useful for traceability, but it cannot establish an independent quality benchmark. Adding a file or matching a keyword never counts as a behavioral run.
