from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "skill-catalog.json"


def load_catalog() -> list[dict[str, object]]:
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    entries = data.get("skills") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ValueError("catalog skills must be a non-empty list")
    names = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("catalog skill must be an object")
        name = entry.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
            raise ValueError("invalid catalog skill name")
        if name in names or entry.get("path") != f"skills/{name}":
            raise ValueError(f"duplicate name or invalid source path: {name}")
        names.add(name)
    return entries


def default_destination() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    return (Path(codex_home) if codex_home else Path.home() / ".codex") / "skills"


def parse_names(raw_names: list[str]) -> list[str]:
    return [name.strip() for item in raw_names for name in item.split(",") if name.strip()]


def validate_plan(planned: list[tuple[Path, Path]]) -> None:
    sources = [source.resolve() for source, _ in planned]
    targets = [target.resolve() for _, target in planned]
    for source in sources:
        if not source.is_dir():
            raise ValueError(f"source skill directory is missing: {source}")
        for target in targets:
            if source == target or source in target.parents or target in source.parents:
                raise ValueError(f"source and destination overlap: {source} / {target}")
    for _, target in planned:
        attributes = getattr(target.lstat(), "st_file_attributes", 0) if target.exists() or target.is_symlink() else 0
        if target.is_symlink() or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            raise ValueError(f"refusing to replace a linked destination: {target}")
        if target.exists() and not target.is_dir():
            raise ValueError(f"destination is not a directory: {target}")


def install_batch(planned: list[tuple[Path, Path]], destination: Path, *, force: bool = False, copy_tree=shutil.copytree) -> None:
    """Stage every copy before replacing any installation; roll back commit errors.

    copy_tree is a filesystem-copy callable so interrupted copies can be tested
    without inducing disk failures on a user's actual installation.
    """
    validate_plan(planned)
    destination.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".consulting-skills-stage-", dir=destination))
    backups: list[tuple[Path, Path]] = []
    installed: list[Path] = []
    preserve_recovery = False
    try:
        for index, (source, _) in enumerate(planned):
            copy_tree(source, staging / f"new-{index}")
        for index, (_, target) in enumerate(planned):
            # Recheck after staging: another process may have installed meanwhile.
            validate_plan([(source, target) for source, _ in planned])
            if target.exists():
                if not force:
                    raise FileExistsError(f"destination appeared or exists; use --force: {target}")
                backup = staging / f"old-{index}"
                target.rename(backup)
                backups.append((target, backup))
            (staging / f"new-{index}").rename(target)
            installed.append(target)
    except BaseException:
        try:
            for target in reversed(installed):
                shutil.rmtree(target)
            for target, backup in reversed(backups):
                backup.rename(target)
        except OSError as exc:
            preserve_recovery = True
            raise OSError(f"rollback incomplete; previous files preserved in {staging}: {exc}") from exc
        raise
    finally:
        if not preserve_recovery:
            shutil.rmtree(staging)


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
    try:
        entries = load_catalog()
    except (OSError, ValueError) as exc:
        print(f"Cannot read skill catalog: {exc}", file=sys.stderr)
        return 2
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
    if not selected or len(selected) != len(set(selected)):
        print("Select at least one skill; duplicate selections are not allowed.", file=sys.stderr)
        return 2
    unknown = sorted(set(selected) - set(by_name))
    if unknown:
        print(f"Unknown skill(s): {', '.join(unknown)}", file=sys.stderr)
        return 2

    destination = args.destination.expanduser().resolve()
    source_root = (ROOT / "skills").resolve()
    if destination == source_root or source_root in destination.parents:
        print("Destination cannot be inside the repository's source skills directory.", file=sys.stderr)
        return 2
    planned = [(ROOT / str(by_name[name]["path"]), destination / name) for name in selected]
    try:
        validate_plan(planned)
    except (OSError, ValueError) as exc:
        print(f"Invalid installation plan: {exc}", file=sys.stderr)
        return 2
    conflicts = [target for _, target in planned if target.exists()]
    if conflicts and not args.force:
        print("Refusing to overwrite existing skill folders; use --force:", file=sys.stderr)
        for conflict in conflicts:
            print(f"- {conflict}", file=sys.stderr)
        return 1

    if not args.dry_run:
        try:
            install_batch(planned, destination, force=args.force)
        except (OSError, ValueError) as exc:
            print(f"Installation failed: {exc}", file=sys.stderr)
            return 1

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
