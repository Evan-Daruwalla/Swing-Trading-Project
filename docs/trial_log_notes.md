# Trial log — what `docs/trial_log.json` is, and what it is NOT

**Built 2026-08-06 (CDT) by `scripts/build_trial_log.py`. Regenerate, never hand-edit.**

## Why this exists

The deflated Sharpe ratio (Bailey & López de Prado) deflates an observed Sharpe by
the number of trials the search actually conducted. **That number is the single
easiest input in the whole method to fudge** — understate it and DSR happily
reports significance that was really bought by search effort. This project's
append-only record is an unusually honest trial log already, but it is *prose*;
a DSR calculation cannot consume prose, and a human re-counting it each time will
drift. This file is the machine-readable extraction.

## The headline numbers

| quantity | value | status |
|---|---|---|
| prereg docs on disk (TEMPLATE excluded) | **37** | verified |
| highest attempt number in the record | **38** | verified |
| **declared variants across all preregs** | **50** | **LOWER BOUND** |
| entries with an unresolvable field | 1 (E18 verdict) | flagged, not guessed |

## ⚠ UNRESOLVED: 37 vs 38

The record numbers attempts up to **#38** (M12) but only **37** prereg documents
exist. The capstone states **37**. **This is not silently resolved**, because
picking one to make the arithmetic tidy is exactly the kind of quiet choice that
makes a trial count untrustworthy.

**Rule for DSR: use the LARGER figure.** A trial count that is too high makes the
deflated Sharpe *more* conservative; too low flatters the strategy. When in doubt
the error must point away from significance.

## The variant count is a LOWER BOUND, and materially so

`declared_variants` counts only variants **declared in a prereg** — e.g. E18's 4
gates, M12's 2×2 cells × 2 cost levels, X8's 2 arms. It **excludes**, and these
are not small:

- **Parameter values explored before pre-registration.** Preregs pin the final
  parameters; the exploration that chose them is not itemised.
- **The ~90-method survey** (2026-07-12) and the **dropped-16 list** (record
  Appendix B) — strategies considered and rejected without a prereg. Rejecting a
  strategy on inspection is still a trial in the search-effort sense.
- **Abandoned variants never written down.**

**Therefore any DSR computed from 50 is OPTIMISTIC** — too generous to the
strategy. The true search effort is strictly larger. That direction of error is
stated here so it cannot be quietly forgotten at the point of use.

## The verdict field is a pointer, not a ruling

`headline_verdict_at_publication` is the first verdict token in the results doc's
headline **at publication**. It is *not* the program's final verdict, and several
were superseded:

- **E4** published **PASS** → later **killed by E5** (92.7% DD in the unseen
  2000–13 window).
- **E6** published **PASS** → downgraded to a *market-dependent risk overlay, not
  a high-return engine*.
- **M10-1** published **PASS-HR** → capped as **IN-SAMPLE-COMPOSED**,
  forward-paper-only.

`final_verdict` is deliberately `null` everywhere: it is not auto-derivable, and
the **append-only record is authoritative**. Do not let a DSR pipeline read the
headline field as a ruling.

**A bug this file exists to remember:** the first matcher took the token before
the first `_`, so `m10_2_*` matched **M10-1's** results doc and the log recorded
m10_2 as **PASS-HR** when M10-2 actually **FAILED** (2.99% CAGR / 83.3% DD). A
trial log that invents a verdict is worse than no trial log. The matcher now
keeps numeric sub-indices and requires delimiters on both sides.

## How this must be used

1. **The log is a hard input to DSR, not a reference.** A DSR run that does not
   read this file has no defensible trial count.
2. **Regenerate before every DSR computation** — `python scripts/build_trial_log.py`.
   A stale log silently under-counts as soon as one more variant is tried.
3. **Every future variant gets a prereg entry, including abandoned ones.** The
   moment an abandoned arm goes unlogged, the count is understated in the
   direction that flatters the result.
4. **Unknowns stay unknown.** The script emits `null` + `_unknown`; nothing
   downstream may fill them by inference.
