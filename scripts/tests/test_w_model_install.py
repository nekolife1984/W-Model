from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "w_model_install.py"
MANIFEST = ROOT / "scripts" / "w_model_install_manifest.json"


class WModelInstallTests(unittest.TestCase):
    def run_installer(self, target: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(target), *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_manifest_contains_only_w_model_assets_and_existing_sources(self) -> None:
        files = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
        self.assertEqual(len(files), len(set(files)))
        for item in files:
            self.assertTrue(item.startswith((".agents/docs/w-model/", ".agents/skills/w-model-", ".agents/templates/w-model/")), item)
            self.assertTrue((ROOT / item).is_file(), item)
        self.assertNotIn("AGENTS.md", files)
        self.assertNotIn(".agents/project.json", files)

    def test_dry_run_does_not_modify_target_and_reports_additions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            result = self.run_installer(target, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("[追加] .agents/docs/w-model/00-index.md", result.stdout)
            self.assertEqual(list(target.iterdir()), [])

    def test_apply_is_idempotent_and_preserves_protected_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "AGENTS.md").write_text("user instructions\n", encoding="utf-8")
            agents = target / ".agents"
            agents.mkdir()
            project = agents / "project.json"
            project.write_text('{"local":true}\n', encoding="utf-8")

            first = self.run_installer(target, "--apply")
            self.assertEqual(first.returncode, 0, first.stderr)
            installed = agents / "docs/w-model/00-index.md"
            expected = (ROOT / ".agents/docs/w-model/00-index.md").read_bytes()
            self.assertEqual(installed.read_bytes(), expected)
            self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), "user instructions\n")
            self.assertEqual(project.read_text(encoding="utf-8"), '{"local":true}\n')

            second = self.run_installer(target, "--apply")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("[同一] .agents/docs/w-model/00-index.md", second.stdout)
            self.assertIn("導入完了: 0ファイル", second.stdout)

    def test_any_conflict_stops_all_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            conflict = target / ".agents/docs/w-model/00-index.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("locally modified\n", encoding="utf-8")

            result = self.run_installer(target, "--apply")
            self.assertEqual(result.returncode, 1)
            self.assertIn("[競合] .agents/docs/w-model/00-index.md", result.stdout)
            self.assertEqual(conflict.read_text(encoding="utf-8"), "locally modified\n")
            self.assertFalse((target / ".agents/skills/w-model-workflow/SKILL.md").exists())

    def test_node_cli_dispatches_to_python_installer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                ["node", str(ROOT / "bin/w-model-install.js"), directory, "--dry-run"],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("モード: dry-run", result.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
