# Session record template

Follow [AGENTS.md](../AGENTS.md). Copy the block below immediately after
`<!-- SESSION ENTRIES -->` in [JOURNAL.md](../JOURNAL.md), newest first, and
replace every placeholder.

**Anchors must be unique and stable.** Use `session-YYYY-MM-DD-short-purpose`;
give a second session on the same day a different suffix. The handoff links the
newest anchor, and the validator checks that it does.

**Never invent an entry to fill a field.** "None", "not run", "unchanged since
_date_", and "unknown" are all valid answers, and each is worth more than a
confident sentence with nothing behind it.

```markdown
<a id="session-YYYY-MM-DD-short-purpose"></a>
## YYYY-MM-DD Short purpose

### Objective and constraints
What the user asked for, the scope, and anything parked or protected during it.

### Changes and decisions
What changed and why, with paths or commits, and any deliberate behaviour a later
session must not "fix". If this supersedes an earlier conclusion, link that entry
and say what new evidence changed it.

### Validation and evidence
Commands or scenarios, their results, the date, and the build or instance they ran
against. Keep **built**, **deployed** and **verified** separate. Link portable
evidence; for local-only evidence, name the path and summarize the result.
State plainly what was **not** checked.

### State at the end
What was touched and what state it is in. Name active experiments or say none.
Record unrelated work left alone, and any commit or push that is blocked —
without claiming a push that has not happened.

### Next action and completion condition
One concrete action, its prerequisites, how success is recognized, and what stays
uncertain. Say when user input is genuinely required; a task list is not
permission to act.

### Do not repeat
Finished work, rejected approaches, and dead ends — with the reason or the
evidence link, so the next session does not pay for the lesson twice.
```

## The state-of-play file uses these sections, in this order

`Current objective` · `Recent observations` · `Active work and constraints` ·
`Completed work` · `Next action` · `Open questions and parked work` ·
`Evidence and session record`

It also carries `Updated:` (ISO date), `Evidence baseline:` (the commit actually
inspected — not the commit being written), `Session status:`, and an explicit
`Completion condition:` under the next action. Change the set in
`handoff.config.json` if this project needs different ones; change it in both
places or the validator will fail.
