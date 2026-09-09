# handoff-kit — pickup

Updated: 2026-09-08
Evidence baseline: `8dbffd1`, pushed to `origin/main`
Session status: Published public and CI green on first run. Not yet used by a
second project.

## Current objective

Make the pickup / session-end pattern from a private hardware project reusable by
any repository, under any AI tool, and keep it honest with a validator that runs
without dependencies. The kit follows its own contract — this file and
[the journal](../JOURNAL.md) are the demonstration.

## Recent observations

| Thing | Last state | Observation and limitation |
|---|---|---|
| `tools/check-handoff.py` | `VERIFIED` 2026-09-08 on Windows/Python 3.12 **and** in CI on ubuntu-latest | Exits 0 on this repo, and eight negative cases each produce their intended error. Portability now rests on one Linux run, not an assumption. |
| `install.py` | `VERIFIED` 2026-09-08 into a scratch directory | Fills placeholders, skips existing files, and the installed tree passes the validator. Tested on Windows only. |
| `.github/workflows/handoff.yml` | `VERIFIED` on `8dbffd1`, run [34307145554](https://github.com/jdburgie/handoff-kit/actions/runs/34307145554) | Green in ~5s on ubuntu-latest: checkout, setup-python, validate, whitespace. ⚠️ The `--base` step is `pull_request`-only and was **skipped** — never exercised on GitHub. |

## Active work and constraints

Nothing running. The repository is **public** at `jdburgie/handoff-kit`, so
anything committed here is published on push — scan before adding content taken
from a private project. Do not add a second pickup document; extending `AGENTS.md`
and this file is the whole point.

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
- Published public and pushed; the workflow ran green on the first attempt.

## Next action

Install the kit into one real project other than its source, and fix whatever
that reveals. A throwaway pull request here would also close the `--base` gap
below, and costs minutes.

Completion condition: a second project passes `python tools/check-handoff.py`
after an install that needed no hand-editing of the validator. Uncertain until
then: whether the default sections suit a software-only project, since they were
generalized from a hardware one.

## Open questions and parked work

- ⚠️ **The `--base` rule has never run on GitHub.** It passed locally both ways,
  but CI skipped it (`pull_request`-only). A throwaway PR would settle it.
- The CI workflow's whitespace step exits 0 by construction; now that it has run,
  decide whether it should be allowed to fail the build.
- No test suite for the validator itself. A handful of fixture repositories —
  one valid, several broken in specific ways — would be worth more than any
  further feature.
- Parked deliberately: no packaging, no installer beyond a script, no GitHub
  Action published to the marketplace.

## Evidence and session record

- [Published, and CI green](../JOURNAL.md#session-2026-09-08-push-and-ci).
- [First build](../JOURNAL.md#session-2026-09-08-build-the-kit).
- The pattern's origin is a private repository; the generalization here was
  written fresh rather than copied, and no private content is included.
