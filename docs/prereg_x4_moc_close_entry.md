# Pre-registration — X4: market-on-close entry probe → forward-paper arm

**Written 2026-09-08, ~23:02 CDT. Committed DOC-ONLY before any runner code.**
PRD_ROADMAP task 48 (X4), open since 2026-07-13 with no pre-registration — 44
`prereg_*.md` exist covering X1/X2/X2b/X3/X6/X7/X8/X9, and there has never been
an X4. Written against `docs/prereg_TEMPLATE.md`, in the numbered form of
`prereg_f3_liquidity_floor_etf_scope.md` because X4 is an execution experiment
(probe → forward arm), not a historical backtest. **X4 is BLOCKED THREE WAYS and
this document does not unblock any of them** (§2, §3).

## 0. Why this exists, and why it is written NOW rather than earlier

X4 is the last honest execution experiment this project has: every strategy here
signs at the close and buys the next open, forfeiting the overnight leg that
record GD measured as the entire source of index return. A market-on-close entry
is the only fill positioned to capture it.

**It is written today, and not earlier, because the prior changed twice this
week and writing it sooner would have pre-registered a prior that is now known
to be wrong in part.** Record GD (2026-09-08) removed one of X4's two stated
reasons. Record GF (2026-09-08) then measured the size of the prize and found it
both larger and narrower than recorded. A prereg written before those would have
fixed a prior that the evidence has since moved. §1 states the rebuilt prior; §7
discloses what is weak about writing it in the same session as GF.

## 1. The prior, rebuilt — four legs, one of them REMOVED

**Prior: FAIL — the kill is confirmed, on better evidence than it used to rest
on.** The four legs, stated separately so a future reader can see which one moved:

1. **NightShares — STANDS.** The NSPY/NIWM ETFs implemented exactly this trade
   (buy close, sell open) and returned **−6.9% / −10%+ against +22% / +16%
   benchmarks**, liquidating in ~14 months on "transaction costs of turning the
   portfolio over twice a day." A real-money implementation of the mechanism
   failed in public.
2. **NY-Fed "flat since 2021" — REMOVED.** Record GD: an unconditional
   decomposition of SPY/QQQ/DIA/IWM puts the post-2021 overnight leg at the
   **45th–57th percentile** of each ticker's own matched-length window history —
   at or near the median, every decline well inside its own 95% CI. This does not
   falsify the NY-Fed paper (its index, window, and price-vs-total-return basis
   are all unrecorded here); it falsifies the confidence with which this project
   carried the sentence since 2026-07-13. **This leg is withdrawn from the prior.**
3. **Cost — STANDS, and is now the sharpest leg.** Record GD: breakeven on an
   overnight-only trade is **1.4–2.6 bps/side** against the **5 bps/side** this
   project prices, so it **loses 11–17 pp/yr in every era**. Holding N days
   amortises the round trip but `net(N) = buy_and_hold − (ID + 25.2)/N`
   converges from BELOW and never crosses.
4. **NEW (record GF), and it cuts BOTH ways.** The entry leg is real and much
   larger than the number always used to measure it: on C1, **entry timing
   +6.61 pp/yr against a +1.38 pp close-to-close gap — 4.8x.** A c2c ablation
   moves the entry and exit fills together, so it reports the net and hides the
   entry term. **But the prize is era-confined and reverses out of sample:** C1
   secondary window 2014–, 0 bps, as-run 8.88% → entry-fixed **7.95%**; at the
   real 5 bps/side, 3.42%/DD 38.7% → **2.54%/DD 52.0%** — worse return and a
   drawdown 13 pp deeper. The favourable era is 2000–2013, the survivorship-
   flattered window **C1's own prereg declared UNINTERPRETABLE**.

**Net: the expected OUTCOME is unchanged from the PRD's original "confirms the
kill". Two of its stated REASONS have changed — one removed, one added — and the
added one is the strongest argument yet that the prize is not where it looks.**

## 2. Step 1 — the broker probe, with PRE-COMMITTED decision rules

**BLOCKED-ON-EVAN: this step requires submitting a real order (paper money) on
Evan's Alpaca account. It will not be submitted unasked.**

