# Consulting Skills Lab

Reusable Codex-style consulting skills for strategy, transformation, diligence, executive communication, interviews, and presentation design.

This repository packages practical consulting workflows as portable skill folders. The current release covers scaling agentic AI beyond pilots, mapping markets from messy signals, running rapid commercial due diligence, turning analysis into executive decision memos, building accountable 100-day value plans, coaching case interviews, and formatting analytical slides.

## Who this is for

- Builders who want consulting-grade structure for ambiguous business problems.
- Strategy, product, operations, and transformation teams using AI assistants.
- Solo operators who need repeatable issue trees, memos, workplans, and risk registers.

## Skills

| Skill | Use it for | Main output |
| --- | --- | --- |
| `agentic-ai-transformation-office` | AI transformation, agentic AI scaling, pilot-to-value diagnosis, workflow redesign, governance | Transformation office plan, portfolio scoring, 30/60/90 roadmap |
| `market-map-signal-scan` | Market analysis, competitive landscape, trend scan, opportunity gap assessment, category entry | Market map, signal register, opportunity gap matrix, decision gate |
| `commercial-due-diligence-sprint` | Market scan, target assessment, investment memo, value creation thesis | Diligence issue tree, evidence plan, IC-ready synthesis |
| `executive-decision-memo` | Board memo, CEO update, steering committee note, decision recommendation | Concise recommendation memo with options, risks, and next actions |
| `value-creation-plan` | Post-diligence 100-day plans, synergy plans, strategic execution, benefit tracking | Owned initiative portfolio, value bridge, and 100-day roadmap |
| `consulting-case-interview-coach` | Mock cases, case math, interviewer-style feedback, practice planning | Interactive interview, anchored scorecard, targeted drill |
| `consulting-template-style` | Consulting decks, chart books, slide redesign, executive presentation formatting | MBB-informed style selection, layout map, formatting and QA rules |

## Install

Copy the skill folders you want into your local Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\agentic-ai-transformation-office "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\skills\market-map-signal-scan "$env:USERPROFILE\.codex\skills\"
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
```

If you have the local Codex skill creator installed, you can also run its quick validator against each skill folder.

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

## Contributing

New skills should include:

- A clear trigger description in `SKILL.md`.
- At least one reusable workflow.
- Concrete output templates.
- Guardrails for overclaiming, weak evidence, and regulated domains.
- Reference files when the workflow depends on external context.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT
