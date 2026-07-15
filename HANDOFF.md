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

## Current state — 34 attempts / 0 clean PASS-HR / 1 in-sample PASS-HR (M10-1) + 1 weak PASS-RA (E18); M11 chart-patterns = FAIL; M3 forward paper = the open lever; nothing live

**Last updated: 2026-07-14 (CST)** — this file is the only live snapshot;
history lives in the record. **Timezone: record/doc stamps are CST (UTC-5);
the cadence hook reports UTC — subtract 5h (record Appendix AZ).**

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
| Live paper | M3 | **BLOCKED — Evan go + Alpaca acct** | E6 (1×) the only candidate, market-dependent risk-mgmt; deploy is Evan's call |
| Program write-up + packaging | M6 | **Done** | Findings doc updated to E1→E7; `README.md` added; git tag |
| Live paper: control + LLM-veto sleeves | M3 | **BLOCKED — gate not open** | E1 did NOT pass M2→M3; needs a new pre-registered strategy that passes + Evan go + Alpaca account |
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
- **Alpaca PAPER account** (PRD M3.15): which of ~3 paper accounts — only
  relevant once a strategy passes and live is authorized.
- **M2.12 survivorship bound**: deferred as moot for failed ETF-only E1; run
  only if a stock strategy enters scope.

## Documentation
- `docs/Project Record — Full Chronological History.md` — append-only
  chronological record; the ground truth. No HTML twin yet.
- `PRD_ROADMAP.md` — the standing plan (written 2026-07-08). Source of truth
  for what to build and in what order; next open task = M0.1.
- `docs/research/` — evidence brief, experiment-ideas list (+ council
  outcome pointer), future power calc / ablation docs.
- `.claude/codebase-memory/` — binned technical memory (INDEX + 6 bins).
- `.claude/pm-cadence.json` — record entry every 3 prompts;
  handoff/PRD/bins event-driven.
