#!/usr/bin/env python3
"""Validate a project's session-contract handoff.

Checks structure, size, dates, local links and journal anchors. Standard library
only, runs from any working directory, and exits non-zero on the first set of
errors so it can gate CI.

It enforces structure, not truth: it cannot tell you whether a handoff is honest,
only whether it exists, is current, is short, and points where it claims to.

    python tools/check-handoff.py
    python tools/check-handoff.py --config handoff.config.json
    python tools/check-handoff.py --base origin/main    # CI: changed code needs a record
"""

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

DEFAULTS = {
    "handoff": "docs/state-of-play.md",
    "journal": "JOURNAL.md",
    "template": "docs/session-template.md",
    "contract": "AGENTS.md",
    "entry_points": ["CLAUDE.md"],
    "required_files": [],
    "max_words": 800,
    "max_entry_point_words": 150,
    "stale_after_days": 30,
    "sections": [
        "Current objective",
        "Recent observations",
        "Active work and constraints",
        "Completed work",
        "Next action",
        "Open questions and parked work",
        "Evidence and session record",
    ],
    "fields": ["Updated", "Evidence baseline", "Session status"],
    "anchor_prefix": "session-",
    "record_paths": [],
    "ignore_paths": [],
}


def load_config(root, path):
    cfg = dict(DEFAULTS)
    candidate = Path(path) if path else root / "handoff.config.json"
    if candidate.is_file():
        try:
            cfg.update(json.loads(candidate.read_text(encoding="utf-8-sig")))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Cannot parse {candidate}: {exc}")
    elif path:
        raise SystemExit(f"Config not found: {candidate}")
    if not cfg["record_paths"]:
        cfg["record_paths"] = [cfg["handoff"], cfg["journal"]]
    return cfg


def repo_root(start):
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(start), capture_output=True, text=True, check=True,
        )
        return Path(out.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return start


def read(root, name):
    path = root / name
    return path.read_text(encoding="utf-8-sig") if path.is_file() else None


def check_links(root, name, text, errors):
    """Every relative markdown link must resolve to a file in the repo."""
    base = (root / name).parent
    for target in re.findall(r"\]\(([^)]+)\)", text):
        target = target.strip().split(" ")[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        resolved = (base / unquote(parts.path)).resolve()
        if not resolved.exists():
            errors.append(f"{name}: link does not resolve: {target}")


def check_handoff(root, cfg, text, errors, warnings):
    name = cfg["handoff"]

    words = len(text.split())
    if words > cfg["max_words"]:
        errors.append(f"{name} is {words} words; maximum is {cfg['max_words']}")

    found = re.findall(r"^## (.+?)\s*$", text, re.M)
    if cfg["sections"] and found != cfg["sections"]:
        errors.append(
            f"{name} sections must match the template, in order.\n"
            f"      expected: {cfg['sections']}\n"
            f"      found:    {found}"
        )

    for field in cfg["fields"]:
        if not re.search(rf"^{re.escape(field)}:\s*\S.*$", text, re.M):
            errors.append(f"{name} needs a '{field}:' line")

    stamped = re.search(r"^Updated:\s*(\S+)", text, re.M)
    if stamped:
        try:
            when = datetime.date.fromisoformat(stamped.group(1))
        except ValueError:
            errors.append(f"{name}: 'Updated:' must be an ISO date (YYYY-MM-DD)")
        else:
            today = datetime.date.today()
            if when > today:
                errors.append(f"{name}: 'Updated:' is in the future ({when})")
            age = (today - when).days
            if cfg["stale_after_days"] and age > cfg["stale_after_days"]:
                warnings.append(
                    f"{name} was updated {age} days ago; treat its specifics as stale"
                )

    if "Completion condition:" not in text:
        errors.append(f"{name}: the next action needs an explicit 'Completion condition:'")


def check_journal(root, cfg, text, handoff, errors):
    name = cfg["journal"]
    anchors = re.findall(rf'<a id="({re.escape(cfg["anchor_prefix"])}[^"]+)"', text)
    if not anchors:
        errors.append(
            f"{name}: no session anchors found "
            f'(entries need <a id="{cfg["anchor_prefix"]}YYYY-MM-DD-topic"></a>)'
        )
        return
    duplicates = {a for a in anchors if anchors.count(a) > 1}
    if duplicates:
        errors.append(f"{name}: anchors must be unique; repeated {sorted(duplicates)}")
    newest = anchors[0]
    if handoff is not None and f"#{newest}" not in handoff:
        errors.append(
            f"{cfg['handoff']} must link the newest journal entry (#{newest})"
        )


def check_entry_points(root, cfg, errors, warnings):
    contract = cfg["contract"]
    for name in cfg["entry_points"]:
        text = read(root, name)
        if text is None:
            warnings.append(f"{name} not present; skipping (no {contract} pointer)")
            continue
        if contract not in text:
            errors.append(f"{name} must point at {contract}, not restate the rules")
        words = len(text.split())
        if words > cfg["max_entry_point_words"]:
            errors.append(
                f"{name} is {words} words; an entry point must stay a short pointer "
                f"(max {cfg['max_entry_point_words']}). Put the rules in {contract}."
            )


def changed_files(root, base):
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...HEAD"],
            cwd=str(root), capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as exc:
        raise SystemExit(f"Cannot diff against {base}: {exc}")
    return [line for line in out.stdout.splitlines() if line.strip()]


def check_base(root, cfg, base, errors):
    """If this branch changed anything substantive, it must also change the record."""
    changed = changed_files(root, base)
    if not changed:
        return
    records = set(cfg["record_paths"])
    ignored = tuple(cfg["ignore_paths"])
    substantive = [
        f for f in changed
        if f not in records and not (ignored and f.startswith(ignored))
    ]
    if substantive and not (records & set(changed)):
        errors.append(
            f"changes against {base} touch {len(substantive)} file(s) but update "
            f"neither {' nor '.join(sorted(records))}.\n"
            f"      first few: {substantive[:5]}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--config", help="path to handoff.config.json")
    parser.add_argument("--root", help="project root (default: the git root)")
    parser.add_argument("--base", help="git ref: require a record update for changes since it")
    parser.add_argument("--quiet", action="store_true", help="only print problems")
    args = parser.parse_args()

    start = Path(args.root).resolve() if args.root else Path.cwd()
    root = start if args.root else repo_root(Path(__file__).resolve().parent)
    cfg = load_config(root, args.config)

    errors, warnings = [], []

    required = [cfg["contract"], cfg["handoff"], cfg["journal"], cfg["template"]]
    required += list(cfg["required_files"])
    texts = {}
    for name in required:
        text = read(root, name)
        if text is None:
            errors.append(f"missing {name}")
        else:
            texts[name] = text

    if not errors:
        handoff = texts[cfg["handoff"]]
        check_handoff(root, cfg, handoff, errors, warnings)
        check_journal(root, cfg, texts[cfg["journal"]], handoff, errors)
        check_entry_points(root, cfg, errors, warnings)
        for name, text in texts.items():
            check_links(root, name, text, errors)

    if args.base:
        check_base(root, cfg, args.base, errors)

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"\n{len(errors)} problem(s). See {cfg['contract']}.")
        return 1
    if not args.quiet:
        print(
            "Handoff structure, links and anchors OK.\n"
            "This checks structure, not truth: read the evidence and the "
            "contradictions yourself."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
