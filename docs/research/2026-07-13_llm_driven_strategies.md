# Research brief — LLM-driven swing-trading strategies (exhaustive ideation + skeptical evidence survey)

**Swing Trading project · 2026-07-13 (CST) · Evan Daruwalla**

**Question this answers:** what is the *full* design space of ways an LLM can
make human-like swing-trading decisions "biased off stock trends" — as an
analyst, an agent, a chart/trend reader, an overlay/meta-labeler, a feature/
factor generator, or a macro/regime interpreter — including paths that require
wiring Claude to a live trading platform or spending more compute? For each:
what is the mechanism, how good is the *evidence* (graded skeptically for
look-ahead/contamination), what data/infra/compute does it need, and is it
testable under this project's constraints (EOD next-open, $100–1,000, K=1–3,
liquidity floor, 5 bps/side, pre-registration, frozen tripwire, and the
existing `e1_control` vs `e1_llm_veto` overlay design)?

**Decision it feeds:** whether any LLM path is worth pre-registering as a new
experiment, and if so which one first and on what infra tier.

**Audience:** the operator (Evan) + any future model executing the PRD. Also a
portfolio artifact — the reasoning trail and the skepticism are deliverables,
so contaminated/hyped ideas are catalogued and graded, not hidden.

---

## TL;DR (verdict first)

**Working hypothesis H1** — "an LLM can make human-like trend decisions that
earn a real, tradable swing edge here" — **is rejected in its strong
(high-return, standalone-engine) form, and survives only in a weak
(risk-adjusted overlay, provable only at a pre-registered readout) form.** The
**null H0** — "published LLM-trading alpha is dominated by look-ahead/
training-cutoff contamination, and the legitimate residual is a thin, decaying,
illiquid-concentrated signal best used as a *treatment overlay measured against
a mechanical control*, not a money engine" — **survives every family.**

Four load-bearing findings:

1. **The literature's headline returns are mostly contaminated, not real.**
   When the multi-agent showcases (FinMem, TradingAgents, FinAgent, FinCon,
   QuantAgent) are re-tested on strictly *post-training-cutoff* windows,
   returns decay **50–72%** and most **fail to beat buy-and-hold** ("Profit
   Mirage" 2025; StockBench 2026, where the best model beat a +0.4% passive
   book by only +1.9% over four months). An LLM scoring a 2019 headline can
   *recall* what happened next (Sarkar-Vafa: Llama-2 volunteers "COVID-19" for
   Sept-2019 earnings calls >25% of the time; Levy JAR 2026: for earnings
   prediction *all* apparent skill can be contamination).

2. **LLMs are demonstrably weak at the thing Evan asked for — reading price
   trends.** Frontier vision-LLMs score **49–53%** on candlestick direction
   (≈ chance); the best time-series foundation models (Chronos/TimesFM/Moirai/
   TimeGPT) beat a random walk in only **2 of 10** return tasks with "small and
   sparse" gains. This collides head-on with the project's own
   chart-TA-dies-on-cost-and-snooping prior — asking an LLM to read a chart
   adds model bias on top of a dead signal.

3. **The genuine residual edge is real but small, decaying, and lives where
   this project can't trade.** The most careful positive result (Lopez-Lira &
   Tang, post-cutoff news reaction) concentrates in **small-cap and
   negative-news** names — exactly what the mandatory liquidity floor excludes
   — and its authors report the edge **decays as LLM adoption rises** and
   collapses from ~350% to ~50% between 10 and 25 bps of cost.

4. **Non-determinism structurally conflicts with the frozen tripwire — and
   there is exactly one clean resolution.** Even at temperature 0, LLM outputs
   drift (30–50% decision-flip rate on repeat); you *cannot* pin a
   d=±0.0000pp reference on a live model. The only compatible architecture is
   the one the project already half-built: **log the LLM's decisions once to an
   immutable `overlay_log`, freeze the log, and pin the tripwire on the
   deterministic backtest that replays it** — never on the model call.

**So the honest recommendation is not "build an LLM trader," it is "run the
LLM as a pre-registered *treatment overlay* on top of a mechanical control,
under strict point-in-time discipline, on the cheapest infra tier (0/1, no API
key needed), expecting at best a risk-adjusted improvement you can only claim
at the pre-registered decision-N."** That is precisely what the existing
`e1_llm_veto` design is — this brief tells you which specific overlay to
pre-register first and how to keep it legitimate.

---

## Method (stage-4 design + limitations)

- **Design:** 7 parallel desk-research agents, one per family (analyst /
  agentic / price-trend / overlay / feature-factor / macro-regime / pitfalls-
  infra), each instructed to *generate many named idea variants* AND grade
  each idea's evidence on a 5-tier scale (**[PR]** peer-reviewed / **[WP]**
  working paper / **[V]** vendor / **[F]** folklore / **[NOVEL]** no direct
  study), report data/infra/compute needs, and issue a testability verdict
  against the project constraints. **~90 idea variants** were produced. Sources
  favor arXiv/SSRN/journals; every source dated.
- **Reconciliation layer:** a 7th agent produced the credibility anchor — the
  look-ahead/reproducibility/cost evidence and the concrete infra ladder — used
  to discount the other six families' hype.
- **Limitations:** (1) desk research — **no backtests were run** producing this
  brief; every testability verdict is a scoping judgment. (2) Several 2026
  arXiv preprints were relayed from abstracts/search, not full-text — flagged
  inline as unverified where so. (3) The field is young and publication-biased;
  positive results are systematically over-represented, which is *itself* a
  finding (>70% of published LLM-trading results fail to replicate). (4) This
  brief cannot resolve whether a *forward-live* test would pay off — only a
  real post-cutoff paper run can, which is scoped below as the honest next step.

---

## Hypotheses (stated before collection)

- **H1 (working):** an LLM reading news/filings/trends produces a directional
  or overlay signal with a real net-of-cost swing edge on liquid names.
- **H1′ (weak form):** an LLM overlay improves a mechanical base signal's
  *risk-adjusted* outcome (precision / drawdown), provable at a pre-registered N.
- **H0 (null/rival):** apparent LLM edge is dominated by look-ahead
  contamination + illiquid-name concentration; on a clean post-cutoff, liquid,
  cost-charged test the standalone edge is ~zero, and the only defensible use is
  a treatment-vs-control overlay.
- **Falsifier fixed in advance:** a pre-registered, strictly-post-cutoff,
  liquidity-floored, cost-charged test in which an LLM overlay beats its
  mechanical control at the decision-N would support H1′; failure supports H0.

Verdict after collection: **H1 dies, H0 survives, H1′ is the only live thread.**

---

## The idea catalog (7 families, ~90 variants)

Evidence tags: **[PR]** peer-reviewed · **[WP]** working paper · **[V]** vendor
· **[F]** folklore · **[NOVEL]** no direct study. Testability: **IN-SCOPE-NOW**
· **OVERLAY-EXT** (extends `e1_llm_veto`) · **DECOUPLED-OFFLINE** (LLM out of
the live loop — best tripwire fit) · **NEEDS-PLATFORM** (live feed) ·
**NEEDS-COMPUTE** · **OUT-OF-SCOPE**.

### Family A — LLM-as-analyst (text → directional signal)

Best-of-family and the honest traps. Full detail in the family notes; the
standouts:

| Idea | Evidence | Testability |
|---|---|---|
| A1 ChatGPT headline-sentiment drift (Lopez-Lira-Tang) | [WP→PR] 350%@10bps→50%@25bps, small/neg-news | OVERLAY-EXT; alpha in illiquid slice floor excludes |
| A2 Open-model (OPT/FinBERT) sentiment long-short | [WP] Sharpe 3.05 but sample overlaps training | IN-SCOPE-NOW (local, **no API key**) |
| A4 **Anonymized financial-statement conviction** (Kim-Muhn-Nikolaev) | [WP] GPT-4 > human analysts, anonymized = look-ahead defense | OVERLAY-EXT / NEEDS-COMPUTE |
| A6 Earnings-call Q&A evasiveness | [PR] +3.9% ann alpha aligned answers | OVERLAY-EXT (post-call tilt) |
| A7 **LLM earnings-surprise → PEAD overlay** | [WP] PEAD robust; LLM-surprise vs SUE control | OVERLAY-EXT (NB E10/E15 killed mechanical PEAD/premium) |
| A9 News-novelty vs stale filter (Tetlock reprint) | [PR] fade stale reprints | OVERLAY-EXT (filter on A1/A2) |
| A12 Calibrated-confidence → fractional-Kelly sizing | [WP] LLMs overconfident, needs recalibration | OVERLAY-EXT (sizing layer) |
| A13/A14 **Look-ahead audit + point-in-time model** (Gao-Jiang-Yan; Sarkar-Vafa) | [WP/PR] LAP collapses post-cutoff | **IN-SCOPE-NOW required gate** |

