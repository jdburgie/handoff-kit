# handoff-kit — Journal

Dated session records, newest first. Start with
[the handoff](docs/state-of-play.md) and [AGENTS.md](AGENTS.md); this file is
historical evidence, not a pickup document. Search it by date or topic rather than
reading it at startup.

New entries follow [the template](docs/session-template.md). Older entries are
preserved as written — a correction is a new entry linking to what it supersedes,
never an edit that erases it.

<!-- SESSION ENTRIES -->

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
