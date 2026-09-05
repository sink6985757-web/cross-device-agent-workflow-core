import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "project-lifecycle.template.json"
SCHEMA = ROOT / ".schemas" / "project-lifecycle.schema.json"
MODULE_PATH = ROOT / "scripts" / "project_lifecycle.py"
SPEC = importlib.util.spec_from_file_location("project_lifecycle", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ProjectLifecycleContractTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))

    def test_schema_and_template_are_valid_json(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.payload["schema_version"], 1)

    def test_template_passes_portable_validator(self):
        self.assertEqual(MODULE.validate_manifest(self.payload), [])
        self.assertEqual(self.payload["checkpoint"]["branch_policy"], "current-work-branch")
        self.assertEqual(self.payload["checkpoint"]["readback"], "remote-sha")

    def test_windows_unc_posix_and_home_absolute_paths_are_rejected(self):
        for bad_path in (
            "C:/" + "Users/example/project/AGENTS.md",
            "//server/share/AGENTS.md",
            "/" + "home/example/project/AGENTS.md",
            "~/project/AGENTS.md",
            "folder" + chr(92) + "AGENTS.md",
        ):
            with self.subTest(path=bad_path):
                payload = copy.deepcopy(self.payload)
                payload["paths"]["agents"] = bad_path
                self.assertTrue(MODULE.validate_manifest(payload))

    def test_parent_escape_is_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["checkpoint"]["allow_paths"].append("../outside")
        self.assertTrue(MODULE.validate_manifest(payload))

    def test_project_root_is_always_actual_git_root(self):
        payload = copy.deepcopy(self.payload)
        payload["routing"]["project_root"] = "part-example/project-example"
        errors = MODULE.validate_manifest(payload)
        self.assertTrue(any("project_root" in error for error in errors))

    def test_standing_scope_cannot_enable_force_push(self):
        payload = copy.deepcopy(self.payload)
        payload["checkpoint"]["mode"] = "standing_scoped"
        payload["checkpoint"]["force_push"] = True
        errors = MODULE.validate_manifest(payload)
        self.assertTrue(any("force_push" in error for error in errors))

    def test_malformed_allowlist_is_rejected_without_crashing(self):
        payload = copy.deepcopy(self.payload)
        payload["checkpoint"]["allow_paths"] = [{"unexpected": "object"}]
        errors = MODULE.validate_manifest(payload)
        self.assertTrue(any("allow_paths" in error for error in errors))

    def test_git_state_matrix(self):
        cases = {
            "CLEAN_SYNCED": dict(remote_matches=True, detached=False, has_upstream=True, dirty=False, ahead=0, behind=0),
            "DIRTY": dict(remote_matches=True, detached=False, has_upstream=True, dirty=True, ahead=0, behind=0),
            "AHEAD": dict(remote_matches=True, detached=False, has_upstream=True, dirty=False, ahead=1, behind=0),
            "BEHIND": dict(remote_matches=True, detached=False, has_upstream=True, dirty=False, ahead=0, behind=1),
            "DIVERGED": dict(remote_matches=True, detached=False, has_upstream=True, dirty=False, ahead=1, behind=1),
            "WRONG_REMOTE": dict(remote_matches=False, detached=False, has_upstream=True, dirty=False, ahead=0, behind=0),
        }
        for expected, inputs in cases.items():
            with self.subTest(expected=expected):
                self.assertEqual(MODULE.classify_state(**inputs), expected)

    def test_github_remote_identity_normalization(self):
        expected = "sink6985757-web/example"
        for remote in (
            "https://github.com/sink6985757-web/example.git",
            "git@github.com:sink6985757-web/example.git",
            "ssh://git@github.com/sink6985757-web/example.git",
        ):
            with self.subTest(remote=remote):
                self.assertEqual(MODULE.normalize_remote(remote), expected)


if __name__ == "__main__":
    unittest.main()