Synthesis: best testable-here = **A7 LLM-surprise PEAD overlay** (real anomaly
+ mechanical SUE control), **A4 anonymized conviction** (least look-ahead-
exposed), **A2 local sentiment** (no key). A12/A9 are cheap force-multipliers.
Biggest trap = look-ahead, not hypothetical (Levy 2026: all earnings skill may
be contamination).

### Family B — Agentic & multi-agent

| Idea | Evidence | Testability |
|---|---|---|
| B1 TradingAgents (7-role debate firm) | [WP] Sharpe 8.21 — **1×5mo bull window, 3 megacaps, look-ahead** | NEEDS-COMPUTE ($0.5–2/decision) |
| B2 FINMEM (layered memory + reflection) | [PR] few tickers, underperformed BH on ≥1 | OVERLAY-EXT (cheapest agent) |
| B9 **Devil's-advocate risk-approver** | [WP] = the veto pattern w/ a red-team persona | **IN-SCOPE-NOW** (~1 call/entry) |
| B11 PnL-journaling reflection (Reflexion) | [PR] journal extends overlay_log | OVERLAY-EXT |
| B12 ReAct broker agent (Alpaca-wired) | [WP] StockBench: mostly fails to beat BH | NEEDS-PLATFORM |
| B14 **Selective-consensus / self-consistency gate** | [WP] fewer higher-quality trades | **IN-SCOPE-NOW** (abstain=cash) |
| B15 **Contamination-free single-agent control** (StockBench) | [WP] most agents can't beat BH, bull-biased | **IN-SCOPE-NOW** (the correct control) |

Synthesis: adapt **B9** (red-team veto), **B14** (consensus gate), **B2/B11**
(memory+journal) into the harness; the full firms (B1/B13) won't survive costs
at $100–1,000. Trap: dazzling numbers are look-ahead artifacts + no realistic
fills (40–60% of reported performance evaporates under realistic costs).

### Family C — LLM + price/trend reasoning (the literal "biased off trends" path)

| Idea | Evidence | Testability |
|---|---|---|
| C1/C12 Multimodal candlestick chart-reader | [WP] **49–53% ≈ chance**; 1/215 pattern hits | OVERLAY-EXT low-priority (chart-TA null) |
| C2 Numeric OHLC-as-text forecaster (LLMTime) | [PR] inferior to ARIMA on noisy series | IN-SCOPE-NOW (cheap to falsify) |
| C3 TS foundation models (Chronos/TimesFM/Moirai/TimeGPT) | [WP] beat random-walk **2/10** tasks, "small sparse" | OVERLAY-EXT / NEEDS-COMPUTE |
| C5 Verbalize-the-trend (VTA/SEP) | [WP] eval inside cutoff = parametric look-ahead | OVERLAY-EXT (explain-trace = artifact) |
| C8 LLM exit / trailing-stop supervisor | [F] vs deterministic ATR baseline | OVERLAY-EXT |
| C9 **LLM regime-classifier → strategy router** | [F/WP] routes, doesn't forecast price | OVERLAY-EXT — highest-merit here |
| C14 **Point-in-time / memory-firewall pattern** | [WP] required harness rule | IN-SCOPE-NOW |

