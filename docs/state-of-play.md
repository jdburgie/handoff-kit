# handoff-kit — pickup

Updated: 2026-10-21
Evidence baseline: `173312b`, fetched from `origin/main`, plus uncommitted work on `feat/skill-package`
Session status: Packaged as an agent skill on `feat/skill-package`; not yet
committed, pushed, or run in CI. Rows dated 2026-09-08 are last recorded then.

## Current objective

Make the pickup / session-end pattern from a private hardware project reusable by
any repository, under any AI tool, and keep it honest with a validator that runs
without dependencies. The kit follows its own contract — this file and
[the journal](../JOURNAL.md) are the demonstration.

## Recent observations

| Thing | Last state | Observation and limitation |
|---|---|---|
| `skills/handoff-kit/` | `BUILT` 2026-10-21, Windows/Python 3.13 | `tests/test_kit.py` passes all 10 tests from a standalone copy, and both plugin manifests validate. Not yet run in CI, installed as a plugin, or loaded by another agent. |
| `tools/check-handoff.py` (merged) | `BUILT` 2026-10-21 | Exits 0 here. Five local adopters pass unchanged. The three oaklink repos need a config for their sections and four journal-link fixes. |
| Second adoption: `esp32-sprinkler-controller` | `VERIFIED` 2026-09-08, commit `3d47c84` | Installed and passed the validator with **no edit to the script or the config**. The manual work was migrating an existing ad-hoc handoff and anchoring the existing journal. |
| `.github/workflows/handoff.yml` | `VERIFIED` on push ([34307145554](https://github.com/jdburgie/handoff-kit/actions/runs/34307145554)) **and on pull request, both directions** | The `--base` step failed a code-only commit ([34307890712](https://github.com/jdburgie/handoff-kit/actions/runs/34307890712)) and passed once the record was updated ([34308026068](https://github.com/jdburgie/handoff-kit/actions/runs/34308026068)). ⚠️ One repo, one-file change, same-repo PR — forked PRs untested. |

## Active work and constraints

Nothing running. The repository is **public** at `jdburgie/handoff-kit`, so
anything committed here is published on push — scan before adding content taken
from a private project. Do not add a second pickup document; extending `AGENTS.md`
and this file is the whole point.

## Completed work

- Packaged the kit as a self-contained agent skill with install, pickup, session
  end and upgrade modes. Added a Claude Code plugin manifest and a kit test
  suite, and merged the esp32-sprinkler-controller validator improvements.
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

With the user's approval, commit `feat/skill-package`, push it, open a PR, and
confirm that the `handoff` and `test` workflows pass. After merge, tag `v1.0.0`.
Listing on a marketplace is the user's own step.

Completion condition: both workflows are green on the PR, and the plugin
installs from `jdburgie/handoff-kit`.

## Open questions and parked work

- **Forked pull requests are untested.** `origin/<base_ref>` may not be fetched
  the same way for a PR from a fork; the rule has only been proven same-repo.
- Upgrade the eight adopter repos with `install.py --upgrade`, one at a time. The
  oaklink repos first need a `handoff.config.json` for their sections.
- The default sections are **still untested on a software-only project**, which
  is where "recent observations" may read oddly.
- 🧹 PR #1 (`test/base-rule`) is open scaffolding. Close it unmerged and delete
  the branch; the `install.py` comment on it must not reach `main`.
- The CI workflow's whitespace step exits 0 by construction; now that it has run,
  decide whether it should be allowed to fail the build.
- Parked deliberately: no GitHub Action published to the Actions marketplace.

## Evidence and session record

- [Packaged as an agent skill](../JOURNAL.md#session-2026-10-21-skill-package).

- [Completion guidance](../JOURNAL.md#session-2026-10-05-completion-guidance).

- [The --base rule proven](../JOURNAL.md#session-2026-09-08-base-rule-proven).
- [Second adoption](../JOURNAL.md#session-2026-09-08-second-adoption).
- [Published, and CI green](../JOURNAL.md#session-2026-09-08-push-and-ci).
- [First build](../JOURNAL.md#session-2026-09-08-build-the-kit).
- The pattern's origin is a private repository; the generalization here was
  written fresh rather than copied, and no private content is included.
