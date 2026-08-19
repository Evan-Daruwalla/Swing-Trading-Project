# Handoff

## Goal

**(Redefined by Evan 2026-07-09, record Appendix R.)** Build a swing trader
that, as accurately as possible, invests in a stock or a few stocks
(concentrated, K=1–3) with a small amount of money ($100–1,000) to earn a
**high percent return over a shorter amount of time** (holds days to a few
weeks). **Losing money is OK and will happen — risk explicitly accepted.**
Gates are return-centric with loosened (never absent) drawdown ceilings; the
pre-registration/OOS rigor machinery stays as the ACCURACY instrument.
SEPARATE project from `D:\ClaudeCode\Trading` (read-only from here). Paper
first; nothing goes live without a pre-registered PASS + Evan's go.

## Current state — SEARCH PHASE CLOSED 2026-08-03 at 37 attempts; FORWARD-EVIDENCE PHASE (M3) is the only open lever

> **37 vs 38 — both numbers are right, disambiguated 2026-08-06 (audit #3).** The
> SEARCH phase closed at **37** pre-registered attempts. The record's running
> tally reads **38** because M12 (record DU) came *after* the close and is a
> DIAGNOSTIC, not a search attempt. `docs/trial_log.json` flags the gap as
> UNRESOLVED and refuses to pick one; DSR deflates by the larger figure (50
> declared variants), so nothing downstream depends on resolving it. Use 37 for
> "how big was the search", 38 for "how many pre-registered runs exist".

> **2026-08-03 — SEARCH PHASE DECLARED CLOSED (Evan's dated decision; record DQ).** Not an
> abandonment and not a claim of success: the backtest search space under this project's
> constraints — **free EOD data · holds of days-to-weeks · K=1–3 · retail costs · $100–1,000**
> — is **exhausted** at 37 pre-registered attempts. E/C/X fixed-strategy space went first, M10
> closed the synthesis arc, M11 killed the last free *shape* mechanism, and **X7/X8/X9 closed
> the last structurally different families** (credit regime · non-equity trend · market-neutral
> relative value). Everything still untested is **1–12 month horizon** (outside the swing scope)
> or **data-gated** (paid borrow data, intraday feed, $22 FMP, total-return prices).
> **Terminal finding of the search phase: decorrelation is not the scarce resource — EDGE is.**
> **What is open:** exactly one lever — **M3 forward paper**, live since 2026-07-15 on 3
> isolated Alpaca paper accounts. It needs *elapsed time*, not another attempt. Its harness is
> instrumented (sim-vs-broker fidelity +0.0/+0.0/+1.3 bps when the EOD discipline holds) and
> self-correcting on share drift. **Disclosed:** the 3 sleeves are ~ONE strategy — a documented
> consequence of the evidence, since nothing uncorrelated *and* profitable was found to deploy.
> **Next research direction (Evan, 2026-08-03): RELAX A CONSTRAINT** rather than hunt a 38th
> rule inside the same box. (This line used to point at "the options block below", which does
> not exist in this file — audit #4 F10. The relaxation plan lives in
> `docs/M12_constraint_relaxation_plan.md`; M12's factorial answered it: HORIZON binds,
> breadth does not — record DU.)

> **2026-08-03 — X9 pairs / relative-value = FAIL; attempt #37 (record DP; results
> `docs/research/2026-08-03_X9_pairs_results.md`).** Evan chose "test a different rule family"
> after X8. Family picked from the project's OWN July-12 survey after removing everything since
> tested (C1/C3/C6/X1/X3): what remains is mostly 1–12 month horizons (outside the days-to-weeks
> scope) or data-gated — **pairs was the one structurally different family left, and the only
> MARKET-NEUTRAL one.** Prereg `00c8c44` (doc-only, predates the runner). **H0 was pre-declared
> as the FAVORED prior** (Do & Faff 2010: Gatev's edge decayed to ~nil post-2002) so a FAIL
> could not be dressed up as a surprise. H0 won.
> Gatev's distance method at his PUBLISHED defaults adopted wholesale (252/63/K=3/2σ/20-stop),
> 29 ETFs (leveraged excluded), 6,927 sessions, **5 bps per side PER LEG = ~20 bps a round trip.**
> **Net: GATE −2.50%/DD 41.3%/Sh −0.47 · SEC −6.71%/DD 60.2%/Sh −1.40**, final NAV **$294.16**
> from $1,000. corr to e6 **−0.0571**. FAILS ①②③, passes only ④.
> **Zero-cost DIAGNOSTIC (post-hoc, not gated) splits the failure in two:** gross GATE
> +2.07%/Sh **0.43**, gross SEC −0.35%/Sh **−0.05** — **the edge had already decayed to nothing
> before costs** (Do & Faff reproduced independently on this project's data), **and then ~81
> round trips/yr × ~20 bps ≈ 16%/yr of drag destroys what remains.** But **87.4% of trades
> CONVERGED** — the mechanism works; the reversion is simply smaller than four legs of cost.
> **PROGRAM-LEVEL FINDING: decorrelation is NOT the scarce resource, EDGE is.** Three straight
> decorrelation attempts cleared the correlation bar and failed profitability: **X8a GLD +0.089
> · X8b TLT −0.191 · X9 pairs −0.057** (bar ≤0.30). The 3 live sleeves remain ~one strategy as a
> DOCUMENTED CONSEQUENCE of the evidence, not an oversight. X9 closes the last
> structurally-different in-scope family.

> **2026-08-02 — X8 non-equity trend sleeve = FAIL both arms; decorrelation attempt deployed
> NOTHING (record DO; results `docs/research/2026-08-02_X8_noneq_trend_results.md`).** Evan:
> "make the sleeves less correlated." **Measured first (record DN): the 3 live sleeves are
> ~ONE strategy** — m10 runs the IDENTICAL e6 rule on **69.7%** of 4,226 sessions, e6/e18 agree
> **84.0%**, all three effectively long **65.3%**, live correlation **+0.86…+0.95** with 7–9 of
> 11 days byte-identical. Root cause is not sloppiness: 35 attempts yielded ONE survivor
> (200-DMA trend gating), market-dependent across equity regions (E7) and failed on crypto (X6)
> — **there was no validated uncorrelated candidate to deploy.**
> Attempt #36 tested the gap: the universe is 100% equity, so the surviving rule had never met a
> NON-EQUITY asset. Prereg `8b408f9` (doc-only, predates the runner), E6's rule verbatim, arms
> GLD + TLT, on an explicitly-labelled **DIVERSIFIER bar** (corr ≤0.30, CAGR>0 both, DD ≤60%
> both, Sharpe > the asset's own buy-hold both) — declared before results precisely so it could
> not look retrofitted.
> **GLD: corr +0.0886, CAGR +11.81%/+6.26%, DD 24.5%/28.4% — 3 of 4, FAILS ④** (Sharpe 0.73 beat
> buy-hold 0.65 in GATE, 0.52 LOST to 0.65 in SEC). **TLT: corr −0.1905 but negative CAGR both
> windows** — and dividend-UNADJUSTED prices materially understate TLT (declared bias, restated).
> **The finding: decorrelation was never the hard part** (+0.09 and −0.19 vs a 0.30 ceiling).
> Finding an uncorrelated asset is easy; finding one where this rule adds value is not. **Sixth
> repetition of the one-window death** (E6-downgrade, C7, X6, X7, M10-2, X8a) — now across US
> equity, non-US equity, crypto, credit and gold. **The bar was NOT lowered for GLD's near-miss,
> and the three running sleeves were NOT modified** (their preregs and 12 sessions of forward
> evidence stay intact). **Decorrelation goal NOT satisfied — stated plainly, not papered over.**
> New gap logged: no total-return (dividend-adjusted) data path, so coupon/dividend-heavy
> instruments cannot be tested fairly.

**Last updated: 2026-08-18 ~23:52 CDT** — this file is the only live snapshot;
history lives in the record. **Timezone: record/doc stamps are Central,
DST-AWARE — read the offset from `date` and label by the number: UTC-6 → CST
(winter), UTC-5 → CDT (summer). Currently UTC-5 = CDT. The cadence hook
reports UTC — subtract the current offset (record Appendix AZ; made DST-aware
2026-07-19; an earlier version of this line hardcoded "CST (UTC-5)", which is
self-contradictory and was corrected 2026-07-28 by audit #7).**

> **2026-07-28 — FULL AUDIT (`/audit`) + 5 fixes landed (records DH, DI; commits
> `1078693`, `6c9b161`, + this session).** System structurally sound; risk was concentrated
> in the LIVE harness, not the research. Clean: 12/12 scheduled runs succeeded, secret scan
> CLEAN across full git history, DB integrity/FK checks pass, 0 duplicate bars, NAV series
> complete, tripwire GREEN. **10 findings (1 crit / 2 high / 4 med / 3 low); 1,2,3,5,6
> FIXED, 4 documented-not-traded, 7 = this update, 8-10 open.**
> - **#1 (crit) `market_is_open()` FAILED OPEN** — returned None on any AlpacaError and the
>   caller then submitted orders ANYWAY, defeating the intraday guard exactly when the broker
>   is flaky (real Alpaca 500 on 2026-07-23). Now always returns a bool: Alpaca clock primary,
>   local ET regular-hours fallback that errs safe.
> - **#2 (high) `fill_divergence` was INERT** (0-for-10 rows had a real fill price) while the
>   docstring claimed gaps are "visible, never assumed" = false verification. Root cause was
>   structural: submit rows carry the order id but a decision-day CLOSE as their sim side,
>   realize rows carry the true sim fill but no order id — the two halves could never be
>   joined. Fixed with `get_order()`, 2 additive columns, and a `backfill_divergence()` pass
>   that polls the real fill and repairs sim_price from `paper_transactions`.
>   **FIRST REAL FIDELITY NUMBERS: +0.0, +0.0, +1.3 bps when the EOD discipline held;
>   −85.7 bps on the one run where it broke (07-20 midday fire).** M3's premise that the DB
>   ledger stands in for broker reality now has EVIDENCE, not an assumption.
> - **#3 (high) no staleness bound on VIX3M** → `VIX3M_MAX_STALE_SESSIONS=2`; e18 now REFUSES
>   to decide on a stale term structure (the exact 5-session lag that inverted it on 07-17
>   would now be blocked).
> - **#6 (med) transient broker errors unretried** — 3× HTTP 500 on 2026-07-23, all on
>   idempotent endpoints (`DELETE /v2/orders` ×2, `GET /v2/positions`). Retry added for
>   GET/DELETE only; **`POST /v2/orders` is never auto-retried** (a timed-out submit may have
>   landed → duplicate order; a missed order self-heals via reconcile, a duplicate does not).
> - **#4 (med) e18 carries a PERMANENT share fork** — record DE's "self-heals at Tue open" was
>   WRONG: it re-converged in STATE, never in QUANTITY. Now MEASURED: DB 1.3957099 vs Alpaca
>   1.4077634 = **+0.864% (+$8.14)**; e6/m10 drift is −0.001%/−0.014% (rounding). NOT traded
>   away: the DB ledger is the primary evidence and is next-open disciplined, so it is never
>   rewritten to match a broker fill, and placing bookkeeping orders is a trading-behavior
>   change = Evan's explicit call. Instead `report_mirror_drift()` now prints the gap every
>   run (flags ≥0.25%), so comparisons are made knowing the offset.
> - ~~Open: #8/#9/#10~~ **ALL CLOSED, verified 2026-08-11 (audit #4 F10):** #8
>   prices.fetch retries on a (2,5,15)s ladder; #9 `.gitattributes` pins `*.bat text
>   eol=crlf` and the file is CRLF on disk; #10 pip-audit is installed and reports
>   "No known vulnerabilities found". This block had claimed them Open for 8 days
>   after the code said otherwise.

> **M3 forward paper — RUNNING, 24 sessions (2026-07-15 → 2026-08-18), 72 NAV rows, ONE
> permanent hole (2026-07-30, record EI).** (This line has now been wrong three separate
> ways, so its history stays visible. It once said "13 sessions, 27 NAV rows, no gaps" —
> 13×3 is 39, not 27, and the 07-30 gap was real; corrected by audit #4 F10. Counts
> re-derived from `paper_nav` 2026-08-13, record EO. Then on 2026-08-16 records EV/EW
> changed it to "TWO holes (07-14 AND 07-30)" — **that correction was itself wrong and is
> REVERTED here (record EY, 2026-08-18).** The task's `<StartBoundary>` is
> 2026-07-15T19:00:00-05:00, so it did not exist on 07-14; the series begins 2026-07-15;
> and the log's session header carries the SESSION date, so the `=== 2026-07-13 ===` header
> is the pre-reset manual fire of records CS/CT, not evidence of a 07-14 miss. A date
> before the series began is not a hole in it — and record EI:6082 had already made exactly
> this correction under the heading "the forward-evidence series lost ONE session, not
> two".) Root cause of the 07-30 miss could not be determined — Windows Task Scheduler
> history logging is disabled (record EV.3; still `enabled: false` as of 2026-08-18). All
> three sleeves currently long QQQ. Latest marks (2026-08-18, written after that
> evening's 19:00 run): **e6_1x $1,007.74 · e18_vixts $1,001.44 · m10_1_nagel
> $1,021.72** — all three down ~1.7% on the 08-18 session (08-17 was $1,025.10 /
> $1,018.69 / $1,039.32)
> (each started at $1,000). Task now runs S4U — fires with nobody logged on. Scheduled task
> `SwingTradingDailyPaper` fires 7pm weekdays via `scripts/daily_swing_paper.bat --execute`;
> logs to `var/daily_swing_paper.log`. **Do NOT fire it manually intraday** — that is what
> caused the 07-20 round-trip and the e18 fork; the guard now blocks order submission while
> the market is open, but the DB ledger still advances on any run.

> **2026-07-15 — X7 HYG:IEF credit gate = FAIL, but the FIRST gate to beat the 200-DMA
> in-window (record Appendix CV; results `docs/research/2026-07-15_X7_credit_gate_results.md`).**
> Completeness kill from the BlackRock HY report. Prereg `f4a4d34` (doc-only, predates
> runner) → `run_x7_credit_gate.py`: long QQQ iff HYG:IEF ratio > its 200-DMA (credit
> appetite on), else cash — the free credit-spread proxy E18's HY-OAS arm couldn't test.
> **Gate (2007-13, GFC): 9.60% CAGR / DD 12.9% / Sh 0.98 — beats the plain 200-DMA overlay
> (0.61) and cuts QQQ-BH's 53.6% DD to 12.9%** (credit led 2008 → de-risked earlier; H1's
> mechanism is real in crisis, the sharpest gate result since E18). **But secondary (2014+)
> collapses: 3.81% / DD 47.6% / Sh 0.34** — worse DD than buy-hold, 221 whipsaw switches on
> credit noise that never became equity drawdowns. **A crisis specialist that self-destructs
> in bulls → FAIL both-windows.** Same one-window death as C7/X6/M10-2, inverted; the
> pre-registered bar killed a 0.98 gate Sharpe. Corroborates BlackRock's own Fig 2/3
> (defensive credit = downside-mitigation-not-alpha) → 3rd-domain confirmation (equities/
> crypto/credit). Attempt 35; MODIFIED-WINDOW PROMISING-capped anyway; not survivor-biased
> (clean FAIL). The plain 200-DMA remains the only robust overlay. Tripwire GREEN.

> **2026-07-15 — M3 rewired to 3-account model; all 3 Alpaca paper accounts VERIFIED
> CONNECTED (record Appendix CQ).** Evan made **3 separate Alpaca paper accounts, $1,000
> each (one per sleeve)** and pasted per-sleeve keys (E_SIX / E_EIGHTEEN_VIX_TS / M_TEN_ONE
> KEY+SECRET, shared paper base URL) into `alpaca_keys.env`. Rewired the code from the
> single-mirror model to mirror ALL 3 sleeves each to its own account
> (`client_for_sleeve()`; `--execute` now does a per-account flatten-then-enter). **Caught +
> fixed two real issues in the new format:** the base URL ends in `/v2` → would double to
> `/v2/v2/...` (fixed: normalize-strip `/v2`); Alpaca rejects notional+limit orders (fixed:
> buys are market-notional DAY, still next-open). **VERIFIED (read-only, no orders):**
> `python -m swing_bot.alpaca_client` → all 3 accounts **200 OK / ACTIVE / $1,000 each**,
> distinct account numbers. Keys work; isolation real. Dry-run intact; paper_* reset clean;
> `var/` added to .gitignore. **Did NOT place orders** — "set up + keys" ≠ "start trading
> tonight", markets closed, data mid-transition (07-14 bar incomplete). **Remaining gates
> (small):** authorize the first `--execute` run / scheduling (task 19, not created — real
> order flow needs Evan's explicit setup); after-hours DAY-order queuing unverified until the
> first live cycle. Account+keys gates from CP are DONE. Keys are PAPER, gitignored, never
> committed. Setup notes: `docs/research/2026-07-15_M3_forward_paper_setup.md`.
> **→ SCHEDULED (record Appendix CR):** committed+pushed (`503b606`); registered Windows
> task **"SwingTradingDailyPaper"** — `scripts/daily_swing_paper.bat` (pure ASCII) runs all
> 3 sleeves via `--execute` **weekday evenings 7pm local**, StartWhenAvailable. Verified
> Ready, NextRun tonight. **FIRST LIVE RUN = 2026-07-15 19:00 CDT** = the acceptance test for
> the (unexercised) order-mirror path; tonight only e6_1x acts (QQQ buy), e18 waits on VIX3M,
> m10 on Friday. **Review `var\daily_swing_paper.log` after 7pm.** The 20-day stabilization
> window (task 20) accrues from tonight.
> **→ FIRST LIVE RUN DONE (record Appendix CS):** Evan fired it early via
> `Start-ScheduledTask`. **e6_1x placed its first real order — BUY QQQ $1,000 market DAY →
> "accepted", buying_power→$0 (queued for next open)** on acct PA38ZZKY6WN0. This VERIFIES the
> previously-unverified after-hours DAY-order queuing — the full mirror pipeline works. (Ran
> at 2:43am off the last complete session 07-13 since 07-14/15 bars weren't posted yet; the
> 7pm cadence avoids that, and tonight's run is convergent — no double-buy.) **M3 is LIVE
> (paper).** Open refinement: fill_divergence doesn't yet re-query filled_avg_price for
> actual slippage (task-20 phase).
> **→ e18 UNDER-TRADE BUG FIXED + CLEAN RESTART (record Appendix CT):** Evan asked "only e6
> has an order, by design?" — e6 (QQQ>200DMA) and m10 (weekly, Fridays only → first acts Fri
> 07-17) were by design, but **e18 was skipping wrongly** — it required an exact-date VIX3M,
> which yfinance posts 1–3 sessions late, so it under-traded (should hold QQQ: VIX/VIX3M=0.92
> <1). Fixed: carry-forward the most-recent VIX/VIX3M ≤ today (past-only, no look-ahead; same
> pattern m10 uses; log shows as-of dates). **Canceled the e6 test order + reset all state to
> clean** ($1,000 cash × 3, DB empty) so tonight's 7pm run launches all sleeves **synchronized
> off complete 07-15 data** (e6 QQQ, e18 QQQ, m10 waits Fri) with DB and broker in lockstep.

> **2026-07-15 — M3 forward-paper infrastructure BUILT; BLOCKED-ON-EVAN for Alpaca keys
> (record Appendix CP).** Evan: "set up M3 forward paper and make a spot (file) to paste
> the keys into." **Adapted M3's stale task 14/18 spec** (`e1_control`/`e1_llm_veto` —
> E1 failed months ago, M2b) **to the 3 real forward-paper candidates:** `e6_1x` (E6),
> `e18_vixts` (E18 arm a), `m10_1_nagel` (M10-1 — the program's first PASS-HR, the one M3
> exists to actually validate). Built: `swing_bot/paper_sleeves.py` (sleeve DB schema +
> decide_* signal functions, each reusing the IDENTICAL condition as its backtest runner
> — implementation-fidelity); `swing_bot/alpaca_client.py` (ported, not imported, from
> Trading's client; paper-only, hard live-guard); **`alpaca_keys.env`** (project root,
> gitignored — confirmed via `git check-ignore -v` — **the spot to paste keys into**, with
> instructions + a SWING_ALPACA_SLEEVE selector); `scripts/daily_swing_paper.py` (one
> evening-run daily loop; dry-run default, `--execute` mirrors one sleeve to Alpaca).
> **Dry-run caught and fixed a real bug:** re-running same-day filled a pending order
> against its own signal day's open (non-idempotent) — fixed (`realize_pending` now
> requires a strictly later session), re-verified. Two operational findings disclosed
> (not bugs): Yahoo's same-session bar can be incomplete for hours after close (schedule
> the real job late evening); ^VIX3M lags ^VIX by ≥1 session (e18_vixts safely skips + logs
> when this happens, never guesses). Frozen tripwire GREEN. **BLOCKED-ON-EVAN:** create/
> choose an Alpaca PAPER account (recommend a NEW one, dedicated — not one of Trading's
> ~3), generate keys, paste into `alpaca_keys.env`, run
> `.venv\Scripts\python.exe -m swing_bot.alpaca_client` to smoke-test, choose
> SWING_ALPACA_SLEEVE (recommend starting with `e6_1x`, simplest, before upgrading to
> `m10_1_nagel`). Scheduling (Task Scheduler) and the 20-day stabilization window are
> explicitly NOT done — deliberately left for Evan once keys are verified. Setup notes:
> `docs/research/2026-07-15_M3_forward_paper_setup.md`.

> **2026-07-14 — M11 chart-pattern detection = FAIL (signal-dead); 9th family closed;
> survivor bias DESTROYS the pattern edge (record Appendices CL–CO).** Evan "1, then 3" →
> finalized + committed the M10 reframe + brief, then ran the chart-pattern kill-shot.
> Prereg `9cb5ac5` (doc-only, predates the runner) → `run_m11_chart_patterns.py`: causal
> close-based pivots (w=5, no look-ahead — LMW's two-sided kernel avoided), long reversal =
> **double-bottom + inverse-H&S**, fresh neckline break on close → next open, time-stop 20d,
> K=3, 39 survivors. **FAIL (attempt 34, the 9th equity family — first to trade *shape* not
> a *number*):** gate 2000–13 **−0.14% CAGR / 50.4% DD / Sh 0.09**, sec 1.67% / 0.19;
> **SIGNAL-DEAD** — frictionless Rung B ≈ 0 and A≈B (no overnight-gap story, unlike IBS);
> loses SPY (1.72%) AND survivorship-clean EW-39 (−0.47%). 314 gate entries; hold 10/40
> don't rescue (not tuned). **Payload:** the reported short-side diagnostic shows fwd-20
> after a bearish top/H&S completion is **+1.70%** (> unconditional +1.15%) — the OPPOSITE
> of Savin (2007) — because **survivorship removed exactly the decliners a bearish pattern
> predicts.** So the survivor universe doesn't merely flatter long dip-buying (E16/C1), it
> **structurally erases the one documented (bearish) pattern edge** — the cleanest asymmetric-
> falsification illustration yet. Every M11.1-brief prediction held. Tripwire GREEN.
> **Terminal claim upgraded: even the chart SHAPES retail traders are taught don't trade at
> retail EOD.** Free backtestable space exhausted again; the one untested *evidence* lever =
> **M3 forward paper** (Evan-gated). Writeup
> `docs/research/2026-07-14_M11_chart_patterns_results.md`.

> **2026-07-14 — FINALIZED THROUGH M10; research OPEN, not done; new direction = M11
> algorithmic chart patterns (record Appendix CL).** Evan: "finalize with M10 but DON'T
> call research done; full report on what didn't work and what might; the project is about
> trying everything (incl. biased-off-different-data)." Reframed the **capstone** from
> "COMPLETE / method space exhausted" → **"ONGOING"** (counts 31→33, M10 folded into the §3
> ledger, and a new **§8 "open frontier"** = the *what-might-work* half of the report:
> chart patterns + M3 forward paper + lower-priority untested levers). **New M11
> (chart-pattern detection — rule-based, NOT LLM)** added to the PRD as the **CURRENT OPEN
> DIRECTION, UNSTARTED**: the one classical mechanism family never tested here (it trades
> *shape*, not a number; price-only → full-window D1-reachable, unlike every post-2000
> experiment). **Honest prior = FAIL** (Lo-Mamaysky-Wang: patterns carry modest info but not
> cost-surviving profit; Sullivan-Timmermann-White / Bajgrowicz-Scaillet snoop-decay;
> McLean-Pontiff; and program-internally the breakout family already died 3× — E8/E11/C3)
> — but genuinely untested, so running it closes the last gap in "trying everything."
> **Docs-only turn:** capstone/PRD/record/HANDOFF/memory updated; tally UNCHANGED (33);
> nothing run; tripwire GREEN. **Next honest experiment = M11** (prereg the LMW
> head-and-shoulders / double-top kill-shot, then run — the reversal-side analogue of C3's
> breakout kill-shot) on Evan's go. M3 forward paper stays the one lever that could validate
> M10-1 (Evan-gated: Alpaca paper account).

> **2026-07-14 — M10 synthesis arc: Nagel Switch = the program's FIRST PASS-HR,
> but IN-SAMPLE-COMPOSED / forward-paper-only (record Appendices CG–CI).** Evan:
> compose the evidence into strategies vs both tiers. A multi-agent design panel
> proved fixed-weight PASS-HR is arithmetically empty (gate needs C1-weight ≥0.66,
> sec ≤0.29) → the only escape is state-conditioning on a causal variable. **M10-1
> Nagel Switch** (VIX>20 → C1 residual reversal, VIX≤20 → E6 trend; Nagel 2012
> mechanism; VIX 1990+ full window) **clears PASS-HR: gate 17.87% CAGR / DD 59.95%
> / Sh 0.66, sec 15.94% / 39.68% / 0.78** — both windows ≥15% CAGR & ≤60% DD.
> **NOT a win, by the program's own discipline:** IN-SAMPLE-COMPOSED (built after
> 31 results), survivor-flattered (reversal buys known survivors in crashes — C1's
> passes were declared UNINTERPRETABLE), gate DD passes by **0.05 pp**, fails at
> VIX>18 (14.83%), fails PASS-RA (Sh 0.66), 15 bps breaks it. Per the M10 cap it's
> **"PROMISING / forward paper REQUIRED,"** not clean/deployable. Tripwire GREEN;
> fixed a carry-forward mark bug (no look-ahead). Attempt 32. Writeup
> `docs/research/2026-07-14_M10-1_nagel_switch_results.md`. **The one thing that
> makes it real = M3 forward paper (Evan-gated).** Other panel survivor still to
> run: M10-2 gap-amortized stress IBS.

> **2026-07-14 — M10-2 gap-amortized stress IBS = FAIL; closes the E2 "c2c
> mirage" (record Appendix CK).** 2× QQQ MR on VIX>20 & IBS≤0.20, 5-session hold,
> trend fallback. Gate 2.99% CAGR / **83.3% DD** / Sh 0.28 (fails HR badly); sec
> 28.95% / 1.08 (one-window bull artifact). **Payload in the FAIL:** the 5-day
> hold neutralized the overnight gap (c2c 3.18% ≈ next-open 2.99%), isolating the
> reversion's gap-free economics — catastrophic in the gate. This **permanently
> closes the E2 c2c 18.15% "mirage"**: the gap was hiding the *drawdown* (2× into
> 2000–02/2008 crashes), not alpha. Sharpens M10-1: unlevered cross-sectional
> reversal passes, 2× index MR is an 83%-DD engine — M10-1's pass is a
> cross-sectional-survivor effect. **M10 arc COMPLETE** (both panel survivors
> run). Tripwire GREEN. Attempt 33. The only lever left to validate M10-1 = M3
> forward paper (Evan-gated).

> **2026-07-14 — X6 crypto pilot = FAIL; E6's lesson generalizes to crypto
> (record Appendix CF).** Evan "do 2" → authorized the crypto scope (X5 stays
> BLOCKED — can't buy the $22 FMP feed, free ratings = look-ahead). Prereg
> `prereg_x6_crypto_trend.md` → `run_x6_crypto_trend.py`: BTC/ETH dual-MA
> (SMA20>SMA100) long-or-flat, next-bar, **25 bps/side**, vs HODL. **FAIL
> (PROMISING-capped):** combined gate 2018–22 29.6% CAGR / DD 60.6% / Sharpe
> 0.76 **crushes HODL** 4.3% / 82.3% / 0.43, but sec 2023– Sharpe 0.76 < HODL
> **1.01** (bull) → fails the beat-HODL-both-windows bar. **Cost-robust** (33
> toggles/5yr — the "25 bps kills it" worry was wrong for a slow overlay).
> **Same lesson as equity E6:** MA trend = drawdown control, not a return-
> enhancer over buy-and-hold in bulls — the structural conclusion generalizes to
> a new asset class. Attempt 31 (30 equity + 1 crypto). Paper-first; nothing
> live; live-money crypto Evan-gated (custody). Tripwire GREEN. Writeup
> `docs/research/2026-07-14_X6_crypto_trend_results.md`. **No free experiment
> remains; all further work Evan-gated (M3 deploy; X5 FMP; live crypto).**

> **2026-07-14 — FREE SWEEP COMPLETE: M8 (C1–C7) + X3 all done; program at 30
> attempts (record Appendices CB–CD).** Evan: "run the Free + autonomous ones."
> Ran the full residual queue, each prereg-committed-before-runner, tripwire
> GREEN after each. **All FAIL/closed:** C3 vol-breakout (time-stop beats the
> channel exit — whipsaw tax); C4 M-M vol-sizing (real DD-cutter, best Sharpe
> 0.77 < 0.80); C6 FOMC even-week (replicates CMVJ then INVERTS post-2014 —
> cleanest decay exhibit); **C1 residual reversal (CLOSEST-EVER: gate 19.08%
> CAGR/DD 57.7% clears both HR legs in-window, dies post-2014 + survivorship)**;
> C2 dividend-initiation (closed on probe, 3 events/26yr); **C7 SVXY carry
> (highest CAGR ever 26.45% and still FAIL — Sharpe 0.76 < SPY 0.82, rides the
> dead −1× instrument, dodged Volmageddon by 1 session = N=1 luck)**; **X3 Reg
> SHO short-volume (FAIL — SVR spread +1.24%/Sh 0.16 = noise; clean contrast to
> X2's real +18.39% short-INTEREST spread)**. Meta-result: the sweep produced
> the program's most *tempting* numbers (C1/C7/C4) and the pre-registered
> both-windows/risk-adjusted/era-honest bars killed every one — the discipline
> demonstrating itself. **Capstone finalized to 30 attempts. No free experiment
> remains; the documented method space is exhausted. Remaining work is
> Evan-gated only (M3 deploy; X5 $22 / X6 crypto).**

> **2026-07-13 — CAPSTONE written; X1 = FAIL; X3 interrupted (record Appendices
> BX–BZ).** Evan: "do 2 then 1 and 3." **(2) Capstone:**
> `docs/CAPSTONE_program_synthesis.md` — the standing full-program synthesis
> (methodology-as-deliverable + 8-family/24-attempt ledger + structural WHY +
> the one uncatchable anomaly). **(1) X1 conditional vol-targeting = FAIL**
> (`prereg 07c22cb` → `run_x1_vol_targeting.py`): the E6×E18 interaction on SPY
> doesn't beat the plain 200-DMA — gate 2006–13 (a) E6 Sharpe 0.58/DD 19.9% is
> best, (c) conditional 0.42 ties VIX-TS and loses to E6; H1 rejected, confirms
> E18. Attempt 24. **(3) X3 Reg SHO short-volume: INCOMPLETE** — ingester
> `ingest_regsho_short_volume.py` (parser tested 3 eras, browser-UA fix for
> Cloudflare) launched, but the background fetch was interrupted at ~2010-05
> (193/~4300 days in `.regsho_cache/`, gitignored, resumable). X3 deferred
> (strong FAIL-prior; won't change the terminal claim). Tripwire GREEN
> throughout. **All session work pushed to origin/main.**

> **2026-07-13 — X2b short-side = FAIL; X2's "strongest anomaly" was a
> frictionless mirage (record Appendix BW).** Evan said "do 1" (pursue the
> short-side). Read as *rigorously test it*, not "open a shorting account"
> (Evan-only). Prereg `prereg_x2b_short_side.md` (`e718f6f`); runner
> `scripts/run_x2b_short_side.py` with real short accounting + a **borrow-fee
> sweep** (0/2/5/10/20%/yr) + delta-turnover trading (caught + fixed a
> full-churn cost over-charge first). **FAIL:** LS gross 17.13%/Sharpe 0.92
> (= X2 spread, edge exists) decays to **9.24%/Sharpe 0.56 at 5% borrow**, only
> **5/9 years positive**; **pure short is negative at every borrow level**
> (high-DTC basket is a mix — IBM/TXN/ORCL rallied — + vol drag + bull tape).
> Breakeven borrow 13.8% ≫ real large-cap borrow, so it fails on risk-adjusted
> return + lumpiness, not borrow supply. **Answer to "pursue the short-side":
> DON'T** — not a deployable market-neutral sleeve; sizing up a margin/shorting
> account isn't justified. The short-side lead is CLOSED. Tripwire GREEN. Writeup
> `docs/research/2026-07-13_X2b_short_side_results.md`. Tally 23 attempts.

> **2026-07-13 — X2 days-to-cover = FAIL (deployable), short-interest anomaly
> real short-side but does NOT survive honest costs (see X2b above; record
> Appendix BU).** Ran the
> data-unblocked E17 on FINRA consolidated short interest (public REST API, no
> auth, 205 biweekly dates 2017-12-29→2026-06-30, 39/39 coverage; scout Appendix
> BU verified access). Prereg `prereg_x2_days_to_cover.md` (`4094889`, doc-only,
> first use of the new TEMPLATE); MODIFIED-WINDOW CAP (single 2018–2026 →
> PROMISING max). **Deployable long-only lowest-DTC leg FAILS:** net 13.32%
> CAGR / Sharpe 0.60 beats SPY on CAGR (12.53%) but loses Sharpe (0.60<0.71) →
> fails the pre-committed CAGR-AND-Sharpe bar. **But the anomaly is alive &
> correctly signed:** long-short spread +18.39% / Sharpe 0.98, high-DTC leg
> −2.63% (most-shorted mega-caps underperform SPY ~15pp/yr) — Boehmer-Huszar-
> Jordan alive on the modern tape. The alpha is **entirely on the non-deployable
> SHORT leg** (no fractional shorting at $100–1,000), exactly as the prereg
> predicted a priori. *(NB: the +18.39% spread is a frictionless gross number;
> X2b above shows it does NOT survive realistic trading+borrow costs — FAIL. The
> earlier "strongest real anomaly" framing is corrected there.)* Ladder A
> 15.93%→B 16.07% (gap flat)→C 13.32% (pure cost). Tripwire GREEN. PASS-HR stays
> 0. Writeup
> `docs/research/2026-07-13_X2_days_to_cover_results.md`. **X3** (Reg SHO
> short-volume) = feasible-deferred (access proven, noisier build). **Free queue
> open:** X3, X1 (vol-targeting); the short-side finding is an Evan-gated
> capital/scope question (shorting needs a bigger account).

> **2026-07-13 — EX-DECOMP (M9 #44) done: closed FAILs decomposed (record
> Appendix BS).** Diagnostic (no D1 verdict; tally unchanged). Ran an A/B/C
> execution ladder (A=c2c 0bps, B=next-open 0bps, C=next-open 5bps) on
> E13/E14/E15/E16/E20; `scripts/run_ex_decomp.py`, writeup
> `docs/research/2026-07-13_EX-DECOMP_results.md`. Regression GREEN (Rung C
> reproduces recorded FAILs), tripwire GREEN. **The PRD's "most signal-dead"
> guess was wrong — only E14 is SIGNAL-DEAD.** E13 = COST-GATED (real calendar
> edge, turnover-killed); E15 = SURVIVES-NULL gate / decays OOS; E16 =
> SURVIVES-NULL gate but survivorship + fails null 2014→; E20 = real-but-
> subscale gap-loaded overnight edge, negative after cost post-2014. Two
> recurring killers — overnight gap (A→B) and cost/turnover (B→C) — not one flat
> null; reconfirms E6-1× (low turnover) as the only sane M3 deploy candidate.
> **Next open:** M9 #43 (prereg-template, doc-only, free), or Evan redirects.

> **2026-07-13 — E19 insider-buy drift = FAIL (clean); M7b CLOSED (record
> Appendix BR).** EDGAR Form-4 ingestion completed (39/39). Ran
> `scripts/run_e19_insider.py` (opportunistic buys, CMP classification,
> next-open, 40-session hold, K=5, survivor universe). **FAIL per D1
> `ebf54a4`:** gate 2003–13 CAGR 4.68% / DD 53.6% / Sharpe 0.31; secondary
> 2014→ CAGR 4.91% / DD 42.6% / Sharpe 0.35 — **underperforms SPY on CAGR AND
> Sharpe in BOTH windows**; both pass tiers fail. Frozen tripwire GREEN (12
> refs, d=±0.0000pp). **Data-quality:** heavy transactionCode-"P"
> contamination (BAC = 44% of all P-buys, dominated by BAC's own issuer CIK,
> incl. $0.01 1-share artifacts); the CMP classifier passed 95% through
> (Appendix-BQ "routine will absorb it" prediction **falsified**). A post-hoc
> de-junk sensitivity (price ≥ $1/$5, same-owner-day dedup cutting entries
> 6,119→2,675) leaves the verdict unchanged and flat sub-beta → **cleaning
> reveals no masked edge; FAIL is robust, not a contamination artifact.**
> Writeup `docs/research/2026-07-13_E19_insider_results.md`. E19 = the 8th
> family (insider/informed-positioning). **Remaining-work split (corrects the
> earlier "autonomous wall" framing — the 2026-07-12 survey + M8/M9 reopened
> free experiments):** *autonomously runnable now, no money/account, but all
> strong-FAIL-prior per the survey* = M9 tasks 43 (prereg-template), 44
> (EX-DECOMP retrofit), 45/X1 (vol-targeting), 46/X2 (FINRA short-interest
> 2021+, FREE), 47/X3 (Reg SHO short-volume 2009+, FREE), and the M8 C1–C7
> data-probe candidates. *Genuinely Evan-gated* = M3 Alpaca paper deploy
> (account+keys+go); X5 (FMP $22); X6 (crypto scope + 25 bps fees); borrow-fee
> (Ortex ~$129); X4/MOC and the LLM arc (need intraday data / M3 live — the
> EOD-only rule blocks MOC until an intraday source exists). Per the PRD
> execute-next-task loop the default idle action is now the cheapest free M9
> task, but expected value is low and Evan may prefer to deploy or stop.

> **2026-07-12 — E19 ingestion RUNNING + full method survey delivered (record
> Appendices BI–BK).** **E19:** Evan authorized + restarted the full EDGAR
> Form-4 ingestion; background task `b2wzwj9gb` is ~7/39 tickers cached
> (~104,496 docs, ~7/s, ~3h). On `INGEST COMPLETE` → run
> `scripts/run_e19_insider.py` (opportunistic-buy drift, D1 + asymmetric
> survivorship framing; prior = near-certain FAIL) → verdict → results → record
> → commit. **Method survey:** ran /research-brief across ALL 8 method families
> (~90 methods, primary-source-graded) →
> `docs/research/2026-07-12_swing_method_full_survey.md`. Payload = the
> reconciliation: literature's top "untested" ideas are ALREADY KILLED here
> (sector momentum E14, turn-of-month E13, earnings premium E15, raw weekly
> reversal E16, dividend capture E20). After reconciliation the genuinely-open
> set is small + all strong-FAIL-prior: (1) short-term RESIDUAL reversal
> (fixes E16's 65.9% DD), (2) dividend-INITIATION drift (≠ E20 capture),
> (3) one consolidated volatility-breakout kill-shot, (4) Moreira-Muir
> vol-targeting sizing overlay, (5) free Reg SHO daily short-volume drift,
> (6) even-week FOMC overlay, (7) SVXY carry gated by VIX-TS. Structural
> conclusion (Hou-Xue-Zhang / McLean-Pontiff / Avramov-Cheng-Metzker): K=1–3
> concentration destroys diversified-decile edges + the edges live in illiquid
> names the floor excludes — 0-for-20 is what an honest retail-EOD program
> should produce. Tally UNCHANGED (survey is research, not a run): 0 PASS-HR /
> 1 weak PASS-RA / 20 attempts / 7 families.

> **2026-07-11 — M7b data-type arc done (record Appendices BD–BF); autonomous
> wall.** **E18 regime-gate bake-off:** no new gate (VIX-TS / HY-OAS /
> breadth) beats the plain 200-DMA overlay on the robust both-windows
> criterion (confirms E6/E7) — BUT per the pre-registered D1, the VIX/VIX3M<1
> gate cleared **PASS-RA, the program's first tier-pass**. It is flagged
> **WEAK**: 2006–13 window (VIX3M starts 2006) has one crash, so the pass
> largely = dodging 2008, and it has *worse* drawdown than buy-hold in the
> 2014→ bull. Per D1 it is a **forward-paper candidate only**, not a validated
> edge; PASS-HR stays 0. (HY-OAS arm inconclusive — FRED free data only
> ~2023+.) **E20 dividend capture:** FAIL — a real but tiny ex-date edge
> (+0.10%/trade) that doesn't compound (0.6%/yr, negative post-2014) and is
> pre-tax. **E19 insider/EDGAR:** FEASIBLE-BUT-DEFERRED — Form-4 data parses
> (39/39 CIKs) but the historical build is the project's heaviest with three
> hazards (CIK changes, XSL-vs-raw-XML, ~1000-filing API cap); deferred vs a
> near-certain-FAIL prior, Evan-gated. **Remaining work is ALL Evan-gated:**
> M3 Alpaca paper deploy of E6-1× (+ the caveated VIX-TS candidate); E19 full
> ingestion authorization; a paid data budget (unblocks HY-OAS, short
> interest / the never-run days-to-cover E17).

> **2026-07-11 — M7 catalog arc E13–E17 all closed (record Appendices
> AX–BC); D1 dual-bar verdict adopted (Appendix AW).** Evan approved D1: a
> pre-registered risk-adjusted tier (PASS-RA: gate Sharpe ≥ 0.80 AND > SPY
> both windows AND positive CAGR both) alongside the unchanged PASS-HR
> (CAGR ≥ 15%, maxDD ≤ 60%). Then ran the five catalog candidates:
> **E13** turn-of-month FAIL (1.4%/yr; matched SPY in the flat decade at 19%
> exposure but lost the bull); **E14** diversified sector momentum FAIL —
> survivorship-CLEAN, the program's cleanest negative, momentum lost to
> equal-weight buy-hold of the same sectors every window; **E15** earnings-
> announcement premium FAIL (clean; the decayed-anomaly twin of E10 — beat
> benchmarks in 2000–13, faded post-2014); **E16** weekly reversal FAIL
> (clean) — the notable one: gate CAGR **16.76%** cleared the 15% return bar
> (first ever) but on **66% drawdown** (breaches ceiling) + Sharpe 0.61, and
> the headline is the expected survivorship artifact of dip-buying survivors;
> **E17** days-to-cover **BLOCKED-ON-DATA** (no free exchange-listed short-
> interest history). Results in `docs/research/2026-07-11_E13..E17_*`.
> **Program 0 PASS / 17 attempts / 7 families.** Next: M7b (E18 regime-gate
> bake-off, E19 insider-EDGAR-probe-gated, E20 dividend capture).

> **2026-07-10 — E10/E11/E12 all FAIL; article-set arc closed (record
> Appendices AO–AP).** Evan supplied a 5-source article set (Investopedia/
> Schwab/TD/CapTrader/SMB + ex-Trillium trader) and said "try everything."
> Three testable directions pre-registered together (`129dc22`, doc-only
> before runners): **E11** volume-gated breakout (E8 + RVOL≥1.5, the pros'
> rule) FAIL — gate CAGR −0.74%, volume thins the signal without giving it
> direction; **E12** confirmed-capitulation MR ("right side of the V") FAIL —
> gate CAGR −4.71%, waiting for confirmation does WORSE than raw dip-buying
> (the confirmation bar surrenders the overnight pop that holds the edge);
> **E10** post-earnings drift (PEAD, E3's survivor basket, asymmetric
> framing) FAIL clean — gate CAGR 5.93% vs 15% bar. NUANCE: E10 is the only
> experiment to beat both benchmarks in 2000-13 (vs EW −0.47%, SPY 1.72%) —
> a real-but-small effect that decayed after ~2010. Results:
> `docs/research/2026-07-10_E10_E11_E12_results.md`. Frozen tests green.
> **Base rate now 0 PASS / 13 attempts / 6 families.** Every codifiable idea
> from the Reddit thread and the article set is tested and falsified.

> **2026-07-10 — E8 + E9 both FAIL; families four and five closed (record
> Appendices AL–AM).** Evan supplied the r/swingtrading strategy thread; its
> two genuinely-new families were pre-registered together (`9b49190`,
> doc-only before runners) and run. **E8 squeeze breakout: FAIL** — gate
> 2000-13 CAGR −1.43%, only +1.10%/yr even in the 2014-26 bull (compression
> predicts expansion, not direction). **E9 "never book a loss" deep-dip
> audit: FAIL with both a-priori predictions CONFIRMED** — the Reddit claim
> is literally true (0/53 realized losses, 100% win rate) AND bad (gate CAGR
> 3.46%, a −79.7% unrealized position, a ~17-year underwater hold, cash idle
> 38% of days): the win rate measures bookkeeping, not performance. Results:
> `docs/research/2026-07-10_E8_E9_results.md`. Frozen tests green. **Base
> rate now 0 PASS / 10 attempts / 5 families.** Repo published PUBLIC at
> https://github.com/Evan-Daruwalla/Swing-Trading-Project (Appendix AK).

> **2026-07-10 — E3 stock momentum FAIL; third family closed (record
> Appendix AI).** Evan opened E3 (concentrated stock momentum). Prereg
> `87bc8d9` with asymmetric-falsification framing (survivorship+lookahead bias
> → only a FAIL is clean). Result: 2000-2013 gate CAGR 6.27% (FAIL vs 15%),
> and momentum UNDERPERFORMED equal-weight buy-hold of its own survivor
> universe in every window (2014-26: 4.79% vs 14.94%). Clean close. **All
> three high-return routes — index mean reversion, leveraged trend, stock
> momentum — now falsified under pre-registration.** Write-up updated to E1→E7
> + E3.

> **2026-07-10 — Program closed + packaged (record Appendices AF-AG).** E7
> (prereg `70ed2a1`) tested on genuinely-unseen non-US regimes (Nikkei 1985+,
> DAX/FTSE/HSI/ASX). **Both arms FAIL:** Arm 1 — E6's 1× overlay generalizes
> to only 3/5 markets (works Japan/Germany/HK, fails UK/Australia) → **E6
> downgraded to market-dependent**; Arm 2 — even a-priori-vol-gated 3×
> rotation fails every gate (mean CAGR 4.55%, 83–97% DDs; HSI 3× mathematically
> wiped out by the 1987 crash). **The high-return-robust question is CLOSED
> with out-of-sample evidence.** Findings write-up updated to E1→E7; README
> added (`M6` packaging). Frozen tests green (12 refs).
>
> **Bottom line:** no high-return-robust EOD edge exists in what was tested
> (now OOS-confirmed). One partly-deployable result: 1× MA rotation as a
> market-dependent risk-management overlay. Deliverable =
> `docs/findings_2026-07-09_experiment_arc.md`.

> **2026-07-09 — C1 + three screens (record Appendices W–Y).** Engine v2
> (`size_on_nav=True`: NAV-proportional, cash-capped; v1 refs intact; 10
> frozen refs green d=±0.0000pp). Screens (in-sample, hypothesis-generating):
> **A3 overnight-IBS DEAD** (broad negative; lev holdout +0.56%/mo < failed
> E2) — Evan's A3 override spent, IBS stop resumes; **B1 gap-reversion DEAD**
> (best +0.23%/mo); **B4 TQQQ/QQQ 200d-MA rotation STANDOUT: +2.59%/mo
> train, +2.15%/mo holdout (CAGR 29%), Sharpe ~0.8, maxDD 48–58%, ~4
> switches/yr.** Caveats recorded: screen saw the holdout (contaminated for
> prereg), variant selection, weeks-long holds stretch the "swing" label.
> **Proposed next: pre-register E4 (TQQQ/QQQ rotation) with robustness-
> battery gates + live paper as true OOS — awaiting Evan.**

> **2026-07-09 — E2 = FAIL; IBS FAMILY SHELVED (record Appendices S-U).**
> E2 (leveraged TQQQ/UPRO/SPXL/SOXL/TNA, K=2, prereg `865c09e`) holdout
> 2022-26: n=351 PASS, exp +31bps PASS, **CAGR 7.98% FAIL (vs 15%), maxDD
> 60.6% FAIL (vs 60%)**. Train 19.6% CAGR → holdout 7.98%: same OOS decay as
> E1b. The c2c (non-executable) run would have PASSED (CAGR 18.15%) — the
> overnight gap remains the killer (M1.8: 54% of edge). **Prereg §7 stop
> executed: no E2b/E1c/execution variants without a NEW dated Evan decision.**
> Engine gotcha logged: fixed initial-capital/K sizing (not NAV/K) — K=1 3x
> run sent NAV negative; future engines size on current NAV. Frozen tests:
> 8 refs (E1+E2) green d=±0.0000pp. Three-experiment scoreboard in Appendix
> U. **No live trading. Options: E3 design / Evan overrides stop for
> near-close-execution IBS / write up the arc.**

> **2026-07-09 — E1b OOS test = FAIL (near-miss) (record Appendix Q).** Evan
> chose to pre-register broad_us with a holdout. E1b (`0126ce3`): broad_us
> HOLDOUT 2022-26 next-open 5bps → n=560, exp +17.8bps (PASS), **Sharpe
> 0.4961 (FAIL vs 0.50)**, maxDD 9.8% (PASS). Fails by 0.004 of Sharpe — NOT
> rounded up. BUT the edge substantially PERSISTED OOS (train 0.66 → holdout
> 0.496 through the 2022 bear) — real-but-decayed, unlike E1's decisive fail.
> Cost is the swing factor (0bps→0.76, 10bps/side→0.23); 5bps/side is
> conservative for SPY/QQQ/DIA/IWM (~1bp spreads). Sectors confirmed dead
> weight (Sharpe −0.05). **No live trading. Awaiting Evan — options below.**

> **2026-07-09 — E1 = FAIL (record Appendices N-P).** Full 29-ETF IBS run per
> `8963e49`: Sharpe 0.23, maxDD 36% → FAIL, no tuning. Cost-fragile; country
> ETFs drag; post-2021 decay. Frozen refs pinned (green, d=0.0000pp).

> **2026-07-09 — M0.4 executed (record Appendix H).** Coverage/quality gate
> `swing_bot/coverage_gate.py` (coverage vs listed-tickers + sanity scan);
> done-check green (OK on real data, fails on truncated fixture). Found 19
> real zero-range bars in XLRE's first 5 months → **E1 MUST skip high==low
> days (IBS div-by-zero); logged in gotchas bin.** Next: M0.5 (frozen-
> regression harness).

> **2026-07-08 — M0.3 executed (record Appendix G).** Frozen 29-ETF universe
> in `swing_bot/universe.py` (4 broad US + 11 SPDR sectors + 14 country/
> regional), each with a verified first-bar date + inclusion reason. Full
> backfill (`scripts/backfill_universe.py`) wrote 89,666 rows into
> `swing.db`. Flag for later: country-ETF IBS has a stale-NAV/overnight
> mechanism distinct from US-index IBS — report E1 per-group. Next: M0.4
> (coverage/quality gate).

> **2026-07-08 — M0.2 executed (record Appendix F).** Data-path decision:
> **own yfinance fetcher**, NOT reuse of Trading's price_cache. Reason:
> price_cache has no high/low/open series (only close+volume+flags), so IBS
> is uncomputable from it; it also lacks DIA/IWM + all country ETFs and has
> no next_open for ETFs. Wrote `swing_bot/prices.py` (OHLCV → `swing.db`,
> `auto_adjust=False`); validated (SPY/QQQ backfilled, IBS computes).
> Tooling: Grep/Glob don't reach `D:\ClaudeCode\Trading`; use venv-python +
> PowerShell for its DB. Next: M0.3 (freeze ETF universe).

> **2026-07-08 — M0.1 (record Appendix E).** Repo skeleton, `.venv`, git
> init; commits `4ac785c`/`940a239`; deps pinned `3ba9cc1`
> (requirements.txt + requirements.lock). Env note: Python 3.14 + pandas 3.0
> are bleeding-edge — pin/downgrade rather than code around any pandas edge.

### Workstreams (mapped to PRD milestones)

| Workstream | PRD | Status | Notes |
|---|---|---|---|
| Doc/memory system | — | **Done** | Bootstrapped 2026-07-08 |
| PRD_ROADMAP.md | — | **Done** | Written 2026-07-08 to council program + Evan's overlay decision |
| Foundations (repo/venv/data/universe/gate/tripwire) | M0 | **Done** | All 5 tasks; modules prices/universe/coverage_gate/signals/test_frozen; `swing.db` 89,666 rows |
| Pre-registration & fill ablation | M1 | **Done** | M1.6 power (`2a9edde`) + M1.7 prereg (`8963e49`) + M1.8 ablation; next-open keeps ~64% |
| E1 IBS backtest | M2 | **Done — E1 FAILED** | Engine (`415c527`), verdict (`d28f899`), frozen refs pinned. E1b OOS near-miss (Sharpe 0.4961, `1a71468`). M2.12 survivorship deferred |
| E2 leveraged-ETF IBS (high-return arm) | M2b | **Done — E2 FAILED** | Prereg `865c09e`; CAGR 7.98%/maxDD 60.6% vs 15%/60% gates; refs pinned; **IBS family SHELVED (pre-committed stop)** |
| E3 concentrated stock momentum | M2c | **FAIL (clean)** | `87bc8d9`; 2000-13 CAGR 6.27% vs 15%, < buy-hold. Stocks closed for a backtested high-return claim |
| E4 leverage rotation (3×) | M2d | **PASS backtest, FAILED regime test** | `313d88a` PASS 2014-26; E5 `09a3a31` FAIL 2000-13 (92.7% DD). De-authorized |
| E6 de-leveraged rotation (1×) | M2d | **PASS, later downgraded** | `0526ea2`; robust in US, but E7 showed market-dependent (3/5). Risk-mgmt overlay, not high-return |
| E7 international validation | M2e | **Both arms FAIL** | `70ed2a1`; closed the high-return-robust question on 5 unseen non-US regimes |
| Live paper | M3 | **RUNNING since 2026-07-15** | 3 sleeves (e6_1x / e18_vixts / m10_1_nagel), one $1,000 Alpaca paper account each; 20 sessions, task S4U green. Row said BLOCKED for 4 weeks after deploy — corrected 2026-08-13, record EO |
| Program write-up + packaging | M6 | **Done** | Findings doc updated to E1→E7; `README.md` added; git tag |
| Live paper: LLM-veto overlay sleeve | M3/M4 | **NOT BUILT — spec superseded** | the `e1_control`/`e1_llm_veto` pair died with E1 (M2b); M3 deployed 3 mechanical sleeves instead. Evan's go and the Alpaca accounts are no longer blockers — an overlay arm needs its own prereg (corrected 2026-08-13, record EO) |
| Overlay readout (continue/cascade/kill) | M4 | **GATED** | At pre-registered N / time horizon |
| Expansion (deferred ideas) | M5 | **GATED** | On M3 stable |

## Candidate strategies (supplied by Evan 2026-07-08 — none chosen yet)

| # | Strategy | Codifiability | Notes |
|---|---|---|---|
| 1 | Trend pullback (20 EMA > 50 EMA, buy 1–3 day dip to 20 EMA, stop below pullback low) | High | Objective rules, EOD-data friendly |
| 2 | Bull-flag breakout (pole + flag channel, buy resistance break) | Low | Pattern detection is fuzzy; hardest to backtest honestly |
| 3 | Mean reversion (RSI < 30 / Bollinger extremes, capitulation + reversal day) | High | Survivorship bias hits this hardest — delisted crashers are exactly what it buys |
| 4 | Sector rotation (leading sector ETFs → leading stocks breaking out) | Medium | Longer holds; overlaps Trading's `sector_momentum` factor |

Full descriptions as Evan gave them: record Phase 0.

## Reusable infrastructure (map of `D:\ClaudeCode\Trading` — verify before use)

- **Data**: `scripts/momentum/daily_price_refresh.py` (~5,200 tickers, EOD),
  `price_cache` SQLite table (SPLIT-ADJUSTED, DIVIDEND-UNADJUSTED,
  `auto_adjust=False`; also caches `next_open`), `trading_bot/factors/universe.py`
  data-quality/universe filters (MIN_DOLLAR_VOL currently 0 — a known gap that
  becomes mandatory to fix at this capital size).
- **Backtest**: `trading_bot/execution/factor_backtest.py` harness;
  frozen-regression-test pattern in `trading_bot/strategies/test_strategies.py`.
- **Paper engine**: `trading_bot/execution/paper_trader.py` schema
  (paper_portfolio / paper_positions / paper_nav / paper_transactions)
  tolerates any cadence; `paper_rebalance.py`'s buy-top-N-hold-a-month logic
  will NOT transfer.
- **Alpaca PAPER**: `alpaca_client.py` (live hard-guarded), `alpaca_sync.py`
  (CASH_BUFFER = 0.01), `fractionability.py` — whole-share fallback is
  load-bearing, not an edge case, at $100–1,000.
- Trading's own `HANDOFF.md` / `.claude/codebase-memory/` are ground truth for
  that repo; the inventory in record Phase 0 is the map, not the territory.

## Hard constraints

- EOD data only: signals computed at close, executed next open. No intraday
  entries or candlestick-trigger logic until an intraday data source exists.
- At $100–1,000, spread/slippage and fractionability dominate economics; a
  real liquidity floor is mandatory, not optional.
- Survivorship bias (yfinance carries currently-listed names only) — every
  backtest is upper-bound-biased; short-horizon mean reversion worst-affected.
- Never modify anything in `D:\ClaudeCode\Trading` from this project without
  Evan's explicit instruction. Never run backtests concurrently against
  Trading's DB.
- If Trading's `price_cache` is reused: read-only from here, and honor
  split-adjusted / dividend-UNadjusted everywhere.
- **Research scripts now REFUSE a stale or mixed-vintage cache (2026-08-12,
  record Appendix EM; the three sites that SWALLOWED that refusal were closed
  2026-08-13, record Appendix EO).** `_note_vintage` in
  `scripts/run_e8_squeeze.py` — the shared data layer **31** files import (30
  experiment runners + the standing proof script), 28 of them naming
  `cache_fetch` itself — raises `StaleCacheError` instead of printing.
  **CACHE REFRESHED 2026-08-13 (record Appendix ER) — the guard is currently
  SILENT and research scripts run.** `.e8e9_cache` is **181 price series at ONE
  vintage, 2026-08-12**, verified with the guard ON and no override. It had held
  5 vintages spanning 2026-07-09 to 2026-08-04, every one of them stale.
  **When it goes stale again, "refresh the cache" is not a one-liner.** It means
  refetching **every** price series, not a subset, and in one sitting: use
  `cache_fetch(t, through=<last settled session>)`, which refetches on a
  short series, with `SWING_ALLOW_STALE_CACHE=1` set FOR THE REFRESH ITSELF
  (a refresh is inherently mixed-vintage while in flight and the guard would
  abort it). A one-script re-run only touches the tickers that script names and
  just replaces the old mixed vintage with a new one. No refresh tool is
  committed and none should be built. The `*_div` / `*_earn` / index side-files
  carry no bar date, are invisible to the guard by design, and are not
  refreshed by this.
  **CHECK THE LAST BAR BEFORE TRUSTING A REFRESH.** Run after the close but
  before the next session and yfinance will hand you a FORMING bar for today.
  The tell is the volume format: a settled day is rounded to hundreds (SPY
  2026-08-12 = 33,179,100), a forming one is not (30,258,928). The 2026-08-13
  refresh wrote one such row into all 181 files and it was trimmed back out.
  Truncate to the last session `paper_nav` actually completed.
  Deliberate historical run: `SWING_ALLOW_STALE_CACHE=1` — strict `=1`, so
  `true`/`yes` silently do nothing and the run still raises (deliberate: an
  override that disables a correctness guard must fail closed); tolerance
  `SWING_MAX_CACHE_STALE_DAYS` (default 5).
  **The live M3 paper loop is unaffected**, but not for the reason this file
  used to give. It DOES import the module, transitively, on every run
  (`daily_swing_paper.py:64` → `run_e10_earnings_drift:27`; `:65` →
  `run_c1_residual_reversal:29`) — it pulls only `UNIV`, `residual_series` and
  `BETA_N`, none of which call `cache_fetch`, the guard's only caller. The
  earlier wording, "`daily_swing_paper.py` does not import that module", was
  false; the conclusion was right for the wrong reason (record EO).

## Decisions taken 2026-07-08 (details in record Appendices B–C)

- Strategy: E1 = ETF IBS mean reversion, per evidence brief + council.
- LLM overlays KEPT and LIVE-ACTING (Evan, overriding council's power-based
  drop; amended same day from a shadow-mode draft) — M3 runs `e1_control`
  (mechanical) + `e1_llm_veto` (treatment) sleeves in parallel from day one;
  overlay readout/kill decision gated on pre-registered N (PRD M4).
- Data layer: read Trading's `price_cache` read-only if ETF coverage
  confirms (PRD M0.2 verifies), own `swing.db` for positions/results.
- Bull flag / sector rotation / 16 other ideas dropped with documented
  reasons (record Appendix B).

## Open decisions (BLOCKED-ON-EVAN)

- ~~POST-E1b direction~~ **RESOLVED 2026-07-09 by Evan's goal redefinition
  (record Appendix R): high-return concentrated path → E2 (leveraged-ETF
  IBS) next, E3 (stocks) after. Prior option menus preserved in record
  Appendices P/Q.**
- **Capital range**: brief says $100–1,000; inventory header said $100–10,000.
  Assuming $100–1,000; sizing is parameterized regardless.
- ~~**Alpaca PAPER account** (PRD M3.15): which of ~3 paper accounts~~
  **RESOLVED 2026-07-15 (record Appendix CQ): 3 NEW dedicated paper accounts,
  $1,000 each, one per sleeve — none of Trading's.** (Left sitting unstruck
  under BLOCKED-ON-EVAN for 4 weeks; corrected 2026-08-13, record EO.)
- **M2.12 survivorship bound**: deferred as moot for failed ETF-only E1; run
  only if a stock strategy enters scope.
- **RUN V3?** `docs/prereg_v3_pbo_scoping.md` is WRITTEN and committed doc-only
  (`6194847`, 2026-08-13, record ET) and **not run**. It scopes PBO to config
  sets where selection is real: sets are declared `SELECTION` or `EXCHANGEABLE`
  at the call site, PBO gates only the former. No threshold moves. Running it
  means editing `swing_bot/validation.py` + `scripts/run_v1_harness_check.py`
  and re-running the harness. **Deliberately left for Evan** — a prereg run in
  the same session it was written is what pre-registration exists to prevent.
  Pre-committed failure condition: if pure noise is ACCEPTED under V3, V3 FAILS
  and reverts in full.
- **Audit #4 F14** — `UPDATE paper_sleeves SET cash=round(cash,9)` to clear a
  floating-point residue. **THREE rows, not one** — re-derived 2026-08-18 (record
  EY): `e6_1x −1.1368683772161603e-13`, `e18_vixts` and `m10_1_nagel` both
  **+1.1368683772161603e-13**. Every prior statement of this item said "one-row";
  the statement was wrong, the un-`WHERE`d UPDATE was always the right scope. A
  write to the live paper ledger, so Evan's call.
- ~~**F2/F3 preregs**~~ **F2 CLOSED 2026-08-19 (record FD)** — E5/E7 now
  implement E6's convention; no verdict moved. **F3 STILL OPEN, and its scope is
  INVERTED (record FG):** the floor provably NEVER fires on the 39-name stock
  universe (0 of 260,363 ticker-sessions), while the 29-ETF universe breaches it
  on 16.07% (26 of 29 names). Re-running the stock experiments would install a
  guard that cannot fire — this project's signature defect, a fifth time.
  Awaiting Evan's redirect. Original wording follows: the 200-DMA convention split (7 inclusive / 6 exclusive;
  E5 and E7 use the opposite convention from the E6 strategy they test) and the
  unenforced liquidity floor. Each moves already-recorded numbers, so each needs
  its own pre-registration; not drafted, because unlike V3 neither has a
  direction fixed in advance and both turn on a judgement Evan should make.

## Documentation
- `docs/Project Record — Full Chronological History.md` — append-only
  chronological record; **the ground truth**.
- `docs/Project Record — Full Chronological History.html` — the HTML twin
  (built 2026-08-19, record FE, closing the M6 gap FB flagged). **DERIVED and
  committed: regenerate with `.venv\Scripts\python.exe
  scripts\render_record_html.py` after EVERY append, or it drifts.** Never edit
  the `.html` by hand; if the two disagree the `.md` wins. The renderer EXITS 1
  on any broken internal anchor — which is how the record's own TOC was found to
  have 32 dead links, now repointed.
- `PRD_ROADMAP.md` — the standing plan (written 2026-07-08). Source of truth
  for what to build and in what order; no unstarted task remains — M3 forward
  paper is the only open lever and it needs elapsed time, not a task (this line
  still read "next open task = M0.1" until 2026-08-13; M0.1 shipped 2026-07-08).
- `docs/research/` — evidence brief, experiment-ideas list (+ council
  outcome pointer), future power calc / ablation docs.
- `.claude/codebase-memory/` — binned technical memory (INDEX + 11 bins).
- `graphify-out/` — the knowledge graph (`/graphify` queries it). **1665 nodes /
  2886 edges / 184 communities / 12 hyperedges as of 2026-08-13** (record ET).
  Wave 2 indexed the last 35 research docs; research-doc nodes went 80 → 384.
  **Still NOT indexed: the project record itself** — it re-reads as uncached
  every time an appendix is appended, and `build_merge` replaces ALL nodes for a
  re-extracted file, so a delta pass would trade its 126 existing nodes for a
  handful. All-or-nothing; open. **Treat the graph as navigation, never as a
  citation** — it is LLM-built and has shipped at least one false fact (record
  EQ). The record and the code are ground truth.
- `.claude/pm-cadence.json` — record entry every 3 prompts;
  handoff/PRD/bins event-driven.