The repo contradicts itself about CLS availability, inside one document:
`docs/research/2026-07-13_execution_microstructure.md:70` — "Alpaca supports
CLS"; `:103` — "no auctions (OPG/CLS = Elite Smart Router only)"; `:145` — the
upgrade path is "whole-share + Elite Smart Router". **`:103` sits in a paragraph
about FRACTIONAL orders**, so the two may not actually conflict: the constraint
may be that auctions are barred for fractional quantities specifically. That is a
hypothesis, not a finding.

**Decision rules, fixed here before any answer is seen** — because an ambiguous
broker response is exactly the kind of thing that gets read to suit:

- **AVAILABLE** — a CLS (or LOC) order for a **whole-share** quantity is
  ACCEPTED on the live paper account and appears in the order book with the
  auction TIF intact. Step 2 becomes reachable (still gated by §3's rule
  conflict).
- **FRACTIONAL-BARRED** — accepted whole-share, rejected fractional. Recorded as
  its own outcome, **not** as AVAILABLE. At $100–1,000 per sleeve, whole-share-
  only sizing materially changes the tradeable universe, which is a **scope
  change requiring its own dated decision** before step 2 is designed.
- **BLOCKED-ON-BROKER-TIER** — rejected for both. **X4 closes.** A rejection
  citing Elite Smart Router, account tier, or entitlement counts as BLOCKED, not
  as "retry later".
- **No amount of documentation reading substitutes for the live submission.**
  Vendor docs have already proved wrong here once (the fractional order-type
  correction at `:100-103`). The probe is a submission or it is nothing.

**Per the repo convention (record: "per PRD, no prereg — the probe gates it"),
step 1 issues no D1 verdict.** It is pre-registered here only for its decision
rules.

## 3. Step 2 — the forward-paper arm, gated

**BLOCKED BY THE EOD-ONLY HARD RULE. This is a RULE CONFLICT, not a gap, and it
is Evan's to rule on.** `CLAUDE.md` states: *"EOD data only: signal at close,
execute next open. No intraday logic until an intraday data source exists."*
Step 2 requires a signal derived from a **frozen 15:50 ET snapshot** — using the
16:00 close to justify a 15:50 order is look-ahead — and that is intraday logic.
**Step 2 does not start until the rule is ruled on. It is not worked around.**

Rules fixed a priori, should it ever run:

- **Two arms, identical signals.** The MOC arm and the next-open control arm
  sign from the *same* frozen 15:50 snapshot on the same sleeve, same universe,
  same K. Only the fill differs. If the arms ever diverge in signal rather than
  fill, the run is VOID (§5).
- **The 15:50→16:00 stub is measured as a residual and REPORTED SEPARATELY.** It
  is never netted into the arm's return. It is the size of the look-ahead the
  design is avoiding, and it must be visible.
- **Costs [STANDING tiered]:** 5 bps/side single stocks, 1 bp/side broad-index
  ETFs, **15 bps/side stress leg reported alongside** the headline. Any auction
  slippage observed beyond the modelled cost is reported as a correction to the
  model (§5), never absorbed.
- **Minimum sample, declared before any comparison is read: ≥ 30 MOC fills**,
  matching the house entry floor. Below that the comparison is **INCONCLUSIVE**
  and is not reported as a direction. *(Note honestly: if X4 is arm-mounted on a
  VIX-gated stress branch, 30 fills may take years. That is itself evidence about
  whether X4 is worth unblocking.)*

## 4. Verdict framing and the forward-only cap [STANDING]

- **Modified-window cap applies.** Step 2 is forward paper on a sample that
  cannot cover 2000–2013, so per `prereg_TEMPLATE.md` the **best achievable
  verdict is "PROMISING — needs forward confirmation". PASS-HR and PASS-RA are
  UNREACHABLE by this design.** No live authorization can follow from X4 alone.
- Where the standard bars apply they are unchanged: CAGR ≥ **15%**, maxDD ≤
  **60%**, Sharpe ≥ **0.80**, entry floor **≥ 30** else INCONCLUSIVE.
- **The primary comparison is MOC arm vs the next-open control on identical
  signals** — not against SPY, not against the recorded backtest. X4 asks an
  execution question, and only the paired contrast answers it.
- **No parameter changes after results; a FAIL is never re-tuned into a pass.**

## 5. Pre-committed failure conditions — the asymmetry, handled

