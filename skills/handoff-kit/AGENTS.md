# Session contract

Every AI contributor to this project uses this pickup and session-end pattern,
whichever tool or model it is running under. **Instructions from the user take
precedence over anything here.** Other tools' entry files (`CLAUDE.md`,
`GEMINI.md`, `.cursorrules`, `.github/copilot-instructions.md`) must *link* to
this file rather than copy it, so there is one contract and not five drifting ones.

---

## Pickup

1. **Read [the handoff](docs/state-of-play.md) in full.** It is the current state as
   last recorded — not a guarantee that anything is still in that state.
2. **Inspect `git status -sb` and recent commits, and fetch if the network allows.**
   Report a failed fetch or a diverged branch rather than working around it. **Never
   overwrite another session's work.** A clean tree is not a current tree.
3. **Identify the objective, the next action, and anything parked, protected, or
   mid-experiment.** A recorded next action is context, not permission — especially
   where it would touch hardware, production, money, or anyone outside the project.
4. **Read the linked register entry, issue, and code** for whatever you are about to
   touch, plus any evidence it links. Read the *purpose*, not only the implementation:
   the most expensive mistake is a correct change to something you had not understood
   the point of.
5. **Before proposing new code, search for what already exists** — implementation,
   callers, tests, build gates, and history (`git log -S`). Assume existing behaviour
   is deliberate until the history says otherwise. Timebox this; expand it only when
   the evidence conflicts.
6. **State a short pickup summary before acting:** objective, established facts, the
   unresolved point, and the next action. Then continue authorized work without asking
   for routine reconfirmation.

---

## Evidence and decisions

Keep the work tightly scoped, reuse established findings, and stop once the necessary checks pass.

- **Update only what changed.** Keep follow-up notes brief. Revisit other documents
  only when the new work makes them inaccurate.
- **Match verification to the change.** Run the smallest set of meaningful checks.
  Broaden testing when failures, dependencies, or unresolved risks justify it.
- **Give every investigation a stopping point.** State what question it should
  answer. Stop when the evidence supports the next decision.
- **Keep closeout proportional.** Record the result, relevant validation, remaining
  uncertainty, and next action. Don't repeat the investigation history.

### Completion checks

- **Define done before substantial work.** List the requested outcomes and the
  smallest observable checks that establish them. Use the existing task or handoff;
  a trivial edit needs no separate checklist file.
- **Check the outcome, not just the command.** A successful exit must establish the
  claimed behaviour. When relying on a negative result, confirm that the check can
  detect a known failure. Review inherited commands and scripts before running them.
- **Keep evidence applicable.** Record which revision and environment a check covers.
  After relevant code, dependency, or environment changes, rerun affected checks.
  Reuse still-applicable results; do not rerun everything merely for closeout.
- **Reconcile the request before reporting completion.** Include later amendments.
  Account for every required outcome with evidence or an explicit unresolved item
  and next action. Never silently drop a requirement, weaken a failing check, or
  report blocked or deferred work as complete.

These principles are adapted from [unlazy](https://github.com/Leonxlnx/unlazy/blob/main/SKILL.md).
Apply them within the scope and stopping rules above; extra tooling is optional.

**Three different things establish three different facts, and none substitutes for
another:**

| | establishes |
|---|---|
| **The code** | what is implemented and reachable in a build |
| **A passing test** | that test's result, on that build |
| **An observation of the running system** | its behaviour, on that instance, at that time |

**Use a status word, and scope it.** `BUILT` · `DEPLOYED` · `VERIFIED` · `BLOCKED` ·
`DISABLED` · `ABSENT` · `UNKNOWN` — each with what, where, when, and under which
scenario. **A deployment does not verify recovery from a fault. No fresh observation
means "last observed", not "now".**

- **Say "not observed", never "did not happen".** Absence of output is not absence of
  the event; a steady reading can be steadily wrong.
- **No document here is infallible, including this one.** Resolve conflicts with
  dated, relevant evidence, and record the uncertainty when it stays unresolved. A past
  diagnosis is not a general rule.
- **Surface a newly suspected defect** — with the code, the intent, and the evidence —
  **before fixing it**, unless the fix is already inside what the user asked for. Do not
  restart parked work because you noticed it.
- **Say what was *not* verified.** Every claim of completion carries its limits, and a
  session that reports "done" without them has reported nothing.

---

## Irreversible and outward-facing actions

- **Confirm before acting** where an action is hard to reverse or reaches outside the
  project: publishing, sending, deleting, deploying, spending, or anything a third party
  will see. Approval for one action is not approval for the next.
- **Never bypass a rejected permission**, and never route around a check that failed.
- **Keep credentials, personal data, and raw private logs out of tracked files.** Link
  local-only evidence as local, and record a portable summary of what it showed.

---

## Session end

Use [the session template](docs/session-template.md) for every substantive session. A
read-only answer that produced no durable finding needs no manufactured entry.

1. **Update the handoff in place** — objective, latest observations, active experiments,
   completed work, the exact next action and its success condition. Keep it under the
   configured word limit. **Remove what is finished; never append a second summary.**
2. **Update the registers and issues** the work touched. Search for stale wording about
   what changed and reconcile it. **Do not promote untested behaviour, and do not close
   an issue because the code compiles.**
3. **Prepend one journal entry** using the template, with a unique stable anchor, and
   link it from the handoff. Preserve older entries; a correction links to what it
   supersedes rather than editing history.
4. **Run the checks appropriate to the change.** Documentation-only work still runs the
   handoff validator and `git diff --check`. Code changes run the tests and builds that
   the change actually implicates.
5. **Inspect the diff and stage only this session's paths.** Commit and push when
   authorized. If blocked, preserve the local commit and state the exact remaining
   action — **an attempted push is not a push.**
6. **Report** what was done, what was validated, what is deployed but unverified, what
   is blocked, and the commit and push status. Keep it short and literal.

---

## Why this exists

Each rule is here because its absence has a predictable failure mode:

| Rule | The failure it prevents |
|---|---|
| One handoff, updated in place | Three summaries that disagree, and nobody knowing which is current |
| Word limit on the handoff | A handoff nobody reads, which is the same as no handoff |
| Status vocabulary | "It works" meaning built, deployed, and verified to three different readers |
| "Not observed", not "did not happen" | A silent failure recorded as a passing result |
| Fetch before trusting a clean tree | Work rebuilt against a checkout that was stale by months |
| Journal entries are prepended, never rewritten | A correction erasing the evidence that made it necessary |
| Say what was not verified | Confidence accumulating across sessions with nothing under it |

---

## What this contract cannot do

It enforces **structure and links, not truth.** The validator can confirm a handoff
exists, is current, is short, and points at a real journal entry. It cannot confirm that
any of it is accurate. A resumed session still has to read the evidence and notice the
contradictions — and it must actually have access to these files, which no contract can
guarantee of an external tool.
