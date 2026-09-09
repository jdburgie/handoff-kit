# handoff-kit

A **pickup and session-end contract** for AI-assisted projects, plus a validator
that keeps it honest. Drop it into any repository, in any language, with any
model or tool.

The problem it solves is not that AI assistants forget. It is that they *resume
confidently* — from a stale checkout, from a summary that was optimistic, from
"it works" that meant "it compiled". This kit makes each session hand the next
one something structured, dated, and checkable.

**Tool-agnostic by construction.** The contract lives in `AGENTS.md`. Every tool's
entry file (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`,
`.github/copilot-instructions.md`) is a two-line pointer to it, so there is one
set of rules rather than five that drift apart.

---

## What gets installed

```
AGENTS.md                    the contract: pickup, evidence, session end
docs/state-of-play.md        the live handoff — one file, updated in place
docs/session-template.md     the shape of a journal entry
JOURNAL.md                   dated records, newest first, never rewritten
tools/check-handoff.py       the validator (standard library only)
handoff.config.json          word limits, section names, required files
CLAUDE.md / .cursorrules …   pointers to AGENTS.md, one per tool you use
```

## Install

```bash
git clone https://github.com/<you>/handoff-kit
python handoff-kit/install.py ../my-project --tools claude,cursor --ci
cd ../my-project && python tools/check-handoff.py
```

`--tools` takes `claude`, `gemini`, `cursor`, `copilot`, `all`, or `none`.
`--ci` adds a GitHub Actions workflow. `--dry-run` shows the plan. **Existing
files are never overwritten** unless you pass `--force`; the installer tells you
what it skipped so you can merge by hand.

Then fill in the placeholders in `docs/state-of-play.md`. Until you do, the
handoff describes the template rather than your project.

## The three ideas

**1 — One handoff, updated in place.** Not a pile of summaries. `state-of-play.md`
is always current, always short (800 words by default), and finished items are
deleted rather than accumulated. A handoff nobody reads is the same as no handoff.

**2 — Evidence has a vocabulary.** `BUILT` is not `DEPLOYED` is not `VERIFIED`.
Code establishes what is implemented; a passing test establishes that test's
result; an observation establishes behaviour on one instance at one time. **None
substitutes for another**, and every claim is scoped to what, where, and when.
"Not observed" is the honest phrase, not "did not happen".

**3 — The journal is append-only.** Entries are prepended, never rewritten. A
correction is a new entry linking to what it supersedes, so the reasoning that
produced the mistake survives alongside the fix.

## What the validator checks

```
python tools/check-handoff.py
python tools/check-handoff.py --base origin/main     # in CI
```

- the contract, handoff, journal and template all exist
- the handoff has the right sections in the right order, the required
  `Updated:` / `Evidence baseline:` / `Session status:` lines, an ISO date that is
  not in the future, and an explicit `Completion condition:`
- it is under the word limit, and it warns when it has gone stale
- journal anchors are unique, and the handoff links the newest one
- every relative markdown link resolves
- tool entry files point at `AGENTS.md` and stay short instead of restating it
- with `--base`: a branch that changed the project also updated the record

> ⚠️ **It enforces structure, not truth.** It can confirm a handoff exists, is
> current, is short, and points where it claims. It cannot confirm any of it is
> accurate. That part is still a person reading the evidence.

## Adapting it

Everything the validator enforces is in `handoff.config.json` — section names,
word limits, required files, the anchor prefix, which paths count as "the record".
Change them there and in the templates together.

Common local additions:

- **a capability or claims register** — one row per capability with its status,
  date, and evidence link; add it to `required_files`
- **an issues file** with a stable ID scheme, so a handoff can point at an item
  rather than re-describe it
- **domain sections** in the handoff — hardware projects want the last observed
  physical state; services want the deployed version and environment

The contract is meant to be edited. It is a working agreement, not a standard.

## Provenance

Extracted from a hardware project where the pattern earned itself: sessions moved
between machines and tools, boards were flashed but not observed, and "verified"
had quietly come to mean three different things. The rules in `AGENTS.md` each
exist because something went wrong without them — the table at the end of that
file says which.

MIT licensed. Use it, fork it, strip it down.