The prior is FAIL. A favourable execution result on a short forward sample is
exactly what a lucky sample looks like, so:

- **If the MOC arm beats the control, that is NOT a PASS and is NOT banked.** It
  is recorded as PROMISING-pending-sample and requires the declared ≥30 fills
  before any direction is read at all. A favourable result below the floor is
  reported as INCONCLUSIVE, with the direction stated but explicitly not claimed.
- **If the 15:50→16:00 stub accounts for a material share of the arm's
  advantage, the result is reported as STUB-DRIVEN, not entry-driven.** The stub
  is the look-ahead the design exists to exclude; an advantage that lives there
  is an artifact of the measurement, not an execution edge.
- **If observed CLS fills show auction slippage beyond the modelled 5 bps, the
  MODEL is declared wrong and re-stated** — the result is not adjusted to fit it.
- **If the two arms ever sign differently, the run is VOID for those sessions**
  and they are excluded and counted, not silently dropped.
- **If step 1 returns BLOCKED-ON-BROKER-TIER, X4 closes as BLOCKED** and this
  prereg is marked spent. It is not re-scoped into a different experiment to
  salvage the work.

## 6. Reporting

Step 1 reports: the exact order submitted, the exact broker response, and which
of the three §2 outcomes it maps to — verbatim, not paraphrased. Step 2, if
reached, reports per session: signal set, MOC fill price vs official close, the
control's next-open fill, the 15:50→16:00 stub, and realized cost per side; then
the paired arm comparison with the fill count. Results land in
`docs/research/<date>_X4_moc_close_entry_results.md` and a record entry.

## 7. Disclosed weaknesses of this pre-registration

- **Same-session authorship.** This is written in the same session as record GF,
  whose numbers form leg 4 of §1 — the weakness `prereg_f3_liquidity_floor_etf_
  scope.md:§6` disclosed about itself. The protection here is §5's pre-committed
  handling of a favourable result, not temporal separation from the author.
- **The number motivating X4 does not transfer to X4.** The +6.61 pp entry leg
  is from **C1's backtest**, on a **survivor universe**, in a window C1's own
  prereg called uninterpretable — and record GF further showed the per-fill
  overnight legs at entry (+7.20 bps) and exit (+6.93 bps) are statistically
  indistinguishable, so the mechanism behind the CAGR asymmetry is **unexplained**.
  X4 is a forward test on a live sleeve. The prize estimate is an upper bound on
  a different thing.
- **The live sleeve's split IS measured, and it argues against X4.** *(This
  bullet read "UNMEASURED" until 2026-09-09. It was written 23:03:37 on
  2026-09-08 and the measurement landed 23:08:26 — stale within five minutes.
  Audit GJ §7 caught it; corrected here rather than left standing.)* The
  `22.82% → 17.87%` pair belongs to **M10-1**, not C1 (record GF §1), and it is
  not even a timing delta: 22.82% is Rung A at 0 bps and 17.87% is Rung C at
  5 bps, so the quoted 4.94 pp is **2.04 pp timing + 2.90 pp cost** — the
  runner's own Rung B (next-open, 0 bps) = 20.77% is skipped by the caveat.
  The timing half is **stocks-only**: `run_m10_1_nagel_switch.py:157` labels it
  "A (c2c stocks 0bps)" and the QQQ legs read `qo[d]` directly at `:101`/`:112`,
  so the `c2c` flag never reaches the branch that holds most of the calendar.
  **Measured entry term: +4.70 pp/yr against a +1.93 pp net c2c gap** (record
  GI, `docs/research/2026-09-08_M10-1_entry_exit_leg_split.md`) — the same
  masking shape C1 showed at 4.8×. **And at the real cost model an MOC entry
  takes M10-1's secondary window to 14.63% CAGR against the ≥15% bar, with
  drawdown 39.7% → 50.6% — converting the program's only PASS-HR into a FAIL.**
  So the sleeve X4 would be mounted on gets *worse* out of sample when its
  entry is fixed. That is now part of this prereg's prior, not a later surprise.
- **X4 may never run.** Pre-registering a triple-blocked experiment risks this
  document going stale before it is used. That is accepted: the alternative is
  writing it after the blocks lift, when the prior would be written in sight of
  the broker answer.
