"""One-shot cleanup: remove the two synthetic rows a landing-check agent wrote
into the live paper ledger on 2026-08-25 while testing the new mark_nav refusal.

Both are test fixtures, not market data:
  paper_nav       e6_1x / 2026-08-25 / 1140.4494...  implies QQQ 812.0000 exactly.
                  The same day's real rows imply ~710.7 (e18_vixts, m10_1_nagel).
  paper_positions e6_1x / ZZZZ / 10 @ 50 / 2026-08-20  no matching transactions.

The 19:00 run already fired against this state: e6_1x correctly REFUSED to
record a NAV (no price for ZZZZ) and exited 1; the other two sleeves ran
normally and placed no orders. After this cleanup e6_1x keeps an honest HOLE
for 2026-08-25 -- that is the designed behaviour, and the missed-session guard
will report it. Tomorrow's run records normally once ZZZZ is gone.

Safe to re-run: reports 0 deleted if already clean.
"""
import sqlite3

c = sqlite3.connect("swing.db")
before_nav = c.execute("select count(*) from paper_nav").fetchone()[0]
before_pos = c.execute("select count(*) from paper_positions").fetchone()[0]

n1 = c.execute(
    "delete from paper_nav where sleeve='e6_1x' and date='2026-08-25'").rowcount
n2 = c.execute(
    "delete from paper_positions where sleeve='e6_1x' and ticker='ZZZZ'").rowcount
c.commit()

after_nav = c.execute("select count(*) from paper_nav").fetchone()[0]
after_pos = c.execute("select count(*) from paper_positions").fetchone()[0]

print("deleted paper_nav rows       : %d" % n1)
print("deleted paper_positions rows : %d" % n2)
print("paper_nav       %d -> %d   (expected 87 -> 86)" % (before_nav, after_nav))
print("paper_positions %d -> %d   (expected  4 ->  3)" % (before_pos, after_pos))

print("\nremaining 2026-08-25 NAV rows, with implied QQQ close:")
rows = list(c.execute(
    "select p.sleeve, p.nav, q.qty from paper_nav p join paper_positions q"
    "  on q.sleeve = p.sleeve and q.ticker = 'QQQ'"
    " where p.date = '2026-08-25' order by p.sleeve"))
for sleeve, nav, qty in rows:
    print("    %-14s nav=%10.2f  implied QQQ=%7.2f" % (sleeve, nav, nav / qty))

print("\nremaining positions:")
for r in c.execute(
        "select sleeve,ticker,qty,entry_price,entry_date from paper_positions"
        " order by sleeve,ticker"):
    print("   ", r)

sane = all(700 < nav / qty < 725 for _, nav, qty in rows)
ok = (after_nav == 86 and after_pos == 3 and n1 == 1 and n2 == 1 and sane)
print("\nRESULT:", "CLEAN" if ok else "UNEXPECTED STATE - check by hand before the next run")
c.close()
