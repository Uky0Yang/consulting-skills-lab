# Agent Guide

This repository contains portable consulting skills.

## Commands

- Install development validation dependency:
  - `python -m pip install -r requirements-dev.txt`

- Validate repository structure:
  - `python scripts/validate_skills.py`
- Run regression tests:
  - `python -m unittest discover -s tests -v`
- Recalculate fictional examples and inspect behavioral evidence:
  - `python scripts/check_example_calculations.py`
  - `python scripts/evaluate_results.py --summary`
- Smoke-test installation:
  - `python scripts/install_skills.py --all --destination build/skills --dry-run`
- Build release packages:
  - `python scripts/package_release.py --output dist --version <version>`
- Run local Codex skill validation when available:
  - `python C:\Users\rayou\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\<skill-name>`

## Rules

- Keep each skill self-contained.
- Do not include private client data, credentials, or proprietary consulting material.
- Add references only when the skill explicitly needs them.
- Prefer practical output templates over abstract framework lists.
- Keep public-source notes summarized and linked.
- Keep the catalog, examples, evaluation manifest, and skill folders synchronized.
- Keep scenario coverage distinct from recorded outputs and independent evaluation; never infer a behavioral pass from static tests.
