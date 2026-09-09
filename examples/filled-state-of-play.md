# Example — a filled-in handoff

What the template looks like once it is doing its job. This one is invented (a
small billing service) and is here to show the *register*: dated, scoped, and
willing to say what is not known.

Copy the tone, not the content.

---

# billing-svc — pickup

Updated: 2026-03-14
Evidence baseline: `a91c33d`; staging deploy `bill-2026.3.2`
Session status: Paused mid-migration. The dual-write is on; the backfill is not.

## Current objective

Move invoice storage from the legacy `invoices` table to `invoice_v2` without
downtime, using dual-write then backfill then cutover. **We are between step 1 and
step 2.**

## Recent observations

| Thing | Last state | Observation and limitation |
|---|---|---|
| Dual-write | `DEPLOYED` to staging `bill-2026.3.2`, 2026-03-14 | 4,102 invoices written to both tables over 6 hours with no divergence in the nightly compare. **Not deployed to production**, and the compare only covers rows created after the deploy. |
| Backfill job | `BUILT`, never run | Passes unit tests. It has never touched a real dataset, and its rate limiting is untested against production row counts. |
| Legacy read path | `VERIFIED` unchanged, 2026-03-14 | Still the only read path. Nothing reads `invoice_v2` yet. |
| Refund edge case | `UNKNOWN` | A partial refund issued *during* the dual-write window has not been exercised. Suspected gap, not a proven defect. |

## Active work and constraints

- Dual-write is **on in staging** — do not redeploy staging without saying so in
  the channel; the compare job's baseline resets.
- ⚠️ **Do not run the backfill against production.** It has no resume, so a
  half-finished run has to be reasoned about by hand.
- The finance team is closing the month until 2026-03-18. **No production
  migration work until they are done**, at their request.

## Completed work

- Dual-write behind `FF_INVOICE_V2_WRITE`, default off in production.
- Nightly compare job reporting divergence count to the dashboard; six clean runs
  in staging. Clean runs cover *new* rows only — they say nothing about history.
- Rollback documented and rehearsed once in staging: flag off, no data deleted.

## Next action

Exercise the partial-refund case against staging with dual-write on, and record
what both tables contain afterwards.

Completion condition: a written comparison of the two rows for a partial refund,
with the discrepancy either explained or filed as a defect. Uncertain even then:
whether the same holds for chargebacks, which nobody has looked at.

## Open questions and parked work

- Backfill throughput against ~9M production rows is a guess; nobody has measured
  it. Estimate before scheduling, not during.
- Parked by the team lead: the read-path cutover design. Do not start it — it
  depends on the backfill numbers above.
- `invoice_v2` has no archival policy. Raised, not decided.

## Evidence and session record

- [Dual-write staging soak](../JOURNAL.md#session-2026-03-14-dual-write-soak).
- [Rollback rehearsal](../JOURNAL.md#session-2026-03-11-rollback-rehearsal).
- Local-only: `~/tmp/compare-2026-03-14.log` — 6 runs, 0 divergences, 4,102 rows.
  The summary here is the portable part; the log is not shared.