Synthesis: only **C9 (regime router)** and the *news leg* of trend+news fusion
have defensible merit — both avoid asking the LLM to forecast price (which it
can't). Everything chart/numeric is a documented near-null before cost.

### Family D — LLM as overlay / veto / sizer / meta-labeler (most testable family)

Schema-compatible extensions of `overlay_log`. The four standouts + the
required ablation:

| Idea | Evidence | Testability |
|---|---|---|
| D1 VetoBaseline (BUY/VETO) | [NOVEL] as overlay | IN-SCOPE-NOW (the control) |
| D2/D16 **Confidence-sizer / Abstain-meta-label** | [V] fractional-Kelly; veto = size-0 | OVERLAY-EXT (direct) |
| D3 **TripleBarrier meta-labeler** (López de Prado) | [PR/V] precision 0.21→0.39 (H&T) | OVERLAY-EXT — **best-evidenced** |
| D6 **Exit-supervisor** (daily HOLD/EXIT) | [F/NOVEL] strongest DD-reduction lever | OVERLAY-EXT (needs exit_log) |
| D7 **Catalyst-landmine check** | [PR-adj] injects genuinely NEW info | OVERLAY-EXT (needs event calendar) |
| D10 Cross-sectional ranker (tie-break >K) | [WP] uses LLM the way evidence supports | OVERLAY-EXT |
| D15 **Trend-blind vs trend-aware A/B** | [WP] required ablation | OVERLAY-EXT (direct) |

Synthesis: pre-register **D3 meta-labeling** (or its D2/D16 graded-size
generalization) + **D6 exit-supervisor** + **D7 catalyst check**, each A/B'd
against **D15** to prove the LLM adds trend-conditioning rather than
re-deriving the base signal. Trap: an overlay can't create edge where the base
has none; value is un-provable until decision-N; and non-determinism must be
frozen out via the decision-log tripwire.

### Family E — LLM as feature extractor / factor miner (LLM out of the live loop)

| Idea | Evidence | Testability |
|---|---|---|
| E1 Headline-sentiment cross-sectional factor | [PR] small/neg-news concentrated | DECOUPLED-OFFLINE, K=1–3 tension |
| E3 Formulaic-alpha mining (AlphaAgent) | [WP] **US IC collapses to 0.006** | NEEDS-COMPUTE, p-hacking engine |
| E4 **LLM offline hypothesis/rule generator → human pre-registers** (Alpha-GPT) | [WP/F] LLM upstream of the frozen loop | **IN-SCOPE-NOW — cleanest fit** |
| E5 Supply-chain lead-lag extraction (Cohen-Frazzini base) | [WP] Sharpe 0.86, FF5 α 7.27% | DECOUPLED-OFFLINE, K=1–3 tension |
| E7 8-K event-tagging over EDGAR | [WP] EDGAR = genuinely point-in-time | DECOUPLED-OFFLINE / IN-SCOPE-NOW |
| E11 **Weak-labeling → distilled deterministic classifier** | [V/F] LLM labels once, small model is live | DECOUPLED-OFFLINE — **best reproducibility** |
| E14 Sentiment VW long-short (Sharpe 3.05) | [WP] the mirage — VW/high-turnover/illiquid | NEGATIVE CONTROL, not a candidate |

Synthesis: **E4** (LLM as a brainstorming peer whose rules a human
pre-registers and a deterministic backtester falsifies) is the single cleanest
philosophical fit to the whole project — it keeps the stochastic LLM entirely
outside the reproducibility-critical path. **E11** (weak-label → pinnable
classifier) and **E7** (EDGAR 8-K tagging) follow. Trap: LLM factor mining is
industrial p-hacking (Harvey-Liu-Zhu t>3, deflated Sharpe, McLean-Pontiff
decay), and the published winners are weakest exactly in the liquid US regime
this project trades.

### Family F — LLM macro / narrative / regime interpretation

All overlays/gates, all low-frequency (tiny effective N). **Benchmark every one
head-to-head against the mechanical E18 VIX/VIX3M gate** (the project's weak
PASS-RA).

| Idea | Evidence | Testability |
|---|---|---|
| F1/F2 **Fed-speak stance / statement-shift scorer** | [WP] GPT-4 stance acc 0.57; reactions track the *shift* | OVERLAY-EXT (≈8 events/yr) |
| F3 Macro-narrative regime classifier | [WP] **negative result** (p=0.48 vs baseline) | REGIME-GATE vs E18 |
| F4 Geopolitical-risk gate (AI-GPR) | [PR] only threat-component predicts | REGIME-GATE vs E18 |
| F6 Single-stock catalyst interpreter | [WP] 90% initial reaction (not tradable) | IN-SCOPE-NOW (liquid, post-cutoff) |
| F11 **LLM risk-on/off day-classifier gate** | [WP] LLM agents no sig alpha, regime-backwards | REGIME-GATE vs E18 (the head-to-head) |
| F15 **Agentic macro-nowcaster** (live web search) | [WP] 15.8 bps/day α, **look-ahead-free** but winners-only, 1-day | NEEDS-PLATFORM |

Synthesis: **F11 / F1-F2** are the defensible ones — cheap, event-anchored,
and admit a clean "beats VIX term structure?" pre-registration; honest prior is
they won't. **F15** is the only genuinely look-ahead-free positive result in the
whole survey, but it needs a live platform and is stock-selection, not a gate.
Dominant trap = effective sample size (a handful of regimes/crises) → trivially
overfit + acute training-cutoff look-ahead.

### Family G — reality check (the credibility anchor)

Not ideas — the discipline. Summarized in the two cross-cutting sections below.

---

## The two things that decide whether ANY of this is legitimate

### 1. Look-ahead / training-cutoff contamination (the killer)
An LLM scoring historical text can *recall* the outcome it was trained on, so an
in-sample backtest measures memorization, not forecasting — and on
high-recall names it can flip the sign of the result. The evidence is not
hypothetical: **Profit Mirage** (2025) shows 50–72% return decay across the
cutoff boundary for five published agents; **Gao-Jiang-Yan** (2025) show
forecast alpha is amplified on exactly the firm-dates the model "remembers" and
collapses to insignificance post-cutoff; **Sarkar-Vafa** (ICML 2025) show a
2019 model volunteering "COVID-19" and that prompt-based date-fencing does not
fix it; **Levy** (JAR 2026) finds that for earnings prediction *all* apparent
skill may be contamination. **Mandatory, non-optional gates for any LLM
experiment here:** (a) evaluate strictly *after* the pinned model's knowledge
cutoff; (b) anonymize tickers to kill the "distraction effect"; (c) run a LAP /
fake-date placebo; (d) pin the exact model ID (a silent upgrade moves the cutoff
and re-contaminates the "clean" window).

### 2. Non-determinism vs the frozen tripwire (and its one resolution)
Even at temperature 0, hosted LLMs drift (30–50% decision-flip on repeat;
floating-point non-associativity across GPU kernels). You **cannot** pin a
d=±0.0000pp reference on a live model call. The only tripwire-compatible
architecture — and it is the one the project already half-built — is: **the LLM
writes its decisions once to an immutable `overlay_log`; the frozen tripwire is
pinned on the deterministic backtest that replays that log, never on the model
call.** This makes the LLM a *frozen data source*, not a live dependency, and
is the single most important design constraint in the brief.

### The infra & compute ladder (what a live platform / more compute buys)

| Tier | What it enables | Per-decision $ | Honors EOD? | Tripwire fit |
|---|---|---|---|---|
| **0 Offline/batch** — LLM scores a frozen post-cutoff batch → immutable log → deterministic backtest replays | ~1–5¢ ×N one-off (no key needed) | trivially | **best** — replay is deterministic |
| **1 Interactive runbook** — human runs LLM nightly, pastes verdicts | ~free (chat UI, **no API key**) | yes | good — determinism via logging |
| **2 Unattended API** — scheduled call → log → Alpaca paper | Haiku ~1–2¢ / Opus ~8–10¢/name·day (~$65/yr Opus×3 = 6.5% of a $1k book) | yes | needs the log-replay split; **BLOCKED-ON-EVAN** (no API key) |
| **3 Live data platform** — real-time news/quotes via MCP/Alpaca | Sonnet ~5–15¢ | tension (intraday temptation) | weak — live inputs non-reproducible; keep a Tier-0 twin |
| **4 Full agentic / self-host GPU** — multi-agent, memory, tools | **$5–30+/decision (multi-agent ≈ $2,500/yr > the whole book)** | fragile | worst — except a *pinned local model* for determinism |

At $100–1,000, **the per-decision API cost is a first-order term** — Tiers 0–2
are the only economically sane options; Tier 4 multi-agent is a research
curiosity whose annual cost exceeds the capital.

---

## Ranked shortlist — what to pre-register here (deduped across families)

All are long-only-capable, EOD, and plug into the existing `e1_control` vs
`e1_llm_veto` harness at **Tier 0/1 (no API key required)**. **Every one carries
a strong prior of, at best, a *risk-adjusted* (not high-return) improvement** —
consistent with the project's 0-PASS-HR record and the contamination reality.

| # | Idea | Why it's first-tier | Honest tradeoff / prior |
|---|---|---|---|
| 1 | **E4 — LLM as offline hypothesis/rule generator** | Cleanest fit: LLM brainstorms rules, human pre-registers one, deterministic backtester falsifies. Zero new infra, zero tripwire risk. *It is literally what this brief's agents just did.* | Not a tradable strategy itself — a workflow that feeds the whole PRD. Value is idea-throughput, not a signal. |
| 2 | **D3 — Triple-barrier meta-labeler** on the e1_llm_veto harness | Best-evidenced overlay (López de Prado meta-labeling; H&T precision 0.21→0.39). The existing veto is already a degenerate binary meta-label. | Can only improve a *profitable* base signal; the project's base signals mostly failed, so needs a live/borderline base to sit on. |
| 3 | **D2/D16 — Confidence-sizer / abstain-meta-label** | Generalizes the veto to graded size (veto = size-0 nested inside); free comparison; directly targets the return-centric gate. | LLM confidence is miscalibrated/overconfident — calibration map must be pre-registered, not assumed. |
| 4 | **D6 — Exit-supervisor** (daily HOLD/EXIT) | Strongest independent drawdown-reduction lever; EOD-clean (≤K calls/day). | Adds a second divergence point → attribution harder; must be its own arm. |
| 5 | **A7 — LLM earnings-surprise PEAD overlay** (vs mechanical SUE control) | Attaches the LLM to a real, decades-robust anomaly with a clean mechanical control. | Mechanical PEAD (E10) and earnings-premium (E15) already FAILED here; this tests only whether LLM-graded surprise beats SUE — thin wrinkle. |
| 6 | **F11 / C9 — LLM regime-classifier gate** benchmarked vs E18 VIX-TS | The one "reads the trend/regime" path that doesn't ask the LLM to forecast price; head-to-head against the project's own weak PASS-RA. | Low effective-N (few regimes) → hard to beat a free mechanical gate; honest prior says it won't. |
| 7 | **B9 / B14 — Red-team veto / consensus gate** | Cheapest agentic overlays; ~1–5 calls/entry; already ≈ the veto pattern. | Over-cautious veto strips winners (bull-bias); pre-register veto-only. |
| 8 | **E11 — Weak-label → distilled deterministic classifier** | Best reproducibility: LLM labels a corpus once offline, a small *pinnable* model is the live feature (frozen-tripwire-native). | Label noise propagates; needs a human-checked gold set; the classifier still faces the K=1–3 / liquidity wall. |

**Required for ALL of them (non-negotiable gates):** strictly post-model-cutoff
evaluation window · ticker anonymization · LAP/placebo audit · frozen tripwire
pinned on the deterministic replay of an immutable `overlay_log` · LLM run as a
**treatment arm vs the mechanical `e1_control`**, never as a standalone claim ·
Tier 0/1 cost accounting.

**Below the line (do not build first):** full multi-agent firms (B1/B13 — cost
> capital), chart/numeric price forecasting (C1-C6/C10-C13 — ≈ chance, collides
with the chart-TA-dead prior), LLM factor mining (E3/E13 — p-hacking engine),
and the value-weighted sentiment long-shorts (E14/A2 headline Sharpes — the
illiquid-concentrated mirage the liquidity floor demolishes; keep as a *negative
control*).

---

## How this extends the program's conclusion

This is the same wall the [full method survey](2026-07-12_swing_method_full_survey.md)
hit, now confirmed for the LLM frontier: **the high-return + robust + retail-EOD
cell stays empty.** LLM paths don't escape the structural problem (the tradable
edge concentrates in illiquid names the floor excludes and decays with
adoption) and they *add* two failure modes the mechanical strategies didn't
have — look-ahead contamination and non-determinism. The realistic ceiling is a
**risk-adjusted overlay improvement, provable only at a pre-registered N** —
which is exactly the tier the `e1_llm_veto` design already targets, and exactly
the tier of the one existing weak PASS-RA (E18). The portfolio-honest framing:
LLMs are a *treatment to be measured*, not an engine to be trusted, and the
project's pre-registration + control-vs-treatment + frozen-tripwire machinery is
the right (and rare) apparatus to measure them cleanly.

