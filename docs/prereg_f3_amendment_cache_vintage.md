# Amendment 1 to the F3 pre-registration — the baseline vintage

**Written 2026-09-05, ~18:05 CDT, BEFORE any floor-on run and BEFORE any runner
code changed.** Amends `docs/prereg_f3_liquidity_floor_etf_scope.md` §4.
Committed doc-only, in its own commit, for the same reason the parent prereg
was: git must prove it predates the results.

## What forced this

The parent prereg's fourth pre-committed failure condition reads:

> **If the re-run does not reproduce the recorded FAIL numbers with the floor
> DISABLED**, everything stops.

That condition cannot be met as written, and the reason has nothing to do with
the liquidity floor. `.e8e9_cache` — the research cache every affected runner
reads — is **19 days stale**: every price series ends **2026-08-17**, against a
5-day tolerance (`SWING_MAX_CACHE_STALE_DAYS`). `cache_fetch` raised
`StaleCacheError` and refused to run, exactly as designed.

Measured before deciding anything: **all 181 price-series files carry the SAME
end date, 2026-08-17.** The cache is stale but **not mixed** — the failure mode
that overstated M12's headline effect 3x (record EM/EO) is absent here.

The original verdicts were produced at earlier vintages (E8 ran 2026-07-10), so
a re-run today cannot reproduce their numbers whatever the floor does. The
window end alone moved.

## The two ways forward, and the choice

| option | what it costs | what it buys | when it breaks |
|---|---|---|---|
| **Refresh the cache** (delete all 181 price-series JSONs, re-run every consumer in one sitting) | a fresh vintage for the whole project; both F3 arms read 2026-09-04 | current data | it moves the window end for BOTH arms anyway, so it does NOT restore reproducibility against the recorded numbers — it just picks a different non-matching vintage, and it silently re-bases every other consumer |
| **Pin the vintage** at 2026-08-17 via `SWING_ALLOW_STALE_CACHE=1` — the documented escape hatch for "this run is deliberately historical" | the numbers are 19 days old | both arms read a byte-identical frozen snapshot, which is the only thing that makes an A/B attributable to the floor | it would break if the cache were MIXED; measured, it is not |

**CHOSEN: pin the vintage at 2026-08-17.** F3 asks one question — does the
liquidity floor change what these experiments hold and conclude — and that
question is only answerable if the floor is the ONLY thing that differs between
the two arms. A refresh changes the data and the floor at once.

## §4's fourth condition, restated

Replacing it, with the same intent and a target that exists:

- **The BASELINE is the floor-OFF run at vintage 2026-08-17**, not the recorded
  historical numbers. Every floor-ON result is compared against that baseline
  and against nothing else.
- **The recorded numbers become a SANITY COMPARISON, not a gate.** They are
  reported beside the baseline. A gap is expected and is attributed to the
  vintage.
- **New stop condition, and it is a real one:** if the floor-OFF baseline
  produces a **different VERDICT** from the recorded one for any experiment —
  a FAIL that is no longer a FAIL, before the floor is applied at all — then
  **everything stops** and that is reported as its own finding. A verdict that
  moves on 19 days of extra data is a fact about the experiment's fragility,
  and no F3 conclusion may be drawn on top of it.
- **Determinism:** each arm is run twice and must produce byte-identical output.
  A non-deterministic runner invalidates its own comparison.

## Everything else in the parent prereg is unchanged

§3's five predictions, §4's first three failure conditions (including the
central one — a FAIL that flips to PASS is a flag for re-examination, never a
banked verdict change), and §2's "threshold is NOT touched" all stand exactly
as written.

## Disclosure

This amendment was written after `run_e8_squeeze.py` was executed ONCE with the
floor off, which is how the staleness was discovered. That run's output is the
baseline this amendment defines, and it is reported in full rather than
discarded: **E8 floor-OFF at vintage 2026-08-17 — gate CAGR −1.43%, maxDD 24.5%,
Sharpe −0.21, n=187; secondary CAGR 1.15%, maxDD 12.6%; VERDICT FAIL.** No
floor-ON run had been executed, and no runner code had been changed, when this
amendment was written.
