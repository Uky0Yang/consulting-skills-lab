import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts import install_skills, package_release


ROOT = Path(__file__).resolve().parents[1]
VERSION = json.loads((ROOT / "data/skill-catalog.json").read_text(encoding="utf-8"))["project_version"]
NAME = "executive-decision-memo"


class TestSafeInstaller(unittest.TestCase):
    """FIX-003: Validate selections and preserve installed files on failure."""

    def run_installer(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/install_skills.py"), *args],
            capture_output=True, text=True, check=False,
        )

    def test_should_reject_empty_selection(self):
        self.assertEqual(2, self.run_installer("--skills", ",,", "--dry-run").returncode)

    def test_should_reject_duplicate_selection(self):
        self.assertEqual(2, self.run_installer("--skills", NAME, NAME, "--dry-run").returncode)

    def test_should_reject_source_destination_overlap(self):
        result = self.run_installer("--all", "--destination", str(ROOT / "skills"), "--force", "--dry-run")
        self.assertEqual(2, result.returncode)

    def test_should_reject_target_ancestor_of_source(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "installed"
            source = target / "source"
            source.mkdir(parents=True)
            with self.assertRaises(ValueError):
                install_skills.install_batch([(source, target)], Path(temp_dir))

    def test_should_preserve_old_installation_when_copy_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            source = base / "source"
            source.mkdir()
            target = base / "destination" / NAME
            target.mkdir(parents=True)
            (target / "old.txt").write_text("keep me", encoding="utf-8")

            def interrupted_copy(source_path, staging_path):
                staging_path.mkdir()
                (staging_path / "partial.txt").write_text("partial", encoding="utf-8")
                raise OSError("simulated interrupted filesystem copy")

            with self.assertRaises(OSError):
                install_skills.install_batch([(source, target)], target.parent, force=True, copy_tree=interrupted_copy)
            self.assertEqual(["old.txt"], sorted(p.name for p in target.iterdir()))

    def test_should_replace_old_installation_with_force(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / NAME
            target.mkdir()
            (target / "old.txt").write_text("old", encoding="utf-8")
            result = self.run_installer("--skills", NAME, "--destination", temp_dir, "--force")
            self.assertEqual((0, True, False), (result.returncode, (target / "SKILL.md").is_file(), (target / "old.txt").exists()))

    def test_should_roll_back_an_earlier_replacement_when_commit_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            source = base / "source"
            source.mkdir()
            (source / "new.txt").write_text("new", encoding="utf-8")
            destination = base / "installed"
            targets = [destination / "first", destination / "second"]
            for target in targets:
                target.mkdir(parents=True)
                (target / "old.txt").write_text("keep", encoding="utf-8")

            def copy_with_rename_collision(source_path, staging_path):
                shutil.copytree(source_path, staging_path)
                if staging_path.name == "new-1":
                    blocker = staging_path.parent / "old-1"
                    blocker.mkdir()
                    (blocker / "occupied").write_text("block rename", encoding="utf-8")

            with self.assertRaises(OSError):
                install_skills.install_batch([(source, target) for target in targets], destination, force=True, copy_tree=copy_with_rename_collision)
            self.assertEqual([["old.txt"], ["old.txt"]], [sorted(p.name for p in target.iterdir()) for target in targets])

    def test_should_not_overwrite_a_destination_created_during_staging(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            source = base / "source"
            source.mkdir()
            target = base / "installed" / "skill"

            def concurrent_install(source_path, staging_path):
                shutil.copytree(source_path, staging_path)
                target.mkdir()
                (target / "other.txt").write_text("other process", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                install_skills.install_batch([(source, target)], target.parent, copy_tree=concurrent_install)
            self.assertTrue((target / "other.txt").is_file())

    def test_should_reject_installing_inside_an_unselected_source_skill(self):
        result = self.run_installer("--skills", NAME, "--destination", str(ROOT / "skills/value-creation-plan"), "--dry-run")
        self.assertEqual(2, result.returncode)

    def test_should_roll_back_on_a_late_plan_validation_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            source = base / "source"
            source.mkdir()
            destination = base / "installed"
            first, second = destination / "first", destination / "second"
            first.mkdir(parents=True)
            (first / "old.txt").write_text("keep", encoding="utf-8")

            def copy_with_concurrent_file(source_path, staging_path):
                shutil.copytree(source_path, staging_path)
                if staging_path.name == "new-1":
                    second.write_text("concurrent file", encoding="utf-8")

            with self.assertRaises(ValueError):
                install_skills.install_batch([(source, first), (source, second)], destination, force=True, copy_tree=copy_with_concurrent_file)
            self.assertTrue((first / "old.txt").is_file())


class TestUsableRelease(unittest.TestCase):
    """FIX-002: A bundle is usable after extraction, not just a collection of skills."""

    def test_should_install_and_validate_from_extracted_bundle(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            package_release.build_release(base / "release", VERSION)
            extracted = base / "extracted"
            with zipfile.ZipFile(base / "release" / f"consulting-skills-lab-{VERSION}.zip") as archive:
                archive.extractall(extracted)
            outcomes = []
            for command in (
                ["scripts/install_skills.py", "--all", "--destination", str(base / "installed")],
                ["scripts/validate_skills.py"],
            ):
                result = subprocess.run([sys.executable, *command], cwd=extracted, capture_output=True, text=True, check=False)
                outcomes.append((result.returncode, result.stderr))
            self.assertEqual([(0, ""), (0, "")], outcomes)

    def test_should_build_identical_bytes_twice(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            first = package_release.build_release(base / "first", VERSION)
            second = package_release.build_release(base / "second", VERSION)
            self.assertEqual([p.read_bytes() for p in first], [p.read_bytes() for p in second])

    def test_should_reject_a_version_that_disagrees_with_catalog(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                package_release.build_release(Path(temp_dir), "999.0.0")

    def test_should_include_the_license_in_individual_skill_archives(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_release.build_release(Path(temp_dir), VERSION)
            with zipfile.ZipFile(Path(temp_dir) / f"{NAME}-{VERSION}.zip") as archive:
                self.assertIn(f"{NAME}/LICENSE", archive.namelist())
