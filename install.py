#!/usr/bin/env python3
"""Install the session contract into a project.

Copies the contract, the handoff, the journal, the templates and the validator
into a target repository, filling in the project name and today's date. It never
overwrites an existing file unless you pass --force, and it says what it skipped.

    python install.py ../my-project
    python install.py ../my-project --tools claude,cursor --ci
    python install.py ../my-project --dry-run

Standard library only. Python 3.8+.
"""

import argparse
import datetime
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent

POINTERS = {
    "claude": ("templates/pointers/CLAUDE.md", "CLAUDE.md"),
    "gemini": ("templates/pointers/GEMINI.md", "GEMINI.md"),
    "cursor": ("templates/pointers/.cursorrules", ".cursorrules"),
    "copilot": ("templates/pointers/copilot-instructions.md",
                ".github/copilot-instructions.md"),
}

CORE = [
    ("AGENTS.md", "AGENTS.md"),
    ("handoff.config.json", "handoff.config.json"),
    ("tools/check-handoff.py", "tools/check-handoff.py"),
    ("templates/state-of-play.md", "docs/state-of-play.md"),
    ("templates/session-template.md", "docs/session-template.md"),
    ("templates/JOURNAL.md", "JOURNAL.md"),
]


def fill(text, project, baseline):
    return (text.replace("{{PROJECT}}", project)
                .replace("{{DATE}}", datetime.date.today().isoformat())
                .replace("{{BASELINE}}", baseline))


def install_one(src, dest, project, baseline, force, dry_run, results):
    if dest.exists() and not force:
        results.append(("skip", dest, "already exists"))
        return
    text = src.read_text(encoding="utf-8-sig")
    if src.suffix in (".md", ".json"):
        text = fill(text, project, baseline)
    if dry_run:
        results.append(("would write", dest, ""))
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8", newline="\n")
    results.append(("wrote", dest, ""))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("target", help="path to the project repository")
    parser.add_argument("--name", help="project name (default: the directory name)")
    parser.add_argument("--baseline", default="not yet recorded",
                        help="value for the handoff's 'Evidence baseline:' line")
    parser.add_argument("--tools", default="claude",
                        help="comma-separated entry points to write: "
                             + ",".join(POINTERS) + ",all,none")
    parser.add_argument("--ci", action="store_true",
                        help="also install the GitHub Actions workflow")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="show what would happen")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.is_dir():
        raise SystemExit(f"Not a directory: {target}")
    if target == KIT:
        raise SystemExit("Refusing to install the kit into itself.")

    project = args.name or target.name
    chosen = [t.strip().lower() for t in args.tools.split(",") if t.strip()]
    if "all" in chosen:
        chosen = list(POINTERS)
    elif "none" in chosen:
        chosen = []
    unknown = [t for t in chosen if t not in POINTERS]
    if unknown:
        raise SystemExit(f"Unknown tool(s): {unknown}. Known: {list(POINTERS)}")

    plan = list(CORE) + [POINTERS[t] for t in chosen]
    if args.ci:
        plan.append((".github/workflows/handoff.yml", ".github/workflows/handoff.yml"))

    results = []
    for src_rel, dest_rel in plan:
        install_one(KIT / src_rel, target / dest_rel, project, args.baseline,
                    args.force, args.dry_run, results)

    width = max(len(a) for a, _, _ in results)
    for action, dest, note in results:
        line = f"  {action:<{width}}  {dest.relative_to(target)}"
        print(f"{line}   ({note})" if note else line)

    skipped = [d for a, d, _ in results if a == "skip"]
    print()
    if skipped:
        print(f"{len(skipped)} file(s) already existed and were left alone. "
              "Merge by hand, or re-run with --force.")
    if args.dry_run:
        print("Dry run: nothing was written.")
        return 0

    print("Next:")
    print(f"  1. Fill in the placeholders in {target.name}/docs/state-of-play.md")
    print(f"  2. Run: python tools/check-handoff.py   (from {target.name})")
    print("  3. Commit the contract before the next session, not after it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
