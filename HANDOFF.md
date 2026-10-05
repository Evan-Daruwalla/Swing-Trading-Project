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

> **2026-10-04 ~20:35 CDT - AUDIT GT ACTED ON (record GU). The loop is marking NAV
> every session; 23:45 was 8 of 9 nights clean.** Evan's four calls:
> (1) **09-22 BACKFILLED** by the GP method (ledger still frozen since 09-01, every
> rule HOLD on 09-22, all 66 rows in 09-01..10-02 reproduced to 1e-9); a read-only
> replica of the missed-session detector now finds **0 unacknowledged pairs**, so
> the next 23:45 run (Mon 10-05) can exit 0 - **read that log line to confirm;
> never run the loop to check.** (2) **FF3 lag:** Ken French's file ends
> 2026-08-31, so the live M10-1 stress basket can never form; the loop now says so
> in `RUN_FAILURES` on a stress decision day. Making it work changes the rule
> (prereg) - not done. (3) **Late fills** now book the open of the first session
> after the signal (the one Alpaca filled at), with a `LATE FILL` line, instead of
> a later wrong open. (4) Commit everything except the record files:
> **authorized but NOT DONE** - the permission system denied `git add` twice
> (record GV), so Evan runs it himself. The record waits for a relaunch with
> `PM_RECORD_UNLOCK=1` to redact GJ.
> Also new: a VIX staleness gate, and the sanity gate refuses a QQQ window under
> 200 bars. Proof `scripts/prove_loop_guards.py` 10/10 (fails 8/10 on the old
> behaviour); `test_frozen` GREEN.
>
> **2026-09-22 ~21:23 CDT - M13.2 FIX APPLIED, NOT VERIFIED (record GO).** Evan
> moved `SwingTradingDailyPaper` 19:00 -> **23:45 CT, Mon-Fri** (GH option D;
> `schtasks /query /xml`: StartBoundary 23:45, WakeToRun, StartWhenAvailable,
> enabled). 23:45 CT is 00:45 ET the NEXT day; `last_completed_session` still
> returns the session that just closed (5 cases checked incl. Friday, Labor Day,
> pre-Thanksgiving). **The loop was darker than this file said:** `paper_nav`
> has 09-18 but not 09-08..09-11, 09-14..09-17 or 09-21 - **9 sessions x 3
> sleeves = 27 holes**. ~~so the first 23:45 run will exit 1 even if the fix
> works~~ **BACKFILLED 2026-09-22 ~21:27 CDT (record GP), Evan's call:** all 27
> rows are exact reconstructions (ledger frozen, every rule said HOLD, formula
> reproduced the 15 live rows to 1e-9). The only holes left are the already-
> acknowledged 07-30 x3 and e6_1x 08-25..08-31, so ~~**tonight's run can exit 0.**~~
> **(2026-10-04, records GT/GU: it could not - that very 23:45 run still saw the NaN
> and refused, losing 09-22; 09-23..10-02 then all passed, and every one exited 1
> only because 09-22 was unacknowledged. 09-22 is now backfilled.)**
> Verify: no `REFUSING TO RUN -- price feed is BEHIND` line in
> `var/daily_swing_paper.log` (this said "FEED-CLOCK", text the log never prints -
> GT HIGH 3; my wording), and a
> `paper_nav` row for 2026-09-22 in all three sleeves. **At ~21:30 CT the
> 09-22 QQQ bar was STILL NaN** (backfill fetch), so 23:45 is a real test.
> **Council follow-up scored (record GQ):** by the rubric pre-registered before any
> advisor ran, v3 is worth its 3.6x cost, by a one-item margin. The exact time 23:45
> came from v3's chairman, not an advisor, and rests on one observation. Correction to
> GO: the 09-18 run fired at **20:51**, not 19:00 (log:1857), so the bar was clean by
> 20:51 that night. Artifacts: `var/council/2026-09-22/` (local, gitignored).

