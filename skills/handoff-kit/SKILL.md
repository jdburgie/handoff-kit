---
name: handoff-kit
description: Pickup and session-end contract for AI-assisted projects. One AGENTS.md every tool points at, a short living handoff, an append-only journal, and a dependency-free validator. Use when the user wants to install a session contract or handoff into a repository, resume or pick up work in a repository that has docs/state-of-play.md, end or hand off a session, write a journal entry, validate a handoff, or upgrade a repository's copy of check-handoff.py.
license: MIT
metadata:
  version: "1.0.0"
  source: https://github.com/jdburgie/handoff-kit
---

# handoff-kit

A repository using this kit has `AGENTS.md` (the contract), `docs/state-of-play.md`
(the live handoff), `JOURNAL.md` (dated records, newest first), and
`tools/check-handoff.py` (the validator), configured by `handoff.config.json`.

**`AGENTS.md` in the target repository is the authority.** This file only routes to
it. Never restate or override its rules here. Instructions from the user take
precedence over both.

Paths below that start with `install.py`, `tools/` or `templates/` are relative to
this skill's own directory. Run Python as `python`, or `py` on Windows if `python`
is not found. Everything is standard library only, Python 3.8+.

Pick the mode from the request:

| The user wants to... | Mode |
|---|---|
| add the contract to a repository that has no `AGENTS.md` handoff yet | Install |
| start, resume, or "pick up" work in a repository that has the kit | Pickup |
| wrap up, hand off, or end a session; write the journal entry | Session end |
| refresh an old or drifted `tools/check-handoff.py` | Upgrade |

## Install

1. Look for a handoff the project already has: a "current state" block in a
   journal, a `HANDOFF*.md`, a pinned issue. If one exists, plan to move its content
   into `docs/state-of-play.md` and mark the original superseded. Two pickup
   documents are worse than none.
2. Preview, then install. Ask which tools the user works with; the default is
   `claude`. Choices are `claude`, `gemini`, `cursor`, `copilot`, `all`, `none`.
   Add `--ci` only if the project is on GitHub and the user wants the check in CI.

   ```
   python install.py <repo> --tools claude,cursor --ci --dry-run
   python install.py <repo> --tools claude,cursor --ci
   ```

   Existing files are never overwritten. Report what was skipped. If `JOURNAL.md`
   was skipped, add a `<!-- SESSION ENTRIES -->` marker and one anchored entry
   (`<a id="session-YYYY-MM-DD-topic"></a>`) by hand. Do not rewrite older entries.
3. Replace every placeholder in `docs/state-of-play.md` with the project's real
   objective, last observed state, and one next action with a
   `Completion condition:`. Use the user's knowledge and the repository; write
   "unknown" rather than inventing anything.
4. Run `python tools/check-handoff.py` from the repository and fix what it reports.

## Pickup

Follow the Pickup section of the repository's `AGENTS.md`. In short: read
`docs/state-of-play.md` in full, check `git status -sb` and recent commits (fetch if
the network allows), read the newest journal entry it links, and state a short
summary before acting. That summary covers the objective, established facts, the
unresolved point, and the next action. A recorded next action is context, not
permission.

## Session end

Follow the Session end section of the repository's `AGENTS.md`, using
`docs/session-template.md` for the journal entry. Skip it for a read-only answer
that produced no durable finding.

1. Prepend one journal entry directly after `<!-- SESSION ENTRIES -->`, with a new
   unique anchor.
2. Update `docs/state-of-play.md` in place: remove finished items, keep it under the
   word limit, set `Updated:` to today and `Evidence baseline:` to the commit
   actually inspected, and link the new anchor.
3. Run `python tools/check-handoff.py` until it passes. On a branch, also run
   `python tools/check-handoff.py --base origin/<default-branch>`.
4. Commit or push only when the user has authorized it, and report what was
   validated and what was not.

## Upgrade

1. If the repository has no `handoff.config.json` and its validator hardcodes
   section names, required files, or limits, write those into a
   `handoff.config.json` first. Use `handoff.config.json` in this skill as the shape.
2. Preview, then apply:

   ```
   python install.py <repo> --upgrade --dry-run
   python install.py <repo> --upgrade
   ```

   This replaces only `tools/check-handoff.py`, plus
   `.github/workflows/handoff.yml` if the repository already has one. It reports
   whether `AGENTS.md` and `docs/session-template.md` differ from the kit. Those
   differences may be deliberate local adaptations: show them to the user rather
   than overwriting them.
3. Run `python tools/check-handoff.py`. The upgraded validator is stricter about
   links: heading fragments must resolve, links must stay inside the repository,
   and the handoff must link the newest journal entry exactly. Fix what it
   reports in the documents, not by weakening the check.

## Limits

The validator enforces structure and links, not truth. A passing check means the
handoff exists, is current, is short, and points where it claims. Whether it is
accurate still needs someone to read the evidence.
