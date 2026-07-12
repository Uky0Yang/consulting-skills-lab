import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts import validate_skills


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "skill-catalog.json"
INSTALLER_PATH = ROOT / "scripts" / "install_skills.py"
PACKAGER_PATH = ROOT / "scripts" / "package_release.py"


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


class TestV1ContentCoverage(unittest.TestCase):
    def test_should_have_a_worked_example_for_every_skill(self) -> None:
        """REQ-V1-001: Every catalogued skill has a realistic worked example."""
        catalog = load_catalog()

        missing = [entry["name"] for entry in catalog["skills"] if not (ROOT / entry["example"]).is_file()]

        self.assertEqual([], missing)

    def test_should_have_two_evaluation_scenarios_for_every_skill(self) -> None:
        """REQ-V1-002: Every skill has at least two realistic evaluation scenarios."""
        catalog = load_catalog()
        manifest = json.loads((ROOT / "evaluations" / "manifest.json").read_text(encoding="utf-8"))
        scenario_counts = {entry["skill"]: len(entry["scenarios"]) for entry in manifest["skills"]}

        insufficient = [entry["name"] for entry in catalog["skills"] if scenario_counts.get(entry["name"], 0) < 2]

        self.assertEqual([], insufficient)

    def test_should_give_each_evaluation_an_explicit_rubric(self) -> None:
        """REQ-V1-002: Evaluation scenarios define observable quality criteria."""
        manifest = json.loads((ROOT / "evaluations" / "manifest.json").read_text(encoding="utf-8"))

        missing = [
            f"{skill['skill']}:{scenario.get('id', 'unknown')}"
            for skill in manifest["skills"]
            for scenario in skill["scenarios"]
            if len(scenario.get("rubric", [])) < 3
        ]

        self.assertEqual([], missing)


class TestV1Installer(unittest.TestCase):
    def run_installer(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER_PATH), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_should_list_every_catalogued_skill(self) -> None:
        """REQ-V1-003: The installer lists available skills from the catalog."""
        result = self.run_installer("--list", "--json")
        expected_names = [entry["name"] for entry in load_catalog()["skills"]]

        self.assertEqual(expected_names, json.loads(result.stdout)["skills"])

    def test_should_install_one_selected_skill(self) -> None:
        """REQ-V1-003: A selected skill is copied to an explicit destination."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_installer(
                "--skills",
                "executive-decision-memo",
                "--destination",
                temp_dir,
            )

            installed = Path(temp_dir) / "executive-decision-memo" / "SKILL.md"
            outcome = (result.returncode, installed.is_file())

        self.assertEqual((0, True), outcome)

    def test_should_reject_an_unknown_skill(self) -> None:
        """REQ-V1-003: Unknown skill names fail without partial installation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_installer("--skills", "not-a-skill", "--destination", temp_dir)

        self.assertNotEqual(0, result.returncode)

    def test_should_not_overwrite_without_force(self) -> None:
        """REQ-V1-003: Existing skill folders are protected by default."""
        with tempfile.TemporaryDirectory() as temp_dir:
            first = self.run_installer("--skills", "executive-decision-memo", "--destination", temp_dir)
            second = self.run_installer("--skills", "executive-decision-memo", "--destination", temp_dir)
            outcome = (first.returncode, second.returncode)

        self.assertEqual((0, 1), outcome)


class TestV1ReleasePackaging(unittest.TestCase):
    def test_should_build_an_all_skills_archive_and_checksum_manifest(self) -> None:
        """REQ-V1-004: Release packaging produces a bundle and SHA-256 manifest."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, str(PACKAGER_PATH), "--output", temp_dir, "--version", "1.0.0"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            output = Path(temp_dir)
            bundle = output / "consulting-skills-lab-1.0.0.zip"
            checksums = output / "SHA256SUMS.txt"
            outcome = (result.returncode, bundle.is_file(), checksums.is_file())

        self.assertEqual((0, True, True), outcome)

    def test_should_package_every_skill_in_the_bundle(self) -> None:
        """REQ-V1-004: The full bundle contains every catalogued skill."""
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.run(
                [sys.executable, str(PACKAGER_PATH), "--output", temp_dir, "--version", "1.0.0"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            bundle = Path(temp_dir) / "consulting-skills-lab-1.0.0.zip"
            with zipfile.ZipFile(bundle) as archive:
                names = set(archive.namelist())
            missing = [
                entry["name"]
                for entry in load_catalog()["skills"]
                if f"skills/{entry['name']}/SKILL.md" not in names
            ]

        self.assertEqual([], missing)

    def test_should_record_the_bundle_checksum(self) -> None:
        """REQ-V1-004: The checksum manifest matches the generated bundle."""
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.run(
                [sys.executable, str(PACKAGER_PATH), "--output", temp_dir, "--version", "1.0.0"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            output = Path(temp_dir)
            bundle = output / "consulting-skills-lab-1.0.0.zip"
            expected = hashlib.sha256(bundle.read_bytes()).hexdigest()
            manifest = (output / "SHA256SUMS.txt").read_text(encoding="utf-8")

        self.assertIn(f"{expected}  {bundle.name}", manifest)


class TestV1IntegrityValidation(unittest.TestCase):
    def test_should_detect_a_broken_internal_markdown_link(self) -> None:
        """REQ-V1-005: Repository validation rejects broken internal links."""
        path = ROOT / "tests" / "temporary-broken-link.md"
        path.write_text("[Missing](../does-not-exist.md)\n", encoding="utf-8")
        self.addCleanup(path.unlink, missing_ok=True)
        errors: list[str] = []

        validate_skills.validate_markdown_links(path, errors)

        self.assertEqual(1, len(errors))

    def test_should_detect_an_unrouted_reference(self) -> None:
        """REQ-V1-005: Skill references must be routed from SKILL.md."""
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as temp_dir:
            skill_dir = Path(temp_dir) / "sample-skill"
            references_dir = skill_dir / "references"
            references_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("Read `references/used.md`.\n", encoding="utf-8")
            (references_dir / "used.md").write_text("used\n", encoding="utf-8")
            (references_dir / "orphan.md").write_text("orphan\n", encoding="utf-8")
            errors: list[str] = []

            validate_skills.validate_reference_routing(skill_dir, errors)

        self.assertEqual(1, len(errors))