---

## What would change this conclusion

- **A live, forward, post-cutoff paper run** of shortlist #2–#5 in which the LLM
  overlay beats its mechanical control at the pre-registered decision-N — the
  only test that can't be contaminated by hindsight. (Requires Tier 2 = an
  `ANTHROPIC_API_KEY`, currently BLOCKED-ON-EVAN; Tier 0/1 can start the
  offline/human-run version now.)
- **F15's forward result holding up** — the agentic live-web-search nowcaster is
  the one genuinely look-ahead-free positive in the literature; if an
  independent forward replication survives costs, macro-nowcasting becomes worth
  a real build.
- **A data source opening** — a structured earnings/event calendar (unblocks D7),
  a licensed news/transcript feed (unblocks A6/F5), or a point-in-time
  fundamentals archive (unblocks E-family cleanly).
- **The mandate loosening** — if K rises toward a diversified book or the
  liquidity floor drops, the cross-sectional sentiment/lead-lag factors (E1/E5)
  become faithful to their evidence instead of caricatures of it.

---

## Sources (deduplicated, dated; primary preferred)

**Look-ahead / contamination / reproducibility (the anchor)**
- Glasserman & Lin — *Assessing Look-Ahead Bias in Stock Return Predictions from GPT Sentiment* (2023) — [arXiv:2309.17322](https://arxiv.org/abs/2309.17322)
- Sarkar & Vafa — *Lookahead Bias in Pretrained Language Models* (SSRN 4754678, ICML 2025) — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4754678)
- Gao, Jiang & Yan — *A Test of Lookahead Bias in LLM Forecasts* (2025) — [arXiv:2512.23847](https://arxiv.org/abs/2512.23847)
- Levy — *Caution Ahead: Numerical Reasoning and Look-Ahead Bias in AI Models* (J. Accounting Research 2026)
- *Profit Mirage: Revisiting Information Leakage in LLM-based Financial Agents* (2025) — [arXiv:2510.07920](https://arxiv.org/abs/2510.07920)
- *Chronologically Consistent Large Language Models* (2025) — [arXiv:2502.21206](https://arxiv.org/abs/2502.21206)
- *Execution Assumptions and Reproducibility in LLM-Based Trading* (2026) — [arXiv:2606.08285](https://arxiv.org/abs/2606.08285)
- StockBench — [stockbench.github.io](https://stockbench.github.io/)

**Analyst / sentiment**
- Lopez-Lira & Tang — *Can ChatGPT Forecast Stock Price Movements?* (arXiv 2304.07619, 2023, fthcmg JFE) — [arXiv](https://arxiv.org/abs/2304.07619)
- Kirtac & Germano — *Sentiment Trading with LLMs* (2024) — [arXiv:2412.19245](https://arxiv.org/abs/2412.19245)
- Kim, Muhn & Nikolaev — *Financial Statement Analysis with LLMs* (2024) — [arXiv:2407.17866](https://arxiv.org/abs/2407.17866)
- Tetlock — *All the News That's Fit to Reprint* (JF 2011); *New News is Bad News* (2023) — [arXiv:2309.05560](https://arxiv.org/pdf/2309.05560)
- *The Language of Evasion* (J. Behavioral Finance 2026)

**Agentic / multi-agent**
- Xiao et al. — *TradingAgents* (2024) — [arXiv:2412.20138](https://arxiv.org/abs/2412.20138)
- Yu et al. — *FINMEM* (2023) — [arXiv:2311.13743](https://arxiv.org/abs/2311.13743)
- Zhang et al. — *FinAgent* (KDD 2024) — [arXiv:2402.18485](https://arxiv.org/abs/2402.18485)
- Fatemi & Hu — *FinVision* (ICAIF 2024) — [arXiv:2411.08899](https://arxiv.org/abs/2411.08899)
- Chen et al. — *StockBench* (2025) — [arXiv:2510.02209](https://arxiv.org/abs/2510.02209)
- Lopez-Lira — *Can LLMs Trade?* (2025) — [arXiv:2504.10789](https://arxiv.org/abs/2504.10789)
- Shinn et al. — *Reflexion* (2023) — [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)

**Price/trend & time-series**
- Hu et al. — *Do VLMs Truly "Read" Candlesticks?* (2026) — [arXiv:2604.12659](https://arxiv.org/html/2604.12659v1)
- Gruver et al. — *LLMs Are Zero-Shot Time Series Forecasters* (NeurIPS 2023) — [arXiv:2310.07820](https://arxiv.org/pdf/2310.07820)
- *Pretrained Time-Series Foundation Models for Financial Return Forecasting* (2026) — [arXiv:2606.27100](https://arxiv.org/abs/2606.27100)
- Koa et al. — *Verbal Technical Analysis* (2025) — [arXiv:2511.08616](https://arxiv.org/pdf/2511.08616); *SEP* — [arXiv:2402.03659](https://arxiv.org/html/2402.03659v3)

**Overlay / meta-labeling**
- López de Prado — *Advances in Financial Machine Learning* (2018), meta-labeling / triple-barrier
- Hudson & Thames — *Does Meta-Labeling Add to Signal Efficacy?* — [hudsonthames.org](https://hudsonthames.org/does-meta-labeling-add-to-signal-efficacy-triple-barrier-method/)
- *Self-consistency / confidence calibration* (AAAI 2025) — [arXiv:2402.13904](https://arxiv.org/html/2402.13904)

**Feature / factor mining**
- Ke, Kelly & Xiu — *Predicting Returns with Text Data (SESTM)* — [NBER w26186](https://www.nber.org/system/files/working_papers/w26186/w26186.pdf)
- *AlphaAgent* (KDD 2025) — [arXiv:2502.16789](https://arxiv.org/html/2502.16789v2); *Navigating the Alpha Jungle* — [arXiv:2505.11122](https://arxiv.org/html/2505.11122v2)
- *Alpha-GPT* (2023) — [arXiv:2308.00016](https://arxiv.org/abs/2308.00016); *2.0* — [arXiv:2402.09746](https://arxiv.org/pdf/2402.09746)
- Cohen & Frazzini — *Economic Links and Predictable Returns* (JF 2008); *Supply-Chain Propagation of Textual Signals* (2026) — [arXiv:2606.29290](https://arxiv.org/abs/2606.29290)
- Harvey, Liu & Zhu — *…and the Cross-Section of Expected Returns* (2016); Bailey & López de Prado — *Deflated Sharpe* (2014); McLean & Pontiff (JF 2016)

**Macro / regime**
- Hansen & Kazinnik — *Can ChatGPT Decipher Fedspeak?* (2023) — [SSRN 4399406](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4399406)
- *Mind the Shift: Monetary Policy Stance from FOMC Statements with LLMs* (2026) — [arXiv:2603.14313](https://arxiv.org/html/2603.14313v1)
- Caldara & Iacoviello — *Measuring Geopolitical Risk* (AER 2022) + *AI-GPR* (2025)
- *Can LLMs Learn Macroeconomic Narratives from Social Media?* (2024, negative result) — [arXiv:2406.12109](https://arxiv.org/html/2406.12109v2)
- *Can LLM Investing Strategies Outperform the Market Long Run?* (2025) — [arXiv:2505.07078](https://arxiv.org/html/2505.07078v5)
- Chen & Pu — *Autonomous Market Intelligence: Agentic AI Nowcasting* (2026) — [arXiv:2601.11958](https://arxiv.org/abs/2601.11958)

**Adversarial / cost**
- *Adversarial News and Lost Profits* (2026) — [arXiv:2601.13082](https://arxiv.org/abs/2601.13082)
- *Cost-awareness taxonomy for multi-agent trading* (2026) — [arXiv:2603.27539](https://arxiv.org/html/2603.27539v1)
- Anthropic pricing — platform.claude.com (July 2026); Alpaca MCP — github.com/alpacahq/alpaca-mcp-server

**Prior project docs**
- [2026-07-12 full method survey](2026-07-12_swing_method_full_survey.md) · [2026-07-10 strategy catalog](2026-07-10_swing_strategy_catalog.md) · E18 VIX-TS regime gate (the existing weak PASS-RA) · the standing `e1_control` vs `e1_llm_veto` overlay design (PRD M3, tasks 14/18)
