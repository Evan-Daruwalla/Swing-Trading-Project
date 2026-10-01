# disclosure — Swing Trading

What may leave this project, and what must never. Created 2026-09-05 (PRD
M13.7, record FL): this bin was prescribed at bootstrap and never written, even
though the repo went **public on 2026-07-10** (record AK).

## The governing fact

`git remote -v` → `https://github.com/Evan-Daruwalla/Swing-Trading-Project.git`
— **public, under Evan's real name, as a college-application portfolio piece.**
So the default is inverted from a private repo: anything committed is
world-readable **permanently**, because git history survives a later deletion.
Ask "would I put this on a résumé" before `git add`, not after.

Pushing is Evan's alone. A `trading-guard` hook blocks the model from running
`git push` at all — publishing is his call, and the block is not to be worked
around.

## NEVER leaves — hard line

| item | why | enforced by |
|---|---|---|
| Alpaca API key/secret pairs (3 paper accounts) | credentials | `.gitignore`: `*_keys.env`, `*.env` — covers `alpaca_keys.env` |
| `swing.db` | the live paper ledger | `.gitignore` (+ journal/wal/shm) |
| `var/` | M3 runtime logs | `.gitignore` |
| Any live brokerage account number, or anything from a non-paper account | this project has never traded real money | no live account exists yet; `alpaca_client._require_paper()` refuses live endpoints |

Two independent gates back this up, and BOTH ran clean on every commit this
session: a native `core.hooksPath` → `scripts/git-hooks/pre-commit` secret scan
(covers shell commits) and a PreToolUse gate (covers model commits). The full
git history was scanned CLEAN in the 2026-07-28 audit.

**Gap, unfixed:** `commit-gate` reads `.claude/secrets-inventory.md` and this
project **has never had that file** (`ls .claude/` → `codebase-memory/`,
`pm-cadence.json` only). The scanners still run on their built-in rules, so
nothing is unguarded, but the project-specific inventory they would consult is
absent. Not fixed here because writing it is a security decision, not a
bookkeeping one.

## Already public, deliberately — do not treat as a leak

- **Alpaca PAPER order-id prefixes.** Record lines 4206–4218 (2026-07-18) carry
  `7d348c06` and `d0b7fc18` in the narrative of the double-run incident. The
  project's own stated position is that these are "regeneratable, not secrets"
  (`.gitignore` comment on `var/`), and they identify orders on paper accounts
  holding no real money. Established practice, not an incident.
- **Every FAILED experiment**, in full. The 37-attempt search phase, the
  falsified predictions, the retracted claims — all public on purpose. A
  failure honestly recorded is the deliverable here.
- **NAV, position sizes and P&L** for the 3 sleeves. They are simulated from a
  $1,000-per-sleeve paper base.

## Judgment calls, with the rule that settled them

- **New fixtures use SYNTHETIC identifiers even when the real ones are already
  public.** `scripts/prove_divergence_census.py` originally seeded its
  throwaway DB with the five real 8-char order-id prefixes; the census only
  ever tests NULL vs NOT NULL, so the real ids added nothing. Replaced with
  `oid-1`…`oid-5` on 2026-09-05. **Rule: "already published elsewhere" is not a
  reason to publish again in a new file — only need is.** Prices were KEPT
  real, because they are what makes the arithmetic checkable by a reader.
- **Absolute local paths** (`D:\ClaudeCode\...`) appear throughout docs and
  headers. Accepted: they are the run instructions on Evan's machine and reveal
  nothing about anyone else.
- **Outward-facing prose** (README, anything portfolio-shaped) goes through
  `the-humanizer` before it ships. Internal work — HANDOFF, record entries,
  PRDs, commit messages, code — does not.

## Before any push, the 30-second check

```bash
git diff --cached --stat                       # what is actually going out
git ls-files --others --exclude-standard       # untracked files that should stay untracked
git diff --cached | grep -inE "key|secret|token|password|[A-Z0-9]{20,}"
```
The pre-commit scan already covers this; the point of doing it by eye is that
the scan cannot judge *embarrassment*, only *secrets*.
