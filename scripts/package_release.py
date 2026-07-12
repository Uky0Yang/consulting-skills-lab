from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "skill-catalog.json"
FIXED_TIMESTAMP = (2020, 1, 1, 0, 0, 0)


def add_file(archive: zipfile.ZipFile, source: Path, archive_name: str) -> None:
    info = zipfile.ZipInfo(str(PurePosixPath(archive_name)), date_time=FIXED_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, source.read_bytes())


def write_archive(output: Path, files: list[tuple[Path, str]]) -> None:
    with zipfile.ZipFile(output, "w") as archive:
        for source, archive_name in sorted(files, key=lambda item: item[1]):
            add_file(archive, source, archive_name)


def skill_files(skill_dir: Path, prefix: str) -> list[tuple[Path, str]]:
    return [
        (path, str(PurePosixPath(prefix) / path.relative_to(skill_dir).as_posix()))
        for path in skill_dir.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    ]


def build_release(output_dir: Path, version: str) -> list[Path]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    entries = catalog["skills"]
    output_dir.mkdir(parents=True, exist_ok=True)
    archives: list[Path] = []
    all_files: list[tuple[Path, str]] = []

    for entry in entries:
        name = entry["name"]
        skill_dir = ROOT / entry["path"]
        files = skill_files(skill_dir, name)
        archive_path = output_dir / f"{name}-{version}.zip"
        write_archive(archive_path, files)
        archives.append(archive_path)
        all_files.extend(skill_files(skill_dir, f"skills/{name}"))

    for extra in (ROOT / "README.md", ROOT / "LICENSE", CATALOG_PATH):
        all_files.append((extra, extra.relative_to(ROOT).as_posix()))

    bundle = output_dir / f"consulting-skills-lab-{version}.zip"
    write_archive(bundle, all_files)
    archives.append(bundle)

    checksum_lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in sorted(archives)]
    (output_dir / "SHA256SUMS.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8", newline="\n")
    return archives


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Consulting Skills Lab release archives.")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--version", required=True)
    args = parser.parse_args(argv)

    archives = build_release(args.output.resolve(), args.version)
    print(f"Built {len(archives)} archive(s) in {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
