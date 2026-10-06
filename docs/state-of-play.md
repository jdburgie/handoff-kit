# handoff-kit — pickup

Updated: 2026-10-05
Evidence baseline: `3762154`, fetched from `origin/main`
Session status: Completion guidance added to the contract. Earlier operational
observations and parked work below remain last recorded on 2026-09-08.

## Current objective

Make the pickup / session-end pattern from a private hardware project reusable by
any repository, under any AI tool, and keep it honest with a validator that runs
without dependencies. The kit follows its own contract — this file and
[the journal](../JOURNAL.md) are the demonstration.

## Recent observations

| Thing | Last state | Observation and limitation |
|---|---|---|
| `tools/check-handoff.py` | `VERIFIED` 2026-09-08 on Windows/Python 3.12 **and** in CI on ubuntu-latest | Exits 0 on this repo, and eight negative cases each produce their intended error. Portability now rests on one Linux run, not an assumption. |
| `install.py` | `VERIFIED` 2026-09-08 into a scratch directory **and one real project** | Fills placeholders, skips existing files, and both installed trees pass the validator. Windows only. |
| Second adoption: `esp32-sprinkler-controller` | `VERIFIED` 2026-09-08, commit `3d47c84` | Installed and passed the validator with **no edit to the script or the config**. The manual work was migrating an existing ad-hoc handoff and anchoring the existing journal. |
| `.github/workflows/handoff.yml` | `VERIFIED` on push ([34307145554](https://github.com/jdburgie/handoff-kit/actions/runs/34307145554)) **and on pull request, both directions** | The `--base` step failed a code-only commit ([34307890712](https://github.com/jdburgie/handoff-kit/actions/runs/34307890712)) and passed once the record was updated ([34308026068](https://github.com/jdburgie/handoff-kit/actions/runs/34308026068)). ⚠️ One repo, one-file change, same-repo PR — forked PRs untested. |

## Active work and constraints

Nothing running. The repository is **public** at `jdburgie/handoff-kit`, so
anything committed here is published on push — scan before adding content taken
from a private project. Do not add a second pickup document; extending `AGENTS.md`
and this file is the whole point.

## Completed work

- Added proportional completion checks inspired by unlazy: observable outcomes,
  meaningful checks, applicable evidence, and final request reconciliation.

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
- Adopted by a second project, and the two frictions it exposed are fixed in
  `install.py` and the README: what to do with an existing `JOURNAL.md`, and to
  look for the ad-hoc handoff a long-running project already has before installing
  a second one beside it.

## Next action

Install the kit into a software-only project — no firmware, no devices — and see
whether "Recent observations" reads naturally there or has to be bent to fit.

Completion condition: a software-only project passes the validator with a handoff
that reads like a real one. Uncertain until then: whether the section set needs a
software-only variant in the config.

## Open questions and parked work

- **Forked pull requests are untested.** `origin/<base_ref>` may not be fetched
  the same way for a PR from a fork; the rule has only been proven same-repo.
- The default sections survived one software+hardware project unchanged. **Still
  untested on a software-only project**, which is where "recent observations" may
  read oddly.
- 🧹 PR #1 (`test/base-rule`) is open scaffolding. Close it unmerged and delete
  the branch; the `install.py` comment on it must not reach `main`.
- The CI workflow's whitespace step exits 0 by construction; now that it has run,
  decide whether it should be allowed to fail the build.
- No test suite for the validator itself. A handful of fixture repositories —
  one valid, several broken in specific ways — would be worth more than any
  further feature.
- Parked deliberately: no packaging, no installer beyond a script, no GitHub
  Action published to the marketplace.

## Evidence and session record

- [Completion guidance](../JOURNAL.md#session-2026-10-05-completion-guidance).

- [The --base rule proven](../JOURNAL.md#session-2026-09-08-base-rule-proven).
- [Second adoption](../JOURNAL.md#session-2026-09-08-second-adoption).
- [Published, and CI green](../JOURNAL.md#session-2026-09-08-push-and-ci).
- [First build](../JOURNAL.md#session-2026-09-08-build-the-kit).
- The pattern's origin is a private repository; the generalization here was
  written fresh rather than copied, and no private content is included.
