from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "skill-catalog.json"


def load_catalog() -> list[dict[str, object]]:
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return data["skills"]


def default_destination() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    return (Path(codex_home) if codex_home else Path.home() / ".codex") / "skills"


def parse_names(raw_names: list[str]) -> list[str]:
    return [name.strip() for item in raw_names for name in item.split(",") if name.strip()]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install Consulting Skills Lab skills into Codex.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--list", action="store_true", help="List available skills.")
    action.add_argument("--all", action="store_true", help="Install every skill.")
    action.add_argument("--skills", nargs="+", metavar="NAME", help="Install comma- or space-separated skills.")
    parser.add_argument("--destination", type=Path, default=default_destination(), help="Target skills directory.")
    parser.add_argument("--force", action="store_true", help="Replace existing selected skill folders.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned changes without copying files.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    entries = load_catalog()
    by_name = {str(entry["name"]): entry for entry in entries}

    if args.list:
        names = list(by_name)
        if args.json:
            print(json.dumps({"skills": names}))
        else:
            for entry in entries:
                print(f"{entry['name']}: {entry['description']}")
        return 0

    selected = list(by_name) if args.all else parse_names(args.skills)
    unknown = sorted(set(selected) - set(by_name))
    if unknown:
        print(f"Unknown skill(s): {', '.join(unknown)}", file=sys.stderr)
        return 2

    destination = args.destination.expanduser().resolve()
    planned = [(ROOT / str(by_name[name]["path"]), destination / name) for name in selected]
    conflicts = [target for _, target in planned if target.exists()]
    if conflicts and not args.force:
        print("Refusing to overwrite existing skill folders; use --force:", file=sys.stderr)
        for conflict in conflicts:
            print(f"- {conflict}", file=sys.stderr)
        return 1

    if not args.dry_run:
        destination.mkdir(parents=True, exist_ok=True)
        for source, target in planned:
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)

    result = {
        "destination": str(destination),
        "installed": selected,
        "dry_run": args.dry_run,
    }
    if args.json:
        print(json.dumps(result))
    else:
        verb = "Would install" if args.dry_run else "Installed"
        print(f"{verb} {len(selected)} skill(s) to {destination}")
        for name in selected:
            print(f"- {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
