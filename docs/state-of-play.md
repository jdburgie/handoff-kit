# handoff-kit — pickup

Updated: 2026-09-08
Evidence baseline: initial commit (no prior history)
Session status: First build complete; validator run against the kit itself and a
scratch install. Not yet used by a second project.

## Current objective

Make the pickup / session-end pattern from a private hardware project reusable by
any repository, under any AI tool, and keep it honest with a validator that runs
without dependencies. The kit follows its own contract — this file and
[the journal](../JOURNAL.md) are the demonstration.

## Recent observations

| Thing | Last state | Observation and limitation |
|---|---|---|
| `tools/check-handoff.py` | `VERIFIED` 2026-09-08 against this repo | Exits 0 here, and reports real errors when sections, anchors, dates or links are wrong. Not yet run under CI on GitHub. |
| `install.py` | `VERIFIED` 2026-09-08 into a scratch directory | Fills placeholders, skips existing files, and the installed tree passes the validator. Tested on Windows only. |
| `.github/workflows/handoff.yml` | `ABSENT` from any real run | Written, never executed — no push has happened yet. |

## Active work and constraints

Nothing running. No remote exists yet: the repository is local, and the user will
create the GitHub repository before anything is pushed. Do not add a second pickup
document — extending `AGENTS.md` and this file is the whole point.

## Completed work

- `AGENTS.md`: the contract — pickup, evidence vocabulary, rules for irreversible
  actions, session end, and a table of the failure each rule prevents.
- Templates for the handoff, the journal, and the session record, plus pointer
  files for Claude, Gemini, Cursor and Copilot that link the contract instead of
  restating it.
- `tools/check-handoff.py`: structure, sections, fields, ISO dates, word limit,
  staleness warning, unique journal anchors, newest anchor linked, relative links
  resolve, entry points stay short, and `--base` for CI.
- `handoff.config.json`: every enforced value is configurable in one place.
- `install.py`: non-destructive install with `--tools`, `--ci`, `--dry-run`,
  `--force`.

## Next action

Create the GitHub repository, add the remote, and push. Then install the kit into
one real project other than its source, and fix whatever that reveals.

Completion condition: a second project passes `python tools/check-handoff.py`
after an install that needed no hand-editing of the validator. Uncertain until
then: whether the default sections suit a software-only project, since they were
generalized from a hardware one.

## Open questions and parked work

- The CI workflow's whitespace step is written defensively and always exits 0;
  decide whether it should fail the build once it has run for real.
- No test suite for the validator itself. A handful of fixture repositories —
  one valid, several broken in specific ways — would be worth more than any
  further feature.
- Parked deliberately: no packaging, no installer beyond a script, no GitHub
  Action published to the marketplace.

## Evidence and session record

- [First build](../JOURNAL.md#session-2026-09-08-build-the-kit).
- The pattern's origin is a private repository; the generalization here was
  written fresh rather than copied, and no private content is included.
