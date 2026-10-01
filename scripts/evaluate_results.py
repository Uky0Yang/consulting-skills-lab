"""Record and validate reviewable skill evaluations; this script does not call an LLM."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def skill_digest(name: str, root: Path = ROOT) -> str:
    directory = root / "skills" / name
    if not directory.is_dir():
        raise ValueError(f"skill source directory is missing: {name}")
    hasher = hashlib.sha256()
    for path in sorted(directory.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            content = path.read_bytes()
            if path.suffix in (".md", ".yaml", ".json", ".py"):
                content = content.replace(b"\r\n", b"\n")
            hasher.update(path.relative_to(directory).as_posix().encode("utf-8") + b"\0")
            hasher.update(hashlib.sha256(content).digest())
    return hasher.hexdigest()


def load_scenarios(root: Path = ROOT) -> dict[str, dict]:
    manifest = json.loads((root / "evaluations/manifest.json").read_text(encoding="utf-8"))
    inputs = json.loads((root / "evaluations/inputs.json").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 2 or not isinstance(manifest.get("skills"), list):
        raise ValueError("invalid evaluation manifest")
    if not isinstance(inputs, dict) or inputs.get("fictional") is not True or not isinstance(inputs.get("scenarios"), dict):
        raise ValueError("invalid fictional input registry")
    result = {}
    for entry in manifest["skills"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("skill"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", entry["skill"]) or not isinstance(entry.get("scenarios"), list):
            raise ValueError("invalid evaluation skill entry")
        for scenario in entry["scenarios"]:
            if not isinstance(scenario, dict) or not isinstance(scenario.get("id"), str):
                raise ValueError("invalid scenario")
            scenario_id = scenario["id"]
            raw = inputs["scenarios"].get(scenario_id)
            if scenario_id in result or not isinstance(raw, dict):
                raise ValueError(f"duplicate scenario or missing inputs: {scenario_id}")
            brief = raw.get("brief")
            guardrails = raw.get("critical_guardrails")
            rubric = scenario.get("rubric")
            if not isinstance(brief, str) or len(brief) < 100:
                raise ValueError(f"incomplete input brief: {scenario_id}")
            if not isinstance(guardrails, list) or not guardrails or not all(isinstance(item, str) and item.strip() for item in guardrails):
                raise ValueError(f"missing guardrails: {scenario_id}")
            if not isinstance(rubric, list) or len(rubric) < 3 or not all(isinstance(item, str) and item.strip() for item in rubric):
                raise ValueError(f"invalid rubric: {scenario_id}")
            result[scenario_id] = {**scenario, **raw, "skill": entry["skill"]}
    if set(result) != set(inputs["scenarios"]):
        raise ValueError("input registry and scenario manifest disagree")
    return result


def prepare_record(scenario_id: str, output: str, *, model: str, run_at: str, root: Path = ROOT) -> dict:
    scenario = load_scenarios(root).get(scenario_id)
    if scenario is None:
        raise ValueError(f"unknown scenario: {scenario_id}")
    version = json.loads((root / "data/skill-catalog.json").read_text(encoding="utf-8"))["project_version"]
    record = {
        "schema_version": 1, "scenario_id": scenario_id, "skill": scenario["skill"],
        "project_version": version, "skill_sha256": skill_digest(scenario["skill"], root),
        "model": model, "run_at": run_at, "execution_mode": "saved_response",
        "prompt": scenario["prompt"], "input": scenario["brief"], "input_sha256": digest(scenario["brief"]),
        "rubric": scenario["rubric"], "critical_guardrails": scenario["critical_guardrails"],
        "output": output, "output_sha256": digest(output), "review": None,
    }
    assess_record(record)
    return record


def assess_record(record: dict) -> dict:
    if not isinstance(record, dict) or record.get("schema_version") != 1:
        raise ValueError("record must be a schema-version-1 object")
    for field in ("scenario_id", "skill", "project_version", "model", "run_at", "execution_mode", "prompt", "input", "output"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"record {field} must be a non-empty string")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", record["skill"]):
        raise ValueError("invalid skill name")
    try:
        date = datetime.fromisoformat(record["run_at"].replace("Z", "+00:00"))
        if date.tzinfo is None:
            raise ValueError("timezone missing")
    except ValueError as exc:
        raise ValueError("run_at must be an ISO timestamp with timezone") from exc
    for field in ("input", "output"):
        if record.get(f"{field}_sha256") != digest(record[field]):
            raise ValueError(f"{field} hash does not match saved content")
    fingerprint = record.get("skill_sha256")
    if not isinstance(fingerprint, str) or len(fingerprint) != 64 or any(c not in "0123456789abcdef" for c in fingerprint):
        raise ValueError("missing skill content fingerprint")
    rubric = record.get("rubric")
    guardrails = record.get("critical_guardrails")
    if not isinstance(rubric, list) or len(rubric) < 3 or not all(isinstance(item, str) and item.strip() for item in rubric):
        raise ValueError("invalid saved rubric")
    if not isinstance(guardrails, list) or not guardrails or not all(isinstance(item, str) and item.strip() for item in guardrails):
        raise ValueError("missing critical guardrails")
    review = record.get("review")
    result = {"scenario_id": record["scenario_id"], "skill": record["skill"], "status": "unreviewed", "points": None, "available": len(rubric) * 2}
    if review is None:
        return result
    if not isinstance(review, dict) or review.get("mode") not in ("self_review", "independent_human", "independent_model"):
        raise ValueError("review must declare self or independent review mode")
    if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip() or review.get("guardrails_reviewed") is not True:
        raise ValueError("reviewer and explicit guardrail review are required")
    scores = review.get("scores")
    failures = review.get("critical_failures")
    if not isinstance(scores, list) or len(scores) != len(rubric):
        raise ValueError("every rubric criterion needs exactly one score")
    if not isinstance(failures, list) or not all(isinstance(item, str) and len(item.strip()) >= 10 for item in failures):
        raise ValueError("critical_failures must be an explicit list of explanations")
    indexes = set()
    points = 0
    for item in scores:
        if not isinstance(item, dict):
            raise ValueError("score must be an object")
        index, score = item.get("criterion"), item.get("score")
        if type(index) is not int or not 0 <= index < len(rubric) or index in indexes:
            raise ValueError("duplicate or invalid criterion index")
        if type(score) is not int or score not in (0, 1, 2):
            raise ValueError("scores must be integers from 0 to 2")
        evidence, rationale = item.get("evidence"), item.get("rationale")
        if not isinstance(rationale, str) or len(rationale.strip()) < 20:
            raise ValueError("score needs an explanatory rationale")
        if not isinstance(evidence, str) or (score > 0 and not evidence.strip()) or (evidence and evidence not in record["output"]):
            raise ValueError("nonzero scores need a verbatim quote from the saved output")
        indexes.add(index)
        points += score
    result.update(status="passed" if points / result["available"] >= .75 and not failures else "failed", points=points, review_mode=review["mode"])
    return result


def summarize_records(records: list[dict], root: Path = ROOT) -> dict:
    scenarios = load_scenarios(root)
    results = [assess_record(record) for record in records]
    unknown = {result["scenario_id"] for result in results} - set(scenarios)
    if unknown:
        raise ValueError("record refers to an unknown scenario")
    for record, result in zip(records, results):
        scenario = scenarios[result["scenario_id"]]
        if record["skill"] != scenario["skill"]:
            raise ValueError("record skill disagrees with its scenario")
        result["current_skill_match"] = record["skill_sha256"] == skill_digest(record["skill"], root)
        result["current_scenario_match"] = all(record[field] == scenario[field] for field in ("prompt", "rubric", "critical_guardrails")) and record["input"] == scenario["brief"]
    reviewed = {result["scenario_id"] for result in results if result["status"] != "unreviewed"}
    return {
        "planned_scenarios": len(scenarios), "recorded_runs": len(records), "reviewed_scenarios": len(reviewed),
        "unrun_scenarios": sorted(set(scenarios) - {result["scenario_id"] for result in results}),
        "results": results, "limitation": "Scores are reviewer judgments; self-review is not an independent benchmark.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--prepare", metavar="SCENARIO_ID")
    action.add_argument("--check", type=Path, metavar="RECORD_JSON")
    action.add_argument("--summary", action="store_true")
    parser.add_argument("--response", type=Path)
    parser.add_argument("--record", type=Path)
    parser.add_argument("--model", help="Use not_exposed when the actual model ID is unavailable; do not guess.")
    parser.add_argument("--run-at", help="Actual response-generation time as ISO timestamp with timezone.")
    parser.add_argument("--runs", type=Path, default=ROOT / "evaluations/runs")
    args = parser.parse_args(argv)
    try:
        if args.prepare:
            if args.response is None or args.record is None or not args.model or not args.run_at:
                parser.error("--prepare requires --response, --record, --model and --run-at")
            output = args.response.read_text(encoding="utf-8")
            record = prepare_record(args.prepare, output, model=args.model, run_at=args.run_at)
            args.record.parent.mkdir(parents=True, exist_ok=True)
            with args.record.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
            result = assess_record(record)
        elif args.check:
            result = assess_record(json.loads(args.check.read_text(encoding="utf-8")))
        else:
            records = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(args.runs.rglob("*.json"))]
            result = summarize_records(records)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Evaluation record validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
