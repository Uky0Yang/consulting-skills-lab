# Contributing

Thanks for helping improve Consulting Skills Lab.

## What Fits

Good contributions usually add or improve:

- Practical consulting workflows.
- Issue trees and diagnostic frames.
- Executive-ready templates.
- Evidence standards and risk language.
- Domain-specific reference notes that can be publicly maintained.

Avoid adding generic prompt collections, unverifiable claims, copied proprietary material, or broad frameworks without an execution artifact.

## Skill Quality Bar

Each skill should:

- Solve one recognizable job.
- Have a precise `description` frontmatter field.
- Explain when to load reference files.
- Include a step-by-step workflow.
- Include at least one concrete output template.
- Include guardrails that prevent overclaiming.
- Keep reference material concise and source-aware.
- Include a realistic worked example under `examples/`.
- Include at least two evaluation scenarios with three or more observable rubric criteria.
- Supply complete fictional raw briefs and critical guardrails in `evaluations/inputs.json`; keep recorded runs and self/independent reviews clearly separated.
- Be registered in `data/skill-catalog.json`.

## Validation

Before opening a pull request, run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python scripts/evaluate_results.py --summary
python -m unittest discover -s tests -v
```

If you have the Codex skill creator locally, also run:

```bash
python C:\Users\rayou\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\<skill-name>
```

Adjust the path for your own machine.

## Pull Request Checklist

- [ ] The skill has a clear user-facing purpose.
- [ ] `SKILL.md` has valid frontmatter.
- [ ] `agents/openai.yaml` exists.
- [ ] Referenced files exist.
- [ ] Templates are actionable.
- [ ] No secrets, private client names, or proprietary content are included.
- [ ] Catalog, worked example, and evaluation scenarios are synchronized.
- [ ] Relevant regression tests cover the change.
