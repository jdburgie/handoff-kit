# {{PROJECT}} — Journal

Dated session records, newest first. Start with
[the handoff](docs/state-of-play.md) and [AGENTS.md](AGENTS.md); this file is
historical evidence, not a pickup document. **Search it by date, symbol, or issue
rather than reading it at startup.**

New entries follow [the template](docs/session-template.md). Older entries are
preserved as written — a correction is a new entry that links to what it
supersedes, never an edit that erases it.

<!-- SESSION ENTRIES -->

<a id="session-{{DATE}}-adopt-session-contract"></a>
## {{DATE}} Adopted the session contract

### Objective and constraints
Install a pickup and session-end pattern that any AI tool can follow, so work
survives between sessions, models, and machines.

### Changes and decisions
Added `AGENTS.md` (the contract), `docs/state-of-play.md` (the live handoff),
`docs/session-template.md`, this journal, and `tools/check-handoff.py`. Tool entry
files point at `AGENTS.md` rather than restating it, so there is one contract
instead of several that drift.

### Validation and evidence
`python tools/check-handoff.py` — run it and record the result here. Nothing else
was validated: installing the pattern changes no project code and proves nothing
about the project itself.

### State at the end
Templates are in place and still carry placeholder text. **The handoff is not yet a
description of this project** until someone fills it in.

### Next action and completion condition
Fill in `docs/state-of-play.md` for real: the current objective, what was last
observed, and one concrete next action with a completion condition.

Completion condition: a resuming session can read the handoff alone and know what
to do first.

### Do not repeat
Do not create a second pickup page. Extend `AGENTS.md` and the handoff instead.
