# M3 Forward Paper — Setup Notes

**Swing Trading project · 2026-07-15 (CST) · Evan Daruwalla**

Not an experiment write-up (no D1 verdict here — this is infrastructure). Documents what
was built for PRD M3 (tasks 14–17), a design adaptation from the PRD's original spec, two
operational findings from the first dry run, and what remains blocked on Evan.

## Adaptation from the stale M3 spec (dated decision, 2026-07-15)

PRD tasks 14/18 (written 2026-07-08, M0 era) describe two sleeves: `e1_control` (mechanical
IBS) + `e1_llm_veto` (LLM cash-veto treatment). **E1 FAILED and was shelved in M2b
(2026-07-09)** — those sleeves no longer correspond to anything worth forward-testing. The
actual forward-paper candidates, per every HANDOFF entry since, are the three D1
tier-clearing (or in-sample-clearing) survivors:

- **`e6_1x`** — QQQ 1×, invested iff QQQ > 200-DMA (E6, prereg `0526ea2`). Simplest sleeve:
  one instrument, a handful of switches per year.
- **`e18_vixts`** — QQQ 1×, invested iff VIX/VIX3M < 1 (E18 arm (a), prereg `f32b008`). The
  program's first (weak) PASS-RA.
- **`m10_1_nagel`** — weekly VIX-gated switch: VIX>20 → bottom-K=4 FF3-residual reversal
  basket on the 39-survivor universe; VIX≤20 → E6 trend (prereg `prereg_m10_1_nagel_switch.md`).
  The program's first PASS-HR, IN-SAMPLE-COMPOSED — **this is the one M3 exists to actually
  validate** (HANDOFF: "the one thing that makes it real = M3 forward paper").

This supersedes tasks 14/18's `e1_control`/`e1_llm_veto` naming. The LLM-overlay design
(PRD M9 task 51) is untouched and still a separate, later, forward-only treatment arm — not
built in this pass.

## What was built