**Last updated: 2026-10-04 ~20:35 CDT** (record GU: audit GT acted on; 09-22 backfilled; late-fill/VIX/sanity/FF3 guards) — this file is the only live snapshot;
history lives in the record. **Timezone: record/doc stamps are Central,
DST-AWARE — read the offset from `date` and label by the number: UTC-6 → CST
(winter), UTC-5 → CDT (summer). Currently UTC-5 = CDT. The cadence hook
reports UTC — subtract the current offset (record Appendix AZ; made DST-aware
2026-07-19; an earlier version of this line hardcoded "CST (UTC-5)", which is
self-contradictory and was corrected 2026-07-28 by audit #7).**

> **2026-09-08 ~00:42 CDT - HOLD-N EXIT-AT-OPEN, analyzed not built (record GE).
> ANALYSIS ONLY: no code, no verdict, tally UNCHANGED.** Evan's thought
> experiment: hold 1-3 days, sell at the open, on SPY or "residual 05/95" from
> the Trading repo.
> **The multi-day hold IS the right fix for GD's cost problem, and it still
> loses.** Holding N days amortizes one round trip over N days: buy close(day 0),
> sell open(day N) captures N overnight legs and N-1 intraday legs. SPY goes
> -15.60 (N=1) -> -2.63 (N=2) -> **+1.70 (N=3)** -> +9.11 (N=21) pp/yr. **But
> buy-and-hold is 10.35, and the structure converges to it FROM BELOW and never
> crosses.** Exact form: **`net(N) = BH - (ID + 25.2)/N`** (25.2 pp/yr = 252 x a
> 10 bps round trip). It beats buy-and-hold only if the intraday leg loses more
> than **25 pp/yr**; the worst measured is IWM at **-4.09**. Strictly dominated
> at every N.
> **The exit-at-open detail is worth almost nothing** - versus exiting at the
> close it only forgoes one intraday leg per cycle, `ID/N` per year: +0.93 pp/yr
> on QQQ at N=3, and a small LOSS on SPY and DIA.
> **THE NUMBER THAT GOVERNS ANY VERSION OF THIS: a strategy round-tripping every
> N days pays 25.2/N pp/yr in cost.** N=1 25.2 · N=2 12.6 · **N=3 8.4** · N=5 5.0
> · N=21 1.2. A 3-day hold needs **8.4 pp/yr of gross alpha before it earns a
> cent**. For scale, M1.8 measured the IBS signal at +7.5 bps gross PER SIGNAL.
> **"residual 05/95" - two corrections.** (a) WRONG HORIZON:
> `D:\ClaudeCode\Trading\trading_bot\factors\residual_momentum.py` is
> Blitz-Huij-Martens residual MOMENTUM - 252-day formation ending 21 days back,
> regressed on SPY, scored `alpha/stdev(residual)`, ~4,000 tickers, **rebalanced
> MONTHLY**. Half-life in months; driving a 1-3 day trade with it is a slow
> signal on a fast trade. (b) **"05/95" does not exist in that repo** - the sleeve
> name `residual_roa_6535` is **65/35** (`zcombo.py:8-9` weights residual
> momentum 0.65, ROA 0.35). Recorded as NOT FOUND rather than guessed.
> **The version scoped for THIS project already exists and IS LIVE.**
> `run_c1_residual_reversal.py:1-7` is FF3 residual REVERSAL, 21-day residual
> sum, bottom K=4, **5-session hold**, weekly rebalance - the program's
> closest-ever HR near-miss (gate 19.08% CAGR, dies post-2014) and **already
> running in paper** as the VIX>20 stress branch of `m10_1_nagel`.
> **What the idea does NOT fix, and it is what bit C1:** ~~C1 leaked ~5 pp/yr from
> c2c 22.82% to next-open 17.87%.~~ **RETRACTED 2026-09-09 (records GF §1, GI §2).
> That pair is M10-1's, not C1's** — Appendix CI caveat (5) states it of the Nagel
> Switch with a parenthetical crediting the mechanism to C1, and the parenthetical
> became the subject one hop downstream. **C1's own gap is 2.78 pp** (Rung A c2c
> 28.24% vs Rung B next-open 25.46%, both 0 bps). M10-1's 4.94 pp is not even a
> timing delta: it is **2.04 pp timing + 2.90 pp cost**, and the timing half is
> stocks-only. What survives is the direction — **the leak is at ENTRY** - signed at the
> close, bought at the next open, forfeiting the overnight leg GD measured as the
> entire source of index return. Exiting at the open does not touch entry. The
> only fill that fixes entry is a market-on-close order = **X4**, blocked on the
> broker tier and the EOD-only rule. **The real question this lands on is "can we
> ENTER at the close?", already the one honest execution experiment left.**
> **Slip logged (GE §7):** I asserted "65/35" as a correction to Evan while
> having inferred it from the digits in a FILENAME, before reading any weighting
> code. The `claim-check` hook flagged it; verification came after the sentence
> and happened to agree. Same class as GA's accusation against FX (GC) and the
> E14 prediction (FV).

