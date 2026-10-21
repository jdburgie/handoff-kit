#!/usr/bin/env python3
"""Kit self-check: the skill installs from a standalone copy, the validator catches
what it claims to, --upgrade refreshes a drifted copy, and the repository's own
installed files match the skill. Standard library only.

    python tests/test_kit.py
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "handoff-kit"

# root path -> canonical path inside the skill
INSTALLED_COPIES = {
    "AGENTS.md": "AGENTS.md",
    "handoff.config.json": "handoff.config.json",
    "LICENSE": "LICENSE",
    "tools/check-handoff.py": "tools/check-handoff.py",
    "docs/session-template.md": "templates/session-template.md",
    ".github/workflows/handoff.yml": "templates/ci/handoff.yml",
}


def run(*args, cwd=None):
    return subprocess.run([sys.executable, *map(str, args)], cwd=cwd,
                          capture_output=True, text=True)


class Kit(unittest.TestCase):
    def setUp(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        # A copy outside the repository proves the skill folder is self-contained.
        self.skill = shutil.copytree(SKILL, tmp / "skill")
        self.project = tmp / "project"
        self.project.mkdir()
        out = run(self.skill / "install.py", self.project, "--tools", "all", "--ci")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)

    def check(self, *extra):
        return run(self.project / "tools/check-handoff.py", "--root", self.project, *extra)

    def edit(self, name, old, new):
        path = self.project / name
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def config(self, **values):
        path = self.project / "handoff.config.json"
        cfg = json.loads(path.read_text(encoding="utf-8"))
        cfg.update(values)
        path.write_text(json.dumps(cfg), encoding="utf-8")

    def assertFails(self, message, *extra):
        out = self.check(*extra)
        self.assertEqual(out.returncode, 1, out.stdout)
        self.assertIn(message, out.stdout)

    def test_fresh_install_passes(self):
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout)

    def test_missing_marker(self):
        self.edit("JOURNAL.md", "<!-- SESSION ENTRIES -->", "")
        self.assertFails("missing session insertion marker")

    def test_broken_heading_fragment(self):
        self.edit("docs/state-of-play.md", "## Next action",
                  "## Next action\n\nSee [nowhere](../AGENTS.md#no-such-heading).")
        self.assertFails("link fragment does not resolve")

    def test_valid_heading_fragment_and_code_block(self):
        self.edit("docs/state-of-play.md", "## Next action",
                  "## Next action\n\nSee [pickup](../AGENTS.md#pickup).\n\n"
                  "```\n[example](../missing.md)\n```")
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout)

    def test_link_leaving_repository(self):
        self.edit("docs/state-of-play.md", "## Next action",
                  "## Next action\n\nSee [outside](../../elsewhere.md).")
        self.assertFails("link leaves the repository")

    def test_handoff_must_link_newest_entry(self):
        self.edit("JOURNAL.md", "<!-- SESSION ENTRIES -->",
                  '<!-- SESSION ENTRIES -->\n\n<a id="session-2099-01-01-newer"></a>\n'
                  "## 2099-01-01 Newer")
        self.assertFails("must link the newest journal entry")

    def test_journal_sections(self):
        sections = ["Objective and constraints", "Changes and decisions",
                    "Validation and evidence", "State at the end",
                    "Next action and completion condition", "Do not repeat"]
        self.config(journal_sections=sections)
        self.assertEqual(self.check().returncode, 0)
        self.config(journal_sections=sections[::-1])
        self.assertFails("newest entry sections must match")

    def test_require_all_records(self):
        if not shutil.which("git"):
            self.skipTest("git not available")
        git = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false"]
        for cmd in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "base"]):
            subprocess.run(git + cmd, cwd=self.project, check=True)
        base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.project,
                              capture_output=True, text=True).stdout.strip()
        (self.project / "code.py").write_text("x = 1\n")
        self.edit("JOURNAL.md", "<!-- SESSION ENTRIES -->", "<!-- SESSION ENTRIES -->\n")
        for cmd in (["add", "-A"], ["commit", "-qm", "change"]):
            subprocess.run(git + cmd, cwd=self.project, check=True)
        self.assertEqual(self.check("--base", base).returncode, 0)
        self.config(require_all_records=True)
        self.assertFails("also require a record update: docs/state-of-play.md",
                         "--base", base)

    def test_upgrade_replaces_drifted_validator(self):
        validator = self.project / "tools/check-handoff.py"
        validator.write_text("# old copy\n")
        out = run(self.skill / "install.py", self.project, "--upgrade")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(validator.read_bytes(),
                         (self.skill / "tools/check-handoff.py").read_bytes())
        self.assertEqual(self.check().returncode, 0)


class RepositoryCopies(unittest.TestCase):
    def test_root_copies_match_skill(self):
        for root_path, skill_path in INSTALLED_COPIES.items():
            with self.subTest(root_path):
                self.assertEqual((REPO / root_path).read_bytes(),
                                 (SKILL / skill_path).read_bytes(),
                                 f"{root_path} has drifted from skills/handoff-kit/{skill_path}")


if __name__ == "__main__":
    unittest.main()
