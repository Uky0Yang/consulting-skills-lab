import json
import shutil
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from scripts import validate_skills

ROOT = Path(__file__).resolve().parents[1]


class TestValidatorRobustness(unittest.TestCase):
    """FIX-005: Validate syntax and bad inputs, not only metadata substrings."""

    def test_should_detect_a_secret_assignment(self):
        text = "pass" + "word = 'test-only-not-a-credential'"
        self.assertTrue(any(pattern.search(text) for _, pattern in validate_skills.SECRET_PATTERNS))

    def test_should_reject_invalid_frontmatter_yaml(self):
        self.assertIsNone(validate_skills.parse_frontmatter("---\nname: [unterminated\ndescription: text\n---\nbody"))

    def test_should_reject_duplicate_frontmatter_keys(self):
        self.assertIsNone(validate_skills.parse_frontmatter("---\nname: first\nname: second\ndescription: text\n---\nbody"))

    def test_should_accept_yaml_multiline_description(self):
        parsed = validate_skills.parse_frontmatter("---\nname: sample\ndescription: >-\n  A folded\n  description.\n---\nbody")
        self.assertEqual("A folded description.", parsed[0]["description"])

    def test_should_reject_invalid_interface_yaml(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = Path(temp_dir) / "executive-decision-memo"
            shutil.copytree(ROOT / "skills/executive-decision-memo", skill)
            (skill / "agents/openai.yaml").write_text("interface: [broken\n", encoding="utf-8")
            errors = []
            validate_skills.validate_skill(skill, errors)
            self.assertTrue(any("YAML" in error for error in errors))

    def test_should_reject_a_json_array_catalog_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "catalog.json"
            path.write_text("[]", encoding="utf-8")
            errors = []
            validate_skills.validate_catalog([], errors, catalog_path=path)
            self.assertTrue(errors)

    def test_should_accept_a_new_semantic_project_version(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "catalog.json"
            catalog = json.loads((ROOT / "data/skill-catalog.json").read_text(encoding="utf-8"))
            catalog["project_version"] = "2.4.9"
            path.write_text(json.dumps(catalog), encoding="utf-8")
            errors = []
            validate_skills.validate_catalog(sorted((ROOT / "skills").iterdir()), errors, catalog_path=path)
            self.assertEqual([], errors)

    def test_should_reject_malformed_evaluation_names_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "manifest.json"
            path.write_text(json.dumps({"skills": [{"skill": [], "scenarios": [1, 2]}]}), encoding="utf-8")
            errors = []
            validate_skills.validate_evaluations([], errors, manifest_path=path)
            self.assertTrue(errors)

    def test_should_detect_missing_evaluation_input_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            errors = []
            validate_skills.validate_evaluation_records(errors, root=Path(temp_dir))
            self.assertTrue(errors)

    def test_should_detect_a_spec_catalog_version_mismatch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "data").mkdir()
            (root / "data/skill-catalog.json").write_text('{"project_version": "1.0.1"}', encoding="utf-8")
            (root / "spec.yaml").write_text('version: "1.0.0"\n', encoding="utf-8")
            errors = []
            validate_skills.validate_versions(errors, root=root)
            self.assertTrue(errors)

    def check_links(self, text, files=None):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "sample.md"
            path.write_text(text, encoding="utf-8")
            for name, content in (files or {}).items():
                (root / name).write_text(content, encoding="utf-8")
            errors = []
            validate_skills.validate_markdown_links(path, errors)
            return errors

    def test_should_detect_a_missing_image(self):
        self.assertTrue(self.check_links("![Example](missing.png)"))

    def test_should_detect_a_missing_reference_style_image(self):
        self.assertTrue(self.check_links("![Example][picture]\n\n[picture]: absent.png\n"))

    def test_should_detect_an_undefined_link_reference(self):
        self.assertTrue(self.check_links("[Example][undefined]\n"))

    def test_should_detect_a_missing_heading_anchor(self):
        self.assertTrue(self.check_links("[Target](other.md#not-present)", {"other.md": "# Present\n"}))

    def test_should_accept_an_angle_bracket_path_with_spaces(self):
        self.assertEqual([], self.check_links("[Target](<my file.md#my-heading>)", {"my file.md": "# My heading\n"}))

    def test_should_ignore_example_links_inside_code_fences(self):
        self.assertEqual([], self.check_links("```markdown\n[Template](not-a-real-file.md)\n```\n"))

    def test_should_check_an_external_http_failure(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(404)
                self.end_headers()

            def log_message(self, *args):
                pass

        with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    path = Path(temp_dir) / "external.md"
                    path.write_text(f"[Missing](http://127.0.0.1:{server.server_port}/missing)", encoding="utf-8")
                    errors = []
                    validate_skills.validate_markdown_links(path, errors, check_external=True)
                    self.assertTrue(any("HTTP 404" in error for error in errors))
            finally:
                server.shutdown()