> **2026-09-10 ~23:22 CDT - LANDING-CHECK ON GK: THE LIVE LOOP IS STILL DARK (record GL).**
> **GK's retry did NOT fix M13.2.** Both scheduled runs since it landed refused
> with exit 1 - 2026-09-09 19:00 and 2026-09-10 19:00 - each printing GK's new
> "last row STILL carries a NaN after 4 attempts" line. `paper_nav` ends at
> **2026-09-04** for all three sleeves: **09-08, 09-09 and 09-10 are unmarked
> (9 sleeve-date holes)**. The NaN is real but lasts HOURS, not seconds: clean at
> 17:35 CT (GH), NaN at every 19:00 CT run since 09-08, clean again by ~23:10 CT
> on 09-10. A 2/5/15-second ladder cannot span that. GH section 4 had already
> warned that option (b) assumed a transient the evidence did not show; I shipped
> it as the fix anyway. What GK DID land is option (c): the log now names our
> filter instead of blaming the vendor.
> **Decisions only Evan can take:** (1) the real fix, now with three nights of
> evidence - GH (d) move the scheduled run past the revision window, or (a)
> narrow the filter; (2) the three dark sessions - once any run succeeds, the
> missed-session detector puts 09-08/09-09 into `RUN_FAILURES`, so every run
> stays red until they are backfilled or added to `ACKNOWLEDGED_NAV_HOLES`;
> (3) whether to re-run the loop now that the feed is clean - it places orders,
> and it would mark only the latest session; (4) **do not commit the record
> yet**: GJ, the scheduled audit's entry, contains Evan's personal email on one
> line, and HEAD has none.
> **Still open from GJ:** section 4 HIGH - `scripts/run_e8_squeeze.py` feeds 34
> of 73 internal modules and has zero tripwire coverage (Evan's call: promote
> `cache_fetch`/`COST`/`CAP0` into `swing_bot/` and pin them, or accept it in
> writing). Section 8: 8 of 13 MEDIUM and all 14 LOW remain; GK closed 5 MEDIUM,
> not 0 as its own section 8 said.
> ~~**Calendar caveat, inherited:** `trading_calendar.holidays()` adds Juneteenth
> for every year although its own comment says NYSE closed for it only from
> 2022. QQQ has 23 real June sessions 1999-2021 that the calendar rejects, so
> `missing_sessions()` cannot see a hole on one of them. GK's "only false
> positives were ten ad-hoc closures" is true in one direction only.~~
> **FIXED 2026-09-11 (record GM):** Juneteenth is added only for `year >= 2022`;
> `prove_session_gap` is 8/8 and its new case fails against the old rule.

> **2026-09-09 ~15:00 CDT - ~~M13.2 FIXED; GJ's AUDIT CLOSED~~ M13.2 FIX
> ATTEMPTED, GJ PARTLY CLOSED (record GK; both headline claims corrected in
> GL).** The
> scheduled `daily-audit` appended **GJ** at 07:35 (34 findings: 1 CRIT / 6 HIGH
> / 13 MED / 14 LOW, including a landing-check on GI). Closed this sitting:
> **(1) CRIT — `swing_bot/prices.py` now RETRIES on a trailing-NaN last row**
> instead of accepting the first non-empty frame, so a bar Yahoo publishes and
> then revises ~~no longer arrives as a short series~~ **STILL arrives short:
> the retry never recovered it in production (09-09, 09-10; record GL)**.
> Exhaustion prints a message
> that names OUR filter rather than blaming the vendor (GH option (c) + (b)).
> Proof `scripts/prove_fetch_trailing_nan.py` **5/5 PASS**, including the
> mandatory negative (a clean frame must NOT retry).
> **(2) HIGH — mid-series gaps are now detectable at all.**
> `trading_calendar.sessions_between()` is the module's first range enumerator;
> `coverage_gate.missing_sessions()` diffs a series against it and flows through
> the existing `RUN_FAILURES` path. **Calibrated against 27 years of real data:**
> the enumerator's only false positives across QQQ's 6,918 bars were **ten
> genuine ad-hoc closures** (9/11 ×4, Reagan, Ford, Sandy ×2, G.H.W. Bush,
> Carter), now pinned in `AD_HOC_CLOSURES` — **derived from the data, not from
> memory**. Full history and the live 200-bar window both scan **0 missing**.
> Proof `scripts/prove_session_gap.py` **7/7 PASS**.
> **(3) HIGH — the V1/V3 rigor harness runs again.** `docs/trial_log.json` was 4
> preregs stale, so `load_trial_count()` raised at the unguarded
> `run_v1_harness_check.py:280`. Rebuilt: 37 → **41 trials**, N 50 → **54**, so
> DSR deflates HARDER. `HARNESS ACCEPTED`, all 5 criteria PASS.
> **(4) MED — two live-loop asymmetries.** `qty_reconcile_orders` scored a
> zero-DB-qty fork as 0.0% drift while its reporting twin called the same case
> `float("inf")`; the function that *decides orders* was blind to what the one
> that only *prints* calls the worst possible fork. And a `list_positions()`
> failure now reaches `RUN_FAILURES` instead of exiting 0 with a blind monitor.
> **(5) MED — the secret gate FAILS CLOSED.** `scripts/git-hooks/pre-commit` now
> exits 1 when the delegated gate is absent; this repo is public, holds live
> Alpaca credentials, and has no `.github/` CI backstop.
> **Tripwire is 12 refs + 22 invariants** (was 19; the three new ones pin the
> zero-qty reconcile case and the calendar enumerator). `CLAUDE.md:51` updated.
> **Three GI claims of mine were WRONG and are corrected in GK, not defended:**
> the tripwire's 12 refs are the `REFERENCES` list in `test_frozen.py` and
> **every one runs an
> engine** — I described the INVARIANTS block and labelled it REFERENCES; the
> real reason it misses the sizing artifact is **scope** (`backtest.py:20-22`).
> The census is **43 files / 4 shared-engine importers**, not 42 / 5. And the
> `run_c1_residual_reversal.py` `px()` citations were 5-7 lines off in three
> artifacts at once (actual `:135-139`, exit `:146`, entry `:149-151`).
> **GJ's "output no program emits" is half right:** GI's 4-decimal block was real
> captured output from a throwaway inline `python -c`, not composed figures — but
> unreproducible, which is the actual defect. Now emitted by
> `ablation_m10_1_entry_exit_legs.py --precision`, reproducing it exactly.

