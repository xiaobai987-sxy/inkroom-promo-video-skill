import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def test_init_and_manifest_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            subprocess.run(
                [sys.executable, str(ROOT / "scripts/init_project.py"), str(project), "--project-id", "demo"],
                check=True,
                capture_output=True,
                text=True,
            )
            state = project / "workflow/state.json"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_manifest.py"), "--state", str(state), "--json"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(json.loads(result.stdout)["ok"])

    def test_rejected_transition_requires_valid_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            subprocess.run([sys.executable, str(ROOT / "scripts/init_project.py"), str(project)], check=True, capture_output=True)
            state = project / "workflow/state.json"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/state.py"), "transition", str(state), "--stage", "qa_pass"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)

    def test_fact_lock_requires_explicit_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            subprocess.run([sys.executable, str(ROOT / "scripts/init_project.py"), str(project)], check=True, capture_output=True)
            state = project / "workflow/state.json"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/state.py"), "transition", str(state), "--stage", "facts_locked"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)

    def test_manifest_is_auto_discovered_next_to_state(self):
        fixture = ROOT / "examples/inkroom-v6-reference"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_manifest.py"), "--state", str(fixture / "workflow/state.json"), "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(result.stdout)["shot_count"], 3)


if __name__ == "__main__":
    unittest.main()
