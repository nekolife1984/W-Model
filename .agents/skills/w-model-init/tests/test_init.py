from __future__ import annotations

import importlib.util
import os
import stat
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts/init.py"
SPEC = importlib.util.spec_from_file_location("w_model_init", SCRIPT)
init = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(init)


class SetupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        template_path = self.root / init.TEMPLATE
        template_path.parent.mkdir(parents=True)
        template_path.write_text(SCRIPT.parents[3].joinpath("templates/w-model/AGENTS.md.template").read_text(encoding="utf-8"), encoding="utf-8")
        for rel in (
            ".agents/docs/w-model/00-index.md", ".agents/docs/w-model/08-end-to-end-workflow.md",
            ".agents/docs/w-model/02-requirements-and-acceptance.md", ".agents/docs/w-model/03-architecture-and-system-test.md",
            ".agents/docs/w-model/04-task-decomposition-and-detailed-design.md", ".agents/docs/w-model/05-implementation-and-unit-testing.md",
            ".agents/docs/w-model/06-traceability.md", ".agents/docs/w-model/07-test-operations-and-qa.md",
            ".agents/skills/w-model-workflow/SKILL.md", ".agents/skills/w-model-requirements/SKILL.md",
            ".agents/skills/w-model-architecture/SKILL.md", ".agents/skills/w-model-task-design/SKILL.md",
            ".agents/skills/w-model-implementation/SKILL.md", ".agents/skills/w-model-traceability/SKILL.md",
            ".agents/skills/w-model-qa/SKILL.md", ".agents/skills/aide-workflow/SKILL.md",
        ):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("link target\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_creates_and_reruns_idempotently(self) -> None:
        self.assertIn("作成", init.setup(self.root))
        first = (self.root / "AGENTS.md").read_bytes()
        self.assertIn("# W-Model 開発案内", first.decode())
        self.assertIn("変更なし", init.setup(self.root))
        self.assertEqual(first, (self.root / "AGENTS.md").read_bytes())

    def test_appends_without_changing_existing_content_and_shifts_headings(self) -> None:
        original = "# Project Rules\n\nKeep this exact.\n"
        (self.root / "AGENTS.md").write_text(original, encoding="utf-8")
        init.setup(self.root)
        result = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertTrue(result.startswith(original))
        self.assertIn("## W-Model 開発案内", result)
        self.assertIn("### 作業の進め方", result)

    def test_conflicting_edit_is_not_overwritten(self) -> None:
        (self.root / "AGENTS.md").write_text("# Existing\n", encoding="utf-8")
        init.setup(self.root)
        path = self.root / "AGENTS.md"
        path.write_text(path.read_text(encoding="utf-8") + "手編集\n", encoding="utf-8")
        before = path.read_bytes()
        with self.assertRaises(init.SetupError):
            init.setup(self.root)
        self.assertEqual(before, path.read_bytes())

    def test_duplicate_section_is_not_changed(self) -> None:
        path = self.root / "AGENTS.md"
        section = init._render((self.root / init.TEMPLATE).read_text(encoding="utf-8"), 1)
        path.write_text(section + "\n\n" + section + "\n", encoding="utf-8")
        before = path.read_bytes()
        with self.assertRaises(init.SetupError):
            init.setup(self.root)
        self.assertEqual(before, path.read_bytes())

    def test_symlink_and_invalid_utf8_are_rejected_without_write(self) -> None:
        target = self.root / "external"
        target.write_text("external\n", encoding="utf-8")
        (self.root / "AGENTS.md").symlink_to(target)
        with self.assertRaises(init.SetupError):
            init.setup(self.root)
        self.assertEqual("external\n", target.read_text(encoding="utf-8"))
        (self.root / "AGENTS.md").unlink()
        (self.root / "AGENTS.md").write_bytes(b"\xff")
        before = (self.root / "AGENTS.md").read_bytes()
        with self.assertRaises(init.SetupError):
            init.setup(self.root)
        self.assertEqual(before, (self.root / "AGENTS.md").read_bytes())

    def test_template_and_parent_symlinks_are_rejected(self) -> None:
        template = self.root / init.TEMPLATE
        actual = template.with_suffix(".real")
        template.rename(actual)
        template.symlink_to(actual)
        with self.assertRaises(init.SetupError):
            init.setup(self.root)
        template.unlink()
        actual.rename(template)

        agents = self.root / ".agents"
        backup = self.root / "agents-real"
        agents.rename(backup)
        agents.symlink_to(backup, target_is_directory=True)
        with self.assertRaises(init.SetupError):
            init.setup(self.root)
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_template_link_must_resolve_inside_repository(self) -> None:
        path = self.root / init.TEMPLATE
        path.write_text(path.read_text(encoding="utf-8").replace(".agents/docs/w-model/00-index.md", "../../outside.md"), encoding="utf-8")
        with self.assertRaises(init.SetupError):
            init.setup(self.root)
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_encoded_and_title_bearing_links_are_rejected(self) -> None:
        path = self.root / init.TEMPLATE
        original = path.read_text(encoding="utf-8")
        for link in ("%2e%2e/outside.md", ".agents/docs/w-model/00-index.md 'title'"):
            with self.subTest(link=link):
                path.write_text(original.replace(".agents/docs/w-model/00-index.md", link), encoding="utf-8")
                with self.assertRaises(init.SetupError):
                    init.setup(self.root)
                self.assertFalse((self.root / "AGENTS.md").exists())
        path.write_text(original, encoding="utf-8")

    def test_concurrent_destination_change_is_not_overwritten(self) -> None:
        destination = self.root / "AGENTS.md"
        destination.write_text("# Original\n", encoding="utf-8")
        original_writer = init._write_atomic

        def race(root: Path, content: bytes, original: bytes | None, mode: int | None = None) -> None:
            destination.write_text("# Concurrent edit\n", encoding="utf-8")
            original_writer(root, content, original, mode)

        with patch.object(init, "_write_atomic", side_effect=race):
            with self.assertRaises(init.SetupError):
                init.setup(self.root)
        self.assertEqual("# Concurrent edit\n", destination.read_text(encoding="utf-8"))

    def test_special_destination_is_rejected_and_mode_is_preserved(self) -> None:
        destination = self.root / "AGENTS.md"
        os.mkfifo(destination)
        with self.assertRaises(init.SetupError):
            init.setup(self.root)
        destination.unlink()
        destination.write_text("# Existing\n", encoding="utf-8")
        destination.chmod(0o640)
        init.setup(self.root)
        self.assertEqual(0o640, stat.S_IMODE(destination.stat().st_mode))

    def test_headings_inside_fenced_code_are_ignored(self) -> None:
        destination = self.root / "AGENTS.md"
        destination.write_text("````markdown\n# Sample\n## W-Model 開発案内\n````\n", encoding="utf-8")
        init.setup(self.root)
        result = destination.read_text(encoding="utf-8")
        self.assertTrue(result.startswith("````markdown\n# Sample\n## W-Model 開発案内\n````\n"))
        headings = init._headings(result)
        self.assertEqual(2, len(headings))
        self.assertEqual("W-Model 開発案内", headings[0].group(3))
        self.assertEqual("作業の進め方", headings[1].group(3))
        self.assertEqual(1, len(headings[0].group(2)))


if __name__ == "__main__":
    unittest.main()