> **2026-09-08 ~00:30 CDT - OVERNIGHT DECOMPOSITION DIAGNOSTIC (record GD):
> a CITED PRIOR IN THIS PROJECT'S OWN DOCS DOES NOT REPRODUCE.** Evan asked about
> buying the close and selling the open. DIAGNOSTIC - no D1 verdict, nothing
> deployed, **attempt tally UNCHANGED**; no prereg. Runner
> `scripts/ablation_overnight_decomp.py` (NEW), results
> `docs/research/2026-09-08_overnight_intraday_decomposition.md`.
> **`execution_microstructure.md:53-55` has carried since July: the overnight
> component is "both uncapturable AND now decayed" (NY Fed, flat since 2021).
> Half of that is wrong.** UNCAPTURABLE: confirmed decisively. NOW DECAYED: does
> NOT reproduce on our data.
> **The anomaly is real and large** - first UNCONDITIONAL decomposition this repo
> has run (`ablation_fill_timing.py` only ever measured IBS<0.20 signal days).
> Annualized pp/yr, log space, total-return arm: **SPY overnight +9.60 vs
> intraday +0.75; QQQ +13.12 vs -2.78; DIA +7.12 vs +1.67; IWM +12.63 vs -4.09.**
> SPY's overnight leg compounded **24.9x** over 33.5 years, its intraday leg
> 1.29x. QQQ's and IWM's intraday legs are outright NEGATIVE over 25 years.
> **"Flat since 2021" fails the FAIR test.** Comparing a 4.6y window to a 29y
> window is not a test (the long window's SE is ~5x tighter). Against all
> overlapping windows of the SAME length in each ticker's own history, the
> current window sits at the **56.0th (SPY), 50.7th (QQQ), 45.5th (DIA), 57.3rd
> (IWM)** percentile - **at or near the MEDIAN**, three of four still above +8
> pp/yr, not one decline approaching its own CI. The post-2022 softness is ONE
> YEAR: SPY 2021 +16.18, **2022 -14.37**, 2023 +5.75, **2024 +21.38**, 2025
> +8.06, 2026 +13.31.
> **The era question was underpowered by ~40x and that is itself the finding.**
> Overnight vol ~10.6%/yr, so post-2022 (n=1,159) the 95% CI on SPY is **+-9.57
> pp/yr** against a 1-2 pp/yr effect; 2-sigma resolution needs ~200 years. Every
> era row prints its CI - a table without one would have manufactured a
> conclusion its data cannot support.
> **STILL NOT TRADEABLE, and this needs no era split.** A full round trip every
> session: breakeven per side `c*=(G-1)/(G+1)` is **SPY 1.90 / QQQ 2.60 / DIA
> 1.41 / IWM 2.51 bps**. **We price 5.** Net **-14.4 / -11.4 / -16.5 / -11.8
> pp/yr**. Even at a fantasy 1 bp/side SPY's +4.7 is BELOW its own buy-and-hold
> of 10.35. Same wall NightShares hit with real money.
> **The trap that would have INVERTED the answer:** on dividend-unadjusted
> `close` the ex-dividend drop falls ENTIRELY in the close->open window, so a
> price-only overnight leg is understated by the whole dividend yield (~183
> bps/yr on SPY) - the same order as the effect - and DIFFERENTIALLY across
> tickers (QQQ ~51). A naive price-only run would have made "the premium died"
> look supported. My first correction (`DIV = TR - PR`, added) was also WRONG,
> breaking by the cross term up to 154 bps; the shipped form is multiplicative
> and exact to one ULP, validated by a dividend cross-check against **667
> independent ex-dates** (worst 1.87e-06 vs 5e-5).
> **DISCLOSED: a result leaked during PLANNING** - a sub-agent computed SPY's
> full-history leg products while validating the identity, so the headline
> existed before the runner did. Recorded, not presented as a virgin run.
> **Consequence:** X4's stated prior (`PRD_ROADMAP.md:1026`) loses one of its two
> legs - NightShares stands, NY-Fed does not reproduce. X4 stays BLOCKED-ON-EVAN
> and BLOCKED-ON-BROKER-TIER; nothing here unblocks it. Does NOT touch the
> 54%-of-edge figure (different conditioning), E2's c2c mirage (CK closed it on
> drawdown grounds), the closed search phase, or any live sleeve.
> **Done-check:** `FROZEN TESTS: GREEN (all d=0)`; all six proofs pass; F3
> determinism - run twice, 288 lines, byte-identical. `swing.db` NEVER OPENED.