- **`swing_bot/paper_sleeves.py`** — schema (`paper_sleeves`, `paper_positions`,
  `paper_transactions`, `paper_nav`, `fill_divergence` — new tables in `swing.db`, does not
  touch the pinned `bars` rows or anything `test_frozen.py` reads) + `decide_e6_1x` /
  `decide_e18_vixts` / `decide_m10_1`, each reusing the **identical signal condition** as its
  backtest runner (same SMA window, same VIX threshold, same `residual_series` FF3 machinery
  — load-bearing for M3's "implementation fidelity vs shadow backtest" success criterion).
- **`swing_bot/alpaca_client.py`** — ported (not imported) from
  `D:\ClaudeCode\Trading\trading_bot\execution\alpaca_client.py` (read-only reference, per
  the established port-not-import rule). ~180-line httpx wrapper, PAPER base URL by default,
  refuses to submit against a live base URL unless the caller explicitly passes
  `allow_live=True` (nothing in this project's scripts does). Reads credentials from
  `alpaca_keys.env`, falling back to OS environment variables.
- **`alpaca_keys.env`** (project root, gitignored — confirmed via `git check-ignore -v`
  against the existing `*_keys.env` pattern) — the keys spot.
- **`scripts/daily_swing_paper.py`** — the daily loop. Run once, any time after that day's
  close: realizes any pending order from the prior run (signal decided at the prior close,
  filled at today's now-known open), then computes today's new signal per sleeve and stores
  it as pending for tomorrow. Records NAV for all three sleeves every run — this DB-simulated
  ledger **is** the forward-paper evidence, independent of Alpaca. Dry-run by default;
  `--execute` mirrors every sleeve to its own account (see the update below).

## UPDATE 2026-07-15 (later, record Appendix CQ) — 3-account model, keys in, verified

Evan created **3 separate Alpaca paper accounts, $1,000 each — one per sleeve** (better than
the original single-mirror plan: fully isolated order flow). `alpaca_keys.env` now holds a
per-sleeve key pair each (`E_SIX_KEY/SECRET` → e6_1x, `E_EIGHTEEN_VIX_TS_KEY/SECRET` →
e18_vixts, `M_TEN_ONE_KEY/SECRET` → m10_1_nagel) plus a shared `APCA_API_BASE_URL`. The old
`SWING_ALPACA_SLEEVE` single-mirror selector is **obsolete and ignored**.

Code rewired: `swing_bot/alpaca_client.py` gained `client_for_sleeve(name)` (builds a client
from that sleeve's own pair), base-URL normalization, and `close_position`/`cancel_all_orders`;
`daily_swing_paper.py --execute` now mirrors **all three** sleeves, each to its own account,
via a flatten-then-enter reconcile. **Two real issues in the new format were caught and fixed
in code (not by touching the keys):** (1) the base URL ends in `/v2` → paths would double to
`/v2/v2/...` → normalized away; (2) Alpaca rejects notional+limit orders → buys are now
market-notional DAY (still next-open, DAY-TIF).

**VERIFIED (read-only, no orders):** `.venv\Scripts\python.exe -m swing_bot.alpaca_client` →
**all 3 accounts 200 OK / ACTIVE / $1,000 cash**, distinct account numbers. The keys work and
the isolation is real. No orders were placed (markets closed; "set up + keys" ≠ "start
trading"; the first `--execute` cycle should be run deliberately with Evan's go).

## Design: one evening run is sufficient

Signal at close → execute next open (the project's EOD hard rule) needs no second
"morning" touch: run once daily, after that day's close posts. By then the script already
has today's full bar (including today's open), so it can (1) realize yesterday's pending
using today's now-known open, then (2) compute today's close signal as tomorrow's pending —
a rolling one-day lag that exactly mirrors every backtest runner's own `pend`-then-fill
mechanism. This also means scheduling later (PRD task 19) only needs one nightly job, not two.

## Bug found and fixed by the first dry run

Running the script twice on the same still-latest session (no new trading day had posted
yet) **filled the pending order against its own signal day's open** — one day too early, and
non-idempotent on re-runs. Fixed: `realize_pending` now requires `today >
pending_signal_date` (strictly later session) before filling. Verified: two consecutive
same-day runs now correctly show `filled-today: False` both times, target unchanged. The
paper_* tables were reset to a clean slate afterward — the test fills from the buggy run
were deleted before any real use (my own dry-run artifacts, not real evidence).

## Two operational findings from the dry run (disclosed, not bugs)

- **Yahoo's same-day bar can be incomplete for several hours after close.** `swing_bot.
  prices.fetch` already (correctly, pre-existing behavior) drops any row with a NaN
  O/H/L/C — so a run late at night can see the just-closed session's Close still unposted
  and correctly fall back to the prior complete session. **Operational implication: schedule
  the real nightly run late evening (e.g. after ~8–9pm ET)**, not immediately at/after 4pm
  ET, to avoid systematically lagging a day.
- **`^VIX3M`'s feed lags `^VIX`'s by at least one session** (confirmed directly against
  yfinance: VIX3M had no row at all for the most recent session while VIX did). When this
  happens, `decide_e18_vixts` correctly returns `None` with a stated reason and the sleeve
  holds its current position — safe, inertial degradation, never a guessed trade.

## What's still blocked on Evan

**STATUS 2026-07-15 (later): items 1–3 below are now DONE** — Evan created 3 dedicated paper
accounts ($1,000 each), pasted the keys, and the smoke test confirmed all 3 connect (200 OK /
ACTIVE). What remains: **(A)** authorize the first real `--execute` run (or schedule it) — no
paper orders have been placed yet; **(B)** the after-hours order-queuing behavior (item 4)
stays unverified until that first live cycle; **(C)** Task Scheduler entry (still not created).
The original blocking list is preserved below for the record.

1. **Create or choose an Alpaca paper account** and generate an API key/secret (dashboard →
   API Keys). Given Swing Trading is deliberately separate from the Trading project
   (CLAUDE.md), a **dedicated new paper account** is recommended over reusing one of
   Trading's ~3 existing accounts, so order flow never mixes. Paste the key/secret into
   `alpaca_keys.env` at the project root.
2. **Choose which sleeve mirrors live** via `SWING_ALPACA_SLEEVE` in that file (or leave
   blank to run all three DB-only, no live orders — a legitimate choice; the DB ledger alone
   is real forward-paper evidence). **Recommendation:** start with `e6_1x` — simplest,
   single-instrument, lowest risk of a plumbing bug corrupting the evidence trail — verify a
   few clean fill cycles, then switch to `m10_1_nagel` (the sleeve M3 actually exists to
   test) once the mechanism is proven end-to-end. This is a recommendation, not a decision
   made on Evan's behalf.
3. **Smoke-test connectivity** once keys are pasted in:
   `.venv\Scripts\python.exe -m swing_bot.alpaca_client` — prints account status or a clear
   403/config error. Not run by Claude (needs real keys Claude never sees).
4. **Confirm the after-hours order-queuing assumption.** `--execute` submits a marketable
   DAY-TIF limit order the evening before the intended fill session (per PRD CONSTRAINTS:
   "no GTC — use a marketable DAY limit"). Whether Alpaca's paper API queues an after-hours
   DAY order for the next session open (vs. rejecting it) is **disclosed as unverified** —
   the first live cycle's `fill_divergence` row (DB-sim price vs. actual Alpaca fill) will
   show whether this assumption holds.

## Explicitly NOT done in this pass

- **Scheduling (PRD task 19).** No Windows Task Scheduler entry was created — an unattended
  process that submits real (paper, but real) order flow to a live brokerage API needs Evan
  to explicitly set up and confirm wants it unattended, not something to auto-schedule.
  `scripts/daily_swing_paper.py` prints this reminder every run.
- **20-day stabilization (task 20).** Can't be "set up" — it's a multi-week observation
  period that starts once real runs begin.
- **LLM overlay (M9 task 51).** Separate, later, forward-only treatment arm; untouched.

## Reproduction

`.venv\Scripts\python.exe scripts\daily_swing_paper.py` (dry-run; safe to run repeatedly).
`.venv\Scripts\python.exe -m swing_bot.alpaca_client` (connectivity smoke test, once keys
are in `alpaca_keys.env`). Frozen tripwire GREEN (12 refs d=0) — new tables only, no pinned
data touched.
