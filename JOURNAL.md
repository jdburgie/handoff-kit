# handoff-kit — Journal

Dated session records, newest first. Start with
[the handoff](docs/state-of-play.md) and [AGENTS.md](AGENTS.md); this file is
historical evidence, not a pickup document. Search it by date or topic rather than
reading it at startup.

New entries follow [the template](docs/session-template.md). Older entries are
preserved as written — a correction is a new entry linking to what it supersedes,
never an edit that erases it.

<!-- SESSION ENTRIES -->

<a id="session-2026-09-08-base-rule-proven"></a>
## 2026-09-08 The --base rule, proven on GitHub in both directions

### Objective and constraints
Close the gap the previous two entries flagged: the "require a session record"
step is `pull_request`-only and had never executed on GitHub, so the only evidence
for it was a local test. Throwaway branch `test/base-rule`, PR #1, not merged.

### Changes and decisions
Nothing in the kit changed. The branch carried a deliberate comment-only edit to
`install.py` so it touched the project without touching the record, then a second
commit adding a journal entry and a handoff link. The branch exists to be thrown
away; its own entry never reaches `main`, which is why this one is self-contained.

### Validation and evidence
**Both halves observed on GitHub, on the same PR, same workflow, same step:**

| Commit | Run | *Require a session record* |
|---|---|---|
| `d799e48` — code only | [34307890712](https://github.com/jdburgie/handoff-kit/actions/runs/34307890712) | 🔴 **failure** |
| `939873d` — code **and** record | [34308026068](https://github.com/jdburgie/handoff-kit/actions/runs/34308026068) | ✅ **success** |

- In the failing run, *Validate the handoff* passed first and the later steps were
  skipped: **the rule fired for the right reason**, not because the workflow was
  broken. In the passing run all nine steps succeeded, in ~4 seconds.
- `origin/${{ github.base_ref }}` resolves as the workflow assumed, with
  `fetch-depth: 0`. Three-dot diff against the PR merge commit behaves correctly.
- The same two outcomes were reproduced locally with
  `python tools/check-handoff.py --base main` before each push.
- ⚠️ Tested on **one** repository, with a one-file change, on a PR into `main`.
  Nothing is known about forked-PR runs, where `origin/<base>` may not be fetched
  the same way.

### State at the end
`main` unchanged apart from this record. PR #1 is open and **must not be merged** —
the `install.py` comment on that branch is scaffolding. The branch and PR are the
user's to close.

### Next action and completion condition
Install the kit into a software-only project. The sections were generalized from a
hardware project and have now been used by another firmware project; "Recent
observations" is the row most likely to read oddly where there is no device.

Completion condition: a software-only project passes the validator, and its
handoff reads naturally rather than being bent to fit the template.

### Do not repeat
Do not re-run this test — both directions are recorded above with run links. Do not
merge `test/base-rule`.

---

<a id="session-2026-09-08-second-adoption"></a>
## 2026-09-08 Second adoption, and what it exposed

### Objective and constraints
Install the kit into `esp32-sprinkler-controller` — the first project other than
this one — and fix whatever that revealed. That was the completion condition in
the previous entry.

### Changes and decisions
The install itself needed **no edit to the validator or the config**, which is the
condition met. Two frictions appeared, and both are now handled in the kit rather
than in that project's head:

- **An existing `JOURNAL.md` is skipped, and the user is left holding a validator
  that wants anchors.** `install.py` now prints exactly what to add — the
  `<!-- SESSION ENTRIES -->` marker and one anchored entry — and says older entries
  keep their shape. **Do not rewrite history to satisfy a check.**
- ⭐ **A long-running project usually already has a handoff, in the wrong place.**
  That one had a "Current pinned state" block at the top of its journal, plus a
  branch-specific `HANDOFF_*.md`. Installing beside it would have produced two
  pickup documents, which is worse than none. The README now says to find it,
  move its content, and mark the original superseded — which is what was done.

### Validation and evidence
- `python tools/check-handoff.py` in `esp32-sprinkler-controller`: **passes**,
  2026-09-08, commit `3d47c84`.
- The new installer output was re-run against the scratch project and prints the
  existing-journal guidance as intended.
- ⚠️ The kit's own CI has not run since these edits, and the `--base` step still
  has never executed on GitHub.

### State at the end
`main` with the installer and README changes plus this record. The second project
is committed and pushed on its own remote; nothing here depends on it.

### Next action and completion condition
Open a throwaway pull request here to exercise the `--base` step.

Completion condition: one PR run where it fails a code-only change, and one where
it passes after the record is updated.

### Do not repeat
Do not claim the sections are proven for software-only projects — the one adoption
so far is a firmware project with hardware, which is the same shape as the source.

---

<a id="session-2026-09-08-push-and-ci"></a>
## 2026-09-08 Published, and the workflow ran

### Objective and constraints
Push the kit to the public repository the user created, then check the result
rather than assume it. Continues [the first build](#session-2026-09-08-build-the-kit).

### Changes and decisions
No code changed. Remote added and `main` pushed at `8dbffd1`. Before pushing, the
tree was scanned for content from the private project it was generalized from —
project name, product names, domain, personal identifiers — because the repository
is public and a push is not reversible in any way that matters. Nothing was found.

### Validation and evidence
- Push: `main` tracking `origin/main`, `8dbffd1`, confirmed by `git status -sb`.
- CI: run [34307145554](https://github.com/jdburgie/handoff-kit/actions/runs/34307145554),
  event `push`, conclusion **success**, ~5 seconds on ubuntu-latest. Steps:
  checkout ✅, setup-python ✅, **validate the handoff ✅**, whitespace ✅,
  and *require a session record* **skipped**.
- ⭐ This is the first evidence the validator runs anywhere but Windows/Python
  3.12. Portability now rests on one Linux run rather than an assumption.
- ⚠️ **The `--base` rule was skipped, not exercised.** It is `pull_request`-only,
  and no pull request exists. It passed locally in both directions - failing a
  code-only commit, passing once the record was updated - and that remains the
  only evidence for it.
- Not tested: macOS, older Pythons, and any second project adopting the kit.

### State at the end
Public repository, `main` at `8dbffd1`, working tree clean apart from this record.
Nothing running, nothing parked.

### Next action and completion condition
Install into one real project other than this one and fix what that exposes; a
throwaway pull request would close the `--base` gap at the same time.

Completion condition: a second project passes the validator after an install that
needed no edits to the script.

### Do not repeat
Do not record the workflow as unrun - it has run, green, and the handoff says so.
Do not treat the skipped `--base` step as evidence that it works on GitHub; the
opposite is true, and the local test is what stands behind it.

---

<a id="session-2026-09-08-build-the-kit"></a>
## 2026-09-08 Build the kit

### Objective and constraints
Extract the pickup / session-end pattern from a private hardware project into a
repository that installs into any project and works under any AI tool. Model
agnostic was the explicit requirement, so the contract lives in `AGENTS.md` and
every tool file is a pointer to it.

### Changes and decisions
- **`AGENTS.md` is the single contract.** Pointer files for Claude, Gemini, Cursor
  and Copilot link to it; the validator fails an entry point that grows past a
  word limit, because a tool file that restates the rules becomes a second,
  drifting contract. That failure mode is the reason the check exists.
- **The evidence vocabulary is the substance**, not the templates: code, a passing
  test, and an observation of the running system establish three different things,
  and none substitutes for another. "Not observed" rather than "did not happen".
- **Sections were generalized** from the source project's hardware-specific set —
  "last observed bench state" became "recent observations", "active experiments"
  became "active work and constraints" — and every enforced value moved into
  `handoff.config.json` so a project can disagree without editing the script.
- **The installer never overwrites.** It reports what it skipped and expects a
  human merge; `--force` exists but is not the default path.
- **The seeded journal entry is real, not a placeholder.** A fresh install
  therefore satisfies the "handoff links the newest anchor" rule immediately
  instead of failing its own check on day one.
- Written fresh rather than copied: no private project content is included.

### Validation and evidence
- `python tools/check-handoff.py` in this repository: **passes**, 2026-09-08.
- Negative checks, same date: a wrong section order, a duplicate anchor, a future
  `Updated:` date, a broken relative link and an over-long entry point each
  produce the intended error.
- `python install.py <scratch> --tools all --ci` into an empty directory, then the
  validator inside it: **passes**. Re-running the installer skipped every file.
- ⚠️ **Not validated:** the GitHub Actions workflow has never run — no remote
  exists yet. Tested on Windows with Python 3.12 only; no macOS or Linux run, and
  no test suite for the validator itself.

### State at the end
Local repository only, on `main`, with no remote and nothing pushed. The user will
create the GitHub repository; the remote and push are the next mechanical step and
have not happened.

### Next action and completion condition
Push, then install into one real project and fix what that exposes.

Completion condition: a second project passes the validator after an install that
required no edits to the script.

### Do not repeat
Do not add a second pickup document, and do not copy the contract into tool files
— both are the failure this kit exists to prevent. Do not make the validator
assert truth; it checks structure, and pretending otherwise would make it worse
than useless.