### Dated history, condensed 2026-09-11

Evan authorized the trim 2026-09-11. Each line below is a removed block's own
headline, newest first; the record appendix it names holds the full account,
and the verbatim block is `git show 7de78f3:HANDOFF.md`. The file was 1,490
lines; `/docs-sync` wants the live snapshot small enough to read first.

**Carried forward** - every OPEN/BLOCKED line inside a removed block was checked:

- **Still open:** `.claude/secrets-inventory.md` has never existed here; the
  scanners run on built-in rules, and writing the inventory is Evan's security
  decision (record FV; also in `PRD_ROADMAP.md`).
- **Stale, not carried:** the FH block said its credential-death and
  missing-price findings were "still open"; record FN found both already fixed.
  M13.2's OPEN status and the 09-04 NAV check are superseded by the GL block
  above (`paper_nav` does end at 2026-09-04, so that row landed).

- 2026-09-06 ~13:40 CDT - FX's SIX REMAINING findings CLOSED (record GA), but its own prescribed fix was a NO-OP and three of its corrections were wrong.
- 2026-09-06 ~00:21 CDT - M13 IS CLOSED: 4/6/7 DONE, 5 closed with no action (records FV, FW).
- 2026-09-05 ~23:25 CDT - M13.3 DONE (record FT): the fidelity instrument now reports its own dark half every run, and the honest denominator is 4, not 5.
- 2026-09-05 ~22:55 CDT - M13.2 INSTRUMENTED but NOT ANSWERED (record FS); commit `2d1cfa1` holds M13.1 and is NOT PUSHED.
- 2026-09-05 ~20:40 CDT - M13.1 DONE (record FQ): the live loop has a SECOND CLOCK and refuses when the feed lags it.
- 2026-09-05 ~19:30 CDT - DRIFT CHECK (record FP). CRIT, NEW: the live loop has been processing YESTERDAY's session since 2026-09-02.
- 2026-09-05 ~18:20 CDT - F3 REDIRECT EXECUTED across all 8 ETF experiments (record FN; results `docs/research/2026-09-05_F3_liquidity_floor_etf_results.md`; prereg `6a23a9a` + amendment `2f0a8a4`, both doc-only and both before any runner code).
- 2026-09-05 ~18:25 CDT - GRAPH RE-INDEXED (record FO): 1,728 nodes / 2,876 edges / 186 communities / 9 hyperedges, health check clean.
- 2026-09-05 - DAILY-AUDIT FIX PASS, committed `87db1c2`, since PUSHED (records FK, FL, FM). The commit needed `--no-verify` on Evan's explicit call:
- 2026-09-01 - record FJ: THE LIVE LEDGER WAS CONTAMINATED and e6_1x recorded NOTHING for five sessions. Every guard fired correctly; nobody was listening.
- 2026-08-25 - record FI: the 2026-08-20 audit (FH) never reached git
- 2026-08-20 - record FH: 7-finding scheduled daily-audit, NOTHING FIXED at the time.
- 2026-08-03 — X9 pairs / relative-value = FAIL; attempt #37 (record DP; results `docs/research/2026-08-03_X9_pairs_results.md`).
- 2026-08-02 — X8 non-equity trend sleeve = FAIL both arms; decorrelation attempt deployed NOTHING (record DO; results `docs/research/2026-08-02_X8_noneq_trend_results.md`).
- 2026-07-28 — FULL AUDIT (`/audit`) + 5 fixes landed (records DH, DI; commits `1078693`, `6c9b161`, + this session).
- 2026-07-15 — X7 HYG:IEF credit gate = FAIL, but the FIRST gate to beat the 200-DMA in-window (record Appendix CV; results `docs/research/2026-07-15_X7_credit_gate_results.md`).
- 2026-07-15 — M3 rewired to 3-account model; all 3 Alpaca paper accounts VERIFIED CONNECTED (record Appendix CQ).
- 2026-07-15 — M3 forward-paper infrastructure BUILT; BLOCKED-ON-EVAN for Alpaca keys (record Appendix CP).
- 2026-07-14 — M11 chart-pattern detection = FAIL (signal-dead); 9th family closed; survivor bias DESTROYS the pattern edge (record Appendices CL–CO).
- 2026-07-14 — FINALIZED THROUGH M10; research OPEN, not done; new direction = M11 algorithmic chart patterns (record Appendix CL).
- 2026-07-14 — M10 synthesis arc: Nagel Switch = the program's FIRST PASS-HR, but IN-SAMPLE-COMPOSED / forward-paper-only (record Appendices CG–CI).
- 2026-07-14 — M10-2 gap-amortized stress IBS = FAIL; closes the E2 "c2c mirage" (record Appendix CK).
- 2026-07-14 — X6 crypto pilot = FAIL; E6's lesson generalizes to crypto (record Appendix CF).
- 2026-07-14 — FREE SWEEP COMPLETE: M8 (C1–C7) + X3 all done; program at 30 attempts (record Appendices CB–CD).
- 2026-07-13 — CAPSTONE written; X1 = FAIL; X3 interrupted (record Appendices BX–BZ).
- 2026-07-13 — X2b short-side = FAIL; X2's "strongest anomaly" was a frictionless mirage (record Appendix BW).
- 2026-07-13 — X2 days-to-cover = FAIL (deployable), short-interest anomaly real short-side but does NOT survive honest costs (see X2b above; record Appendix BU).
- 2026-07-13 — EX-DECOMP (M9 #44) done: closed FAILs decomposed (record Appendix BS).
- 2026-07-13 — E19 insider-buy drift = FAIL (clean); M7b CLOSED (record Appendix BR).
- 2026-07-12 — E19 ingestion RUNNING + full method survey delivered (record Appendices BI–BK).
- 2026-07-11 — M7b data-type arc done (record Appendices BD–BF); autonomous wall.
- 2026-07-11 — M7 catalog arc E13–E17 all closed (record Appendices AX–BC); D1 dual-bar verdict adopted (Appendix AW).
- 2026-07-10 — E10/E11/E12 all FAIL; article-set arc closed (record Appendices AO–AP).
- 2026-07-10 — E8 + E9 both FAIL; families four and five closed (record Appendices AL–AM).
- 2026-07-10 — E3 stock momentum FAIL; third family closed (record Appendix AI).
- 2026-07-10 — Program closed + packaged (record Appendices AF-AG).
- 2026-07-09 — C1 + three screens (record Appendices W–Y).
- 2026-07-09 — E2 = FAIL; IBS FAMILY SHELVED (record Appendices S-U).
- 2026-07-09 — E1b OOS test = FAIL (near-miss) (record Appendix Q).
- 2026-07-09 — E1 = FAIL (record Appendices N-P).
- 2026-07-09 — M0.4 executed (record Appendix H).
- 2026-07-08 — M0.3 executed (record Appendix G).
- 2026-07-08 — M0.2 executed (record Appendix F).
- 2026-07-08 — M0.1 (record Appendix E).

> **2026-09-11 note: the counts in this block stop at 2026-09-05.** Since then
> `paper_nav` gained the 2026-09-04 row on all three sleeves and then went DARK:
> no row for 09-08, 09-09 or 09-10 (record GL). Not re-counted here.
>
> **M3 forward paper — RUNNING, 36 sessions (2026-07-15 → 2026-09-03), 103 NAV rows,
> and the hole count is NOT one.** (Through 2026-08-18 it was 24 sessions / 72 rows,
> which is what the sentence below was written against.) **Holes as of 2026-09-05:
> 2026-07-30 (all three sleeves, record EI) PLUS five e6_1x-only holes — 2026-08-25,
> 08-26, 08-27, 08-28 and 08-31 (record FJ).** e6_1x therefore has 31 NAV marks where
> its peers have 36, so any cross-sleeve return or NAV comparison is running on
> UNEQUAL series until that is resolved. The five are **neither backfilled nor
> acknowledged** — BLOCKED-ON-EVAN, see below. The missed-session detector could not
> see them: it compared `SELECT DISTINCT date`, so a date counted as covered when any
> ONE sleeve wrote it. Fixed per-sleeve 2026-09-05 (finding 2).
>
> (This line has now been wrong FOUR separate ways, so its history stays visible. It once said "13 sessions, 27 NAV rows, no gaps" —
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
> three sleeves currently long QQQ (e6_1x re-entered 2026-09-01 after the five-session
> stall). Latest marks (**2026-09-03**, read-only 2026-09-05): **e6_1x $1,007.96 ·
> e18_vixts $1,001.66 · m10_1_nagel $1,021.94** (09-02 was $996.12 / $989.89 /
> $1,009.94). The 2026-08-18 marks this line used to carry were $1,007.74 / $1,001.44 /
> $1,021.72.
> (each started at $1,000). Task now runs S4U — fires with nobody logged on. Scheduled task
> `SwingTradingDailyPaper` fires 7pm weekdays via `scripts/daily_swing_paper.bat --execute`;
> logs to `var/daily_swing_paper.log`. **Do NOT fire it manually intraday** — that is what
> caused the 07-20 round-trip and the e18 fork; the guard now blocks order submission while
> the market is open, but the DB ledger still advances on any run.

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
| Live paper | M3 | **RUNNING since 2026-07-15** | 3 sleeves (e6_1x / e18_vixts / m10_1_nagel), one $1,000 Alpaca paper account each; 36 sessions (2026-07-15 → 2026-09-03), task S4U green. Said "20 sessions" while :140 six lines earlier said 24 and the DB agreed with 24 — corrected 2026-09-05, finding 6. Row said BLOCKED for 4 weeks after deploy — corrected 2026-08-13, record EO |
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
- Trading's own `HANDOFF.md` / `.claude/project-memory/` are ground truth for
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
  (`daily_swing_paper.py:67` → `run_e10_earnings_drift:27`; `:68` →
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
- ~~**RUN V3?**~~ **RUN 2026-08-19, record Appendix FC** (~line 7763 at 2026-09-06; search the
heading, the number moves +1 per append) - V3 IMPLEMENTED and ACCEPTED, but its repair is UNDEMONSTRATED.** `docs/prereg_v3_pbo_scoping.md` was committed doc-only
  (`6194847`, 2026-08-13, record ET) BEFORE any code moved. It scopes PBO to config
  sets where selection is real: sets are declared `SELECTION` or `EXCHANGEABLE`
  at the call site, PBO gates only the former. No threshold moves. Running it
  means editing `swing_bot/validation.py` + `scripts/run_v1_harness_check.py`
  and re-running the harness. Both edits landed 2026-08-19; thresholds did NOT
  move (`DSR_ALPHA = 0.05`, `PBO_FAIL_AT = 0.5` in
  `scripts/run_v1_harness_check.py`). The pre-committed failure condition -- if
  pure noise is ACCEPTED under V3, V3 FAILS and reverts in full -- did NOT fire.
  **FC.5's nuance, preserved:** the false positive V3 was written to remove did
  not reproduce. Planted-edge PBO came out 0.486 under V3 against 0.514 under
  V2, and V2's rule would not have rejected it either, so V3 is accepted on its
  reasoning and NOT on a demonstrated repair. (This bullet sat under
  BLOCKED-ON-EVAN for 17 days after the work was finished -- the third stale
  BLOCKED row this project has carried; see record EO for the first. Struck
  2026-09-05, finding 5.)
- ~~**Audit #4 F14**~~ **EXECUTED 2026-08-19, record FC.** `UPDATE paper_sleeves SET cash=round(cash,9)` to clear a
  floating-point residue. **THREE rows, not one** — re-derived 2026-08-18 (record
  EY): `e6_1x −1.1368683772161603e-13`, `e18_vixts` and `m10_1_nagel` both
  **+1.1368683772161603e-13**. Every prior statement of this item said "one-row";
  the statement was wrong, the un-`WHERE`d UPDATE was always the right scope. A
  write to the live paper ledger, so it was Evan's call and he made it. Verified
  read-only 2026-09-05: `paper_sleeves.cash` is `0.0` for all three sleeves,
  no e-13 residue. (Struck 2026-09-05, finding 5.)
- ~~**F2/F3 preregs**~~ **F2 CLOSED 2026-08-19 (record FD)** — E5/E7 now
  implement E6's convention; no verdict moved. **F3 STILL OPEN, and its scope is
  INVERTED (record FG):** the floor provably NEVER fires on the 39-name stock
  universe (0 of 260,363 ticker-sessions), while the 29-ETF universe breaches it
  on 16.07% (26 of 29 names). Re-running the stock experiments would install a
  guard that cannot fire — this project's signature defect, a fifth time.
  ~~Awaiting Evan's redirect.~~ **F3 REDIRECTED and EXECUTED 2026-09-05 (record
  FN): the floor now runs in E1/E8/E9/E11/E12/C3/E20/X9; no verdict flipped to
  PASS, E11 went INCONCLUSIVE on sample size, C3's drawdown halved. Struck
  2026-09-05.** Original wording follows: the 200-DMA convention split (7 inclusive / 6 exclusive;
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
  for what to build and in what order. ~~**M13.2 is OPEN**~~ ~~**M13.2 is CLOSED
  2026-09-09 (records GH, GK) — answered and fixed.**~~ **M13.2 is still
  OPEN (2026-09-10, record GL): root cause answered (GH), fix attempted (GK)
  and it did NOT unblock the 09-09 or 09-10 runs.** (was: root-cause the feed
  lag; blocked on a trading day, earliest Tue 2026-09-08) — see the M13 block at
  the top of this file and PRD M13 task 2. Apart from it, no unstarted task
  remains and M3 forward paper needs elapsed time, not a task. (This line read
  "next open task = M0.1" until 2026-08-13; M0.1 shipped 2026-07-08. It then
  read "no unstarted task remains" while the top of this same file said M13.2
  was open — corrected 2026-09-06, audit FX.)
- `docs/research/` — evidence brief, experiment-ideas list (+ council
  outcome pointer), future power calc / ablation docs.
- `.claude/project-memory/` — binned technical memory (INDEX + 13 bins; was
  11 before M13.7 added `DIRECTORY.md` and `disclosure.md`).
- `graphify-out/` — the knowledge graph (`/graphify` queries it). **2,070 nodes /
  3,142 edges / 229 communities / 30 hyperedges as of 2026-09-08** (full rebuild,
  5 semantic chunks; was 1,728 / 2,876 / 186 / 9 at record FO and 1665 / 2886 /
  184 / 12 at record ET). **The hyperedge-loss warning below did NOT bite on that
  rebuild** — it went through `to_json`, not `build_merge`, and hyperedges rose
  9 → 30. **The project record IS now
  indexed** — its TOC is the highest-degree node at 169 edges. **`build_merge`
  REPLACES hyperedges instead of unioning them** (bit twice: wave 2, and FO);
  back up `graph.json` before any `--update` and compare hyperedge counts after.
  Four hyperedges lost in FO, recoverable from `git show
  30a5bfa:graphify-out/graph.json`. **Treat the graph as navigation, never as a
  citation** — it is LLM-built and has shipped at least one false fact (record
  EQ). The record and the code are ground truth.
- `docs/research/2026-09-05_F3_liquidity_floor_etf_results.md` — the F3 A/B
  across eight ETF experiments, with the falsified predictions recorded as
  written.
- `docs/prereg_f3_liquidity_floor_etf_scope.md` + `docs/prereg_f3_amendment_cache_vintage.md`
  — F3's prereg and its vintage amendment, both doc-only commits.
- `.claude/pm-cadence.json` — record entry every 3 prompts;
  handoff/PRD/bins event-driven.

## Handoff prompt (paste into the next session)

```
Swing Trading, fresh session. Read in order: CLAUDE.md ->
.claude/project-memory/important.md -> HANDOFF.md (top block = record GU) ->
record Appendices GT, GU -> PRD_ROADMAP.md M13. The append-only record is
ground truth.

STATE (2026-10-04): search phase closed at 37 attempts. M3 forward paper is the
only lever. The loop runs at 23:45 CT Mon-Fri and has marked NAV every session
since 2026-09-23 (the first 23:45 run, 09-22, still hit the vendor NaN and
refused; 09-22 was then backfilled, record GU). 30 paper_nav rows (09-08..09-22)
are backfilled and must be excluded from any uptime figure. HEAD = 5dde35a;
the GU work (everything except the record files) was authorized for commit
but staging was denied (record GV) - check `git status` and the git log.

FIRST THING: read the end of var/daily_swing_paper.log for the Mon 2026-10-05
23:45 run. Expect `exit code 0` and no `REFUSING TO RUN -- price feed is
BEHIND`. Never run the loop (scripts/daily_swing_paper.py or any .bat) to check.

BLOCKED-ON-EVAN -- ask, never work around:
  1. Record Appendix GJ holds Evan's personal email (one line in the .md, one in
     the .html). Relaunch with PM_RECORD_UNLOCK=1, replace it with [redacted],
     re-render, confirm 0 case-insensitive hits in both; only then commit the
     record files (they were deliberately left out of the GU commit).
  2. The live M10-1 stress basket cannot form (FF3 ends ~a month back). Any fix
     that makes it form changes the rule and needs a prereg.
  3. GJ section 4 HIGH: run_e8_squeeze.py has zero tripwire coverage.
  4. Open from audit GT: coverage-gate ad-hoc-closure path (MED 7), CPCV purge
     (MED 10), doc counts (MED 11), pip-audit (MED 12), and the LOWs.

HARD CONSTRAINTS: swing.db mode=ro unless you are the writer. test_frozen must
print FROZEN TESTS: GREEN (all d=0) -- 12 refs + 22 invariants -- after any
change to swing_bot/ or scripts/daily_swing_paper.py. Append the record only via
append-record-entry.js and re-render the HTML twin after. Run `date` before any
timestamp. Commit only when Evan authorizes; publishing is Evan's alone; no
Co-Authored-By line.
```
