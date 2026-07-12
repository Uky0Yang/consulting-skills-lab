from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
CATALOG_PATH = ROOT / "data" / "skill-catalog.json"

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SECRET_PATTERNS = [
    ("GitHub OAuth token", re.compile(r"gho_[A-Za-z0-9_]{20,}")),
    ("GitHub personal access token", re.compile(r"ghp_[A-Za-z0-9_]{20,}")),
    ("GitHub fine-grained token", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("OpenAI-style API key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private key block", re.compile(r"PRIVATE KEY")),
    ("password assignment", re.compile(r"(?i)(password|token|secret)\\s*[=:]\\s*['\"][^'\"]+")),
]


def fail(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            return None
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"

    if not skill_md.exists():
        fail(errors, skill_dir, "missing SKILL.md")
        return
    if not openai_yaml.exists():
        fail(errors, skill_dir, "missing agents/openai.yaml")

    text = skill_md.read_text(encoding="utf-8")
    parsed = parse_frontmatter(text)
    if parsed is None:
        fail(errors, skill_md, "missing or invalid YAML frontmatter")
        return

    frontmatter, body = parsed
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if name != skill_dir.name:
        fail(errors, skill_md, f"name must match directory name ({skill_dir.name})")
    if not NAME_RE.match(name):
        fail(errors, skill_md, "name must be lowercase kebab-case and <= 64 characters")
    if len(description) < 80:
        fail(errors, skill_md, "description should explain triggers and use cases")
    if "TODO" in text or "PLACEHOLDER" in text:
        fail(errors, skill_md, "contains TODO or PLACEHOLDER")
    if re.search(r"^## .*Workflow", body, re.MULTILINE) is None:
        fail(errors, skill_md, "missing workflow section")
    if "## Guardrails" not in body:
        fail(errors, skill_md, "missing ## Guardrails section")
    if "```" not in body and "| --- |" not in body:
        fail(errors, skill_md, "expected at least one concrete template or table")

    yaml_text = openai_yaml.read_text(encoding="utf-8") if openai_yaml.exists() else ""
    if f"${name}" not in yaml_text:
        fail(errors, openai_yaml, f"default prompt should mention ${name}")
    if "display_name:" not in yaml_text or "short_description:" not in yaml_text:
        fail(errors, openai_yaml, "missing interface metadata")

    for ref in sorted(set(re.findall(r"`(references/[^`]+)`", text))):
        if not (skill_dir / ref).exists():
            fail(errors, skill_md, f"referenced file does not exist: {ref}")


def validate_secrets(errors: list[str]) -> None:
    validator_path = Path(__file__).resolve()
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.resolve() == validator_path:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(errors, path, f"possible secret pattern: {label}")


def validate_catalog(skill_dirs: list[Path], errors: list[str]) -> None:
    if not CATALOG_PATH.exists():
        fail(errors, CATALOG_PATH, "missing machine-readable skill catalog")
        return

    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        fail(errors, CATALOG_PATH, f"invalid JSON: {exc}")
        return

    if catalog.get("schema_version") != 1:
        fail(errors, CATALOG_PATH, "schema_version must be 1")

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
        primary_output = entry.get("primary_output")
        if not isinstance(name, str) or not NAME_RE.match(name):
            fail(errors, CATALOG_PATH, f"skills[{index}].name is invalid")
            continue
        catalog_names.append(name)
        if not isinstance(category, str) or not category.strip():
            fail(errors, CATALOG_PATH, f"{name}: category is required")
        if not isinstance(primary_output, str) or len(primary_output.strip()) < 20:
            fail(errors, CATALOG_PATH, f"{name}: primary_output must be descriptive")

    if len(catalog_names) != len(set(catalog_names)):
        fail(errors, CATALOG_PATH, "contains duplicate skill names")

    folder_names = {path.name for path in skill_dirs}
    if set(catalog_names) != folder_names:
        missing = sorted(folder_names - set(catalog_names))
        extra = sorted(set(catalog_names) - folder_names)
        fail(errors, CATALOG_PATH, f"catalog mismatch; missing={missing}, extra={extra}")


def main() -> int:
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
