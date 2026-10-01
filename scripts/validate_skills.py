from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError:
    raise SystemExit("YAML validation requires: python -m pip install -r requirements-dev.txt")

if __package__:
    from . import check_example_calculations, evaluate_results
else:
    import check_example_calculations
    import evaluate_results


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
CATALOG_PATH = ROOT / "data" / "skill-catalog.json"
EVALUATIONS_PATH = ROOT / "evaluations" / "manifest.json"

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
# Lookahead permits overlapping image and wrapper links in linked badges.
MARKDOWN_LINK_RE = re.compile(r"(?=!?\[(?:[^\[\]\n]|\[[^\]\n]*\])*\]\((<[^>]+>(?:#[^\s)]*)?|[^\s)]+)(?:\s+['\"][^)]*['\"])?\))")
IGNORED_PARTS = {".git", "build", "dist", "__pycache__", ".venv", "venv"}
SECRET_PATTERNS = [
    ("GitHub OAuth token", re.compile(r"gho_[A-Za-z0-9_]{20,}")),
    ("GitHub personal access token", re.compile(r"ghp_[A-Za-z0-9_]{20,}")),
    ("GitHub fine-grained token", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("OpenAI-style API key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private key block", re.compile(r"PRIVATE KEY")),
    ("password assignment", re.compile(r"(?i)\b(password|token|secret)\s*[=:]\s*['\"][^'\"]+")),
]


def fail(errors: list[str], path: Path, message: str) -> None:
    try:
        label = path.relative_to(ROOT)
    except ValueError:
        label = path
    errors.append(f"{label}: {message}")


class UniqueSafeLoader(yaml.SafeLoader):
    """Safe YAML types only, with duplicate mapping keys rejected."""

    def construct_mapping(self, node, deep=False):
        keys = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in keys:
                raise yaml.YAMLError("mapping keys must be unique strings")
            keys.add(key)
        return super().construct_mapping(node, deep=deep)


def load_yaml_mapping(text: str) -> dict:
    data = yaml.load(text, Loader=UniqueSafeLoader)
    if not isinstance(data, dict):
        raise yaml.YAMLError("expected a YAML mapping")
    return data


def parse_frontmatter(text: str) -> tuple[dict, str] | None:
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    raw = text[4:end]
    body = text[end + 5 :]
    try:
        data = load_yaml_mapping(raw)
    except (yaml.YAMLError, ValueError, RecursionError):
        return None
    return data, body


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"

    if not skill_md.exists():
        fail(errors, skill_dir, "missing SKILL.md")
        return
    if not openai_yaml.exists():
        fail(errors, skill_dir, "missing agents/openai.yaml")

    try:
        text = skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        fail(errors, skill_md, "cannot read UTF-8 skill instructions")
        return
    parsed = parse_frontmatter(text)
    if parsed is None:
        fail(errors, skill_md, "missing or invalid YAML frontmatter")
        return

    frontmatter, body = parsed
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if set(frontmatter) != {"name", "description"}:
        fail(errors, skill_md, "frontmatter must contain only name and description")

    if name != skill_dir.name:
        fail(errors, skill_md, f"name must match directory name ({skill_dir.name})")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        fail(errors, skill_md, "name must be lowercase kebab-case and <= 64 characters")
    if not isinstance(description, str) or len(description) < 80:
        fail(errors, skill_md, "description should explain triggers and use cases")
    if "TODO" in text or "PLACEHOLDER" in text:
        fail(errors, skill_md, "contains TODO or PLACEHOLDER")
    if re.search(r"^## .*Workflow", body, re.MULTILINE) is None:
        fail(errors, skill_md, "missing workflow section")
    if "## Guardrails" not in body:
        fail(errors, skill_md, "missing ## Guardrails section")
    if "```" not in body and "| --- |" not in body:
        fail(errors, skill_md, "expected at least one concrete template or table")

    if openai_yaml.is_file():
        try:
            metadata = load_yaml_mapping(openai_yaml.read_text(encoding="utf-8"))
            interface = metadata.get("interface")
            if not isinstance(interface, dict):
                fail(errors, openai_yaml, "interface must be a mapping")
            else:
                for field in ("display_name", "short_description", "default_prompt"):
                    value = interface.get(field)
                    if not isinstance(value, str) or not value.strip():
                        fail(errors, openai_yaml, f"interface.{field} must be a non-empty string")
                short = interface.get("short_description", "")
                if isinstance(short, str) and not 25 <= len(short) <= 64:
                    fail(errors, openai_yaml, "short_description must be 25-64 characters")
                prompt = interface.get("default_prompt", "")
                if isinstance(prompt, str) and f"${name}" not in prompt:
                    fail(errors, openai_yaml, f"default prompt should mention ${name}")
        except (OSError, UnicodeError, yaml.YAMLError, ValueError, RecursionError):
            fail(errors, openai_yaml, "invalid YAML syntax, duplicate keys, or unreadable metadata")

    for ref in sorted(set(re.findall(r"`(references/[^`]+)`", text))):
        if not (skill_dir / ref).exists():
            fail(errors, skill_md, f"referenced file does not exist: {ref}")

    validate_reference_routing(skill_dir, errors)


def validate_reference_routing(skill_dir: Path, errors: list[str]) -> None:
    references_dir = skill_dir / "references"
    if not references_dir.exists():
        return
    skill_md = skill_dir / "SKILL.md"
    skill_text = skill_md.read_text(encoding="utf-8")
    for reference in sorted(path for path in references_dir.rglob("*") if path.is_file()):
        relative = reference.relative_to(skill_dir).as_posix()
        if f"`{relative}`" not in skill_text:
            fail(errors, reference, "reference is not routed from SKILL.md")


def without_code(text: str) -> str:
    text = re.sub(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$", "", text)
    return re.sub(r"`[^`\n]*`", "", text)


def heading_anchors(text: str) -> set[str]:
    anchors = set(re.findall(r'\bid=["\']([^"\']+)["\']', text))
    counts: dict[str, int] = {}
    for heading in re.findall(r"(?m)^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", text):
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\-\s]", "", heading.lower(), flags=re.UNICODE).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def check_external_url(target: str, timeout: float) -> str | None:
    try:
        request = Request(target, headers={"User-Agent": "consulting-skills-lab-link-check/1"})
        with urlopen(request, timeout=timeout) as response:
            response.read(1)
    except HTTPError as exc:
        qualifier = "unverified (access/rate limit)" if exc.code in (401, 403, 429) else "broken"
        return f"{qualifier} external link: {target} (HTTP {exc.code})"
    except (OSError, URLError, ValueError):
        return f"unverified external link: {target} (network/TLS/timeout error)"
    return None


def validate_markdown_links(path: Path, errors: list[str], *, check_external: bool = False, timeout: float = 10, cache: dict | None = None) -> None:
    text = without_code(path.read_text(encoding="utf-8"))
    cache = {} if cache is None else cache
    targets = MARKDOWN_LINK_RE.findall(text)
    definitions = {label.casefold(): target for label, target in re.findall(r"(?m)^\s{0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)", text)}
    targets.extend(definitions.values())
    for label, reference in re.findall(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]", text):
        if (reference or label).casefold() not in definitions:
            fail(errors, path, f"undefined link reference: {reference or label}")
    for raw_target in targets:
        target = raw_target.replace("<", "").replace(">", "")
        if target.startswith(("http://", "https://")):
            if check_external:
                if target not in cache:
                    cache[target] = check_external_url(target, timeout)
                if cache[target]:
                    fail(errors, path, cache[target])
            continue
        if target.startswith("mailto:"):
            continue
        parts = urlsplit(target)
        if parts.scheme:
            fail(errors, path, f"unsupported link scheme: {parts.scheme}")
            continue
        target_path = unquote(parts.path)
        resolved = (path.parent / target_path).resolve() if target_path else path
        if not resolved.exists():
            fail(errors, path, f"broken internal link: {target}")
        elif parts.fragment and resolved.suffix.lower() == ".md":
            anchors = heading_anchors(without_code(resolved.read_text(encoding="utf-8")))
            if unquote(parts.fragment) not in anchors:
                fail(errors, path, f"broken heading anchor: {target}")


def repository_files():
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if path.is_file() and not path.is_symlink() and not IGNORED_PARTS.intersection(relative.parts):
            yield path


def validate_secrets(errors: list[str]) -> None:
    validator_path = Path(__file__).resolve()
    for path in repository_files():
        if path.resolve() == validator_path:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(errors, path, f"possible secret pattern: {label}")


def validate_catalog(skill_dirs: list[Path], errors: list[str], *, catalog_path: Path = CATALOG_PATH) -> None:
    CATALOG_PATH = catalog_path
    if not CATALOG_PATH.exists():
        fail(errors, CATALOG_PATH, "missing machine-readable skill catalog")
        return

    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError, OSError):
        fail(errors, CATALOG_PATH, "invalid or unreadable JSON")
        return
    if not isinstance(catalog, dict):
        fail(errors, CATALOG_PATH, "catalog must be an object")
        return

    if catalog.get("schema_version") != 2:
        fail(errors, CATALOG_PATH, "schema_version must be 2")
    version = catalog.get("project_version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        fail(errors, CATALOG_PATH, "project_version must be major.minor.patch")

    entries = catalog.get("skills")
    if not isinstance(entries, list):
        fail(errors, CATALOG_PATH, "skills must be a list")
        return

    catalog_names: list[str] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(errors, CATALOG_PATH, f"skills[{index}] must be an object")
            continue
        name = entry.get("name")
        category = entry.get("category")
        description = entry.get("description")
        primary_output = entry.get("primary_output")
        skill_path = entry.get("path")
        example = entry.get("example")
        tags = entry.get("tags")
        if not isinstance(name, str) or not NAME_RE.match(name):
            fail(errors, CATALOG_PATH, f"skills[{index}].name is invalid")
            continue
        catalog_names.append(name)
        if not isinstance(category, str) or not category.strip():
            fail(errors, CATALOG_PATH, f"{name}: category is required")
        if not isinstance(description, str) or len(description.strip()) < 60:
            fail(errors, CATALOG_PATH, f"{name}: description must be specific")
        if not isinstance(primary_output, str) or len(primary_output.strip()) < 20:
            fail(errors, CATALOG_PATH, f"{name}: primary_output must be descriptive")
        if skill_path != f"skills/{name}" or not (ROOT / str(skill_path)).is_dir():
            fail(errors, CATALOG_PATH, f"{name}: path is invalid")
        if not isinstance(example, str) or not (ROOT / example).resolve().is_relative_to(ROOT) or not (ROOT / example).is_file():
            fail(errors, CATALOG_PATH, f"{name}: example is missing")
        if not isinstance(tags, list) or len(tags) < 3 or not all(isinstance(tag, str) for tag in tags):
            fail(errors, CATALOG_PATH, f"{name}: at least three tags are required")

    if len(catalog_names) != len(set(catalog_names)):
        fail(errors, CATALOG_PATH, "contains duplicate skill names")

    folder_names = {path.name for path in skill_dirs}
    if set(catalog_names) != folder_names:
        missing = sorted(folder_names - set(catalog_names))
        extra = sorted(set(catalog_names) - folder_names)
        fail(errors, CATALOG_PATH, f"catalog mismatch; missing={missing}, extra={extra}")


def validate_evaluations(skill_dirs: list[Path], errors: list[str], *, manifest_path: Path = EVALUATIONS_PATH) -> None:
    EVALUATIONS_PATH = manifest_path
    if not EVALUATIONS_PATH.exists():
        fail(errors, EVALUATIONS_PATH, "missing evaluation manifest")
        return
    try:
        manifest = json.loads(EVALUATIONS_PATH.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError, OSError):
        fail(errors, EVALUATIONS_PATH, "invalid or unreadable JSON")
        return
    if not isinstance(manifest, dict):
        fail(errors, EVALUATIONS_PATH, "manifest must be an object")
        return
    if manifest.get("schema_version") != 2 or manifest.get("inputs") != "evaluations/inputs.json":
        fail(errors, EVALUATIONS_PATH, "manifest schema_version must be 2 with the input registry")
    entries = manifest.get("skills")
    if not isinstance(entries, list):
        fail(errors, EVALUATIONS_PATH, "skills must be a list")
        return
    expected_names = {path.name for path in skill_dirs}
    actual_names = [entry.get("skill") for entry in entries if isinstance(entry, dict) and isinstance(entry.get("skill"), str)]
    if set(actual_names) != expected_names or len(actual_names) != len(entries) or len(set(actual_names)) != len(actual_names):
        fail(errors, EVALUATIONS_PATH, "evaluation skills must match skill folders")
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = entry.get("skill", "unknown")
        scenarios = entry.get("scenarios")
        if not isinstance(scenarios, list) or len(scenarios) < 2:
            fail(errors, EVALUATIONS_PATH, f"{name}: at least two scenarios are required")
            continue
        ids: list[str] = []
        for scenario in scenarios:
            if not isinstance(scenario, dict):
                fail(errors, EVALUATIONS_PATH, f"{name}: scenario must be an object")
                continue
            scenario_id = scenario.get("id")
            prompt = scenario.get("prompt")
            rubric = scenario.get("rubric")
            if not isinstance(scenario_id, str) or not scenario_id:
                fail(errors, EVALUATIONS_PATH, f"{name}: scenario id is required")
            else:
                ids.append(scenario_id)
            if not isinstance(prompt, str) or len(prompt) < 40:
                fail(errors, EVALUATIONS_PATH, f"{name}:{scenario_id}: prompt is too short")
            if not isinstance(rubric, list) or len(rubric) < 3 or not all(isinstance(item, str) and item.strip() for item in rubric):
                fail(errors, EVALUATIONS_PATH, f"{name}:{scenario_id}: at least three rubric items are required")
        if len(ids) != len(set(ids)):
            fail(errors, EVALUATIONS_PATH, f"{name}: duplicate scenario ids")


def validate_evaluation_records(errors: list[str], *, root: Path = ROOT) -> None:
    try:
        evaluate_results.load_scenarios(root)
    except (OSError, ValueError, KeyError, TypeError):
        fail(errors, root / "evaluations/inputs.json", "invalid, missing, or inconsistent evaluation inputs")
        return
    records = []
    for path in sorted((root / "evaluations/runs").rglob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            evaluate_results.assess_record(record)
            records.append(record)
        except (OSError, ValueError, KeyError, TypeError):
            fail(errors, path, "invalid evaluation evidence record")
    try:
        evaluate_results.summarize_records(records, root)
    except (OSError, ValueError, KeyError, TypeError):
        fail(errors, root / "evaluations/runs", "evaluation record/scenario mismatch")


def validate_versions(errors: list[str], *, root: Path = ROOT) -> None:
    try:
        catalog = json.loads((root / "data/skill-catalog.json").read_text(encoding="utf-8"))
        spec = load_yaml_mapping((root / "spec.yaml").read_text(encoding="utf-8"))
        if not isinstance(catalog, dict) or spec.get("version") != catalog.get("project_version"):
            fail(errors, root / "spec.yaml", "spec version must match catalog project_version")
    except (OSError, ValueError, yaml.YAMLError, RecursionError):
        fail(errors, root / "spec.yaml", "cannot validate spec/catalog version")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate skills and local links; network checks are opt-in.")
    parser.add_argument("--check-external-links", action="store_true")
    args = parser.parse_args(argv)
    errors: list[str] = []
    skill_dirs: list[Path] = []
    if not SKILLS_DIR.exists():
        fail(errors, SKILLS_DIR, "missing skills directory")
    else:
        skill_dirs = [p for p in sorted(SKILLS_DIR.iterdir()) if p.is_dir()]
        if not skill_dirs:
            fail(errors, SKILLS_DIR, "no skills found")
        for skill_dir in skill_dirs:
            validate_skill(skill_dir, errors)

    validate_catalog(skill_dirs, errors)
    validate_evaluations(skill_dirs, errors)
    validate_versions(errors)
    validate_evaluation_records(errors)
    try:
        errors.extend(check_example_calculations.validate_examples(ROOT))
    except (OSError, ValueError, KeyError, TypeError):
        fail(errors, ROOT / "data/example-calculations.json", "invalid or missing calculation inputs/examples")
    cache = {}
    for markdown_path in sorted(path for path in repository_files() if path.suffix == ".md"):
        try:
            validate_markdown_links(markdown_path, errors, check_external=args.check_external_links, cache=cache)
        except (OSError, UnicodeError, ValueError):
            fail(errors, markdown_path, "unreadable UTF-8 Markdown or malformed link target")
    validate_secrets(errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
