# Consulting Skills Lab

[![Validate](https://github.com/Uky0Yang/consulting-skills-lab/actions/workflows/validate.yml/badge.svg)](https://github.com/Uky0Yang/consulting-skills-lab/actions/workflows/validate.yml)
[![Latest release](https://img.shields.io/github/v/release/Uky0Yang/consulting-skills-lab)](https://github.com/Uky0Yang/consulting-skills-lab/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Reusable Codex-style consulting skills for strategy, transformation, diligence, executive communication, interviews, and presentation design.

This repository packages practical consulting workflows as portable skill folders. The current release covers scaling agentic AI beyond pilots, mapping markets from messy signals, triangulating market size, running rapid commercial due diligence, turning analysis into executive decision memos, building accountable 100-day value plans, coaching case interviews, and formatting analytical slides.

## Who this is for

[![A brief becomes an options analysis and an accountable decision](docs/assets/decision-memo-walkthrough.svg)](examples/decision-memo-walkthrough.md)

[30-second walkthrough: input → analysis → decision memo](examples/decision-memo-walkthrough.md). Fictional inputs are clearly labelled; this demonstrates the output structure, not a real client outcome.

- Builders who want consulting-grade structure for ambiguous business problems.
- Strategy, product, operations, and transformation teams using AI assistants.
- Solo operators who need repeatable issue trees, memos, workplans, and risk registers.

## Skills

| Skill | Use it for | Example |
| --- | --- | --- |
| [`agentic-ai-transformation-office`](skills/agentic-ai-transformation-office/SKILL.md) | AI transformation, pilot-to-value diagnosis, workflow redesign, governance | [90-day pilot reset](examples/agentic-ai-transformation-office.md) |
| [`market-map-signal-scan`](skills/market-map-signal-scan/SKILL.md) | Market analysis, competitive landscape, signal confidence, opportunity gaps | [Contact-center QA market](examples/market-map-signal-scan.md) |
| [`market-sizing-sanity-check`](skills/market-sizing-sanity-check/SKILL.md) | TAM/SAM/SOM, demand sizing, capacity and growth sanity checks | [Compliance software sizing](examples/market-sizing-sanity-check.md) |
| [`commercial-due-diligence-sprint`](skills/commercial-due-diligence-sprint/SKILL.md) | Target assessment, investment memo, growth and customer diligence | [Vertical SaaS diligence](examples/commercial-due-diligence-sprint.md) |
| [`executive-decision-memo`](skills/executive-decision-memo/SKILL.md) | Board memo, steering note, decision recommendation | [Vendor renewal decision](examples/executive-decision-memo.md) |
| [`value-creation-plan`](skills/value-creation-plan/SKILL.md) | 100-day plans, synergies, initiative ownership, benefits tracking | [Distributor value plan](examples/value-creation-plan.md) |
| [`consulting-case-interview-coach`](skills/consulting-case-interview-coach/SKILL.md) | Mock cases, case math, anchored feedback, practice planning | [Profitability case](examples/consulting-case-interview-coach.md) |
| [`consulting-template-style`](skills/consulting-template-style/SKILL.md) | Consulting decks, chart books, slide redesign, formatting QA | [Market-entry deck](examples/consulting-template-style.md) |

## Install

List the available skills:

```bash
python scripts/install_skills.py --list
```

Install selected skills into the default Codex skills directory:

```bash
python scripts/install_skills.py --skills market-sizing-sanity-check value-creation-plan
```

Install all skills, or preview the operation first:

```bash
python scripts/install_skills.py --all
python scripts/install_skills.py --all --dry-run
```

Use `--destination <path>` for a custom directory and `--force` to replace an existing selected skill. The installer validates every requested name before copying anything.

### Manual installation

Copy the skill folders you want into your local Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\agentic-ai-transformation-office "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\skills\market-map-signal-scan "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\skills\market-sizing-sanity-check "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\skills\commercial-due-diligence-sprint "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\skills\executive-decision-memo "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\skills\value-creation-plan "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\skills\consulting-case-interview-coach "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\skills\consulting-template-style "$env:USERPROFILE\.codex\skills\"
```

Then start a new Codex session and trigger a skill by name, for example:

```text
Use $agentic-ai-transformation-office to diagnose why our AI pilots are not scaling.
```

```text
Use $market-map-signal-scan to analyze the market for AI meeting assistants and identify credible opportunity gaps.
```

```text
Use $market-sizing-sanity-check to triangulate this market estimate and identify which assumptions could change the entry decision.
```

```text
Use $consulting-case-interview-coach to run a hard candidate-led case and score my performance.
```

```text
Use $value-creation-plan to turn this investment thesis into a finance-validated 100-day value creation plan.
```

```text
Use $consulting-template-style to redesign this market analysis deck in a Bain-informed style.
```

## Validate

Run the repository validator:

```bash
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

If you have the local Codex skill creator installed, you can also run its quick validator against each skill folder.

The repository includes two realistic evaluation scenarios per skill in [`evaluations/manifest.json`](evaluations/manifest.json). Each scenario defines observable rubric criteria and a pass rule for forward-testing skill behavior.

## Release Packages

Every tagged release contains one ZIP per skill, an all-skills bundle, and `SHA256SUMS.txt`. Maintainers can reproduce the artifacts locally:

```bash
python scripts/package_release.py --output dist --version 1.0.0
```

## Design Principles

- Decision first: outputs should help someone decide, not just summarize.
- Evidence aware: confidence and missing evidence must be visible.
- Workflow based: AI and transformation work should change operating routines, not only introduce tools.
- Practical artifacts: every skill should provide templates a team can use immediately.
- Public-source friendly: references summarize public signals without copying long passages.
- Original by default: practice cases are newly written and third-party casebooks are linked, not mirrored.
- Rights aware: presentation rules are distilled from reference decks without redistributing source templates, logos, or client material.

## Current Signals Used

The AI transformation skill references public 2025-2026 signals from McKinsey, BCG, Bain, and industry reporting about AI value realization, agentic AI adoption, and organizational barriers to scaling. These references are used as context, not as proprietary methodology.

The case-interview coach includes an official-source guide checked in July 2026. It links to current firm and consulting-club resources while keeping copyrighted casebooks out of the repository.

The repository also exposes a versioned machine-readable catalog at [`data/skill-catalog.json`](data/skill-catalog.json) so installers and documentation tools can discover skill paths, descriptions, examples, outputs, and tags without parsing the README.

## Contributing

New skills should include:

- A clear trigger description in `SKILL.md`.
- At least one reusable workflow.
- Concrete output templates.
- Guardrails for overclaiming, weak evidence, and regulated domains.
- Reference files when the workflow depends on external context.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Security and responsible disclosure guidance is in [SECURITY.md](SECURITY.md). Community participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

MIT
