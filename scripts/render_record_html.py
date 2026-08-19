r"""Render the append-only project record to a standalone, self-contained HTML twin.

PORTED, NOT IMPORTED, from Trading's scripts/render_record_html.py (the two repos
are separate and Trading is read-only from here). Same approach, this project's
title and paths.

WHY THIS EXISTS: PRD M6 scopes a "record HTML twin" and it was never built --
HANDOFF said "No HTML twin yet" while M6 was marked Done (record FB). Evan chose
BUILD over narrowing the milestone (2026-08-19). The markdown record stays the
ground truth; this is a reading view (clickable TOC, tables, light/dark).

REGENERATE AFTER EVERY APPEND, or the twin drifts from the record it mirrors.
It is a DERIVED artifact: never edit the .html by hand, and never treat it as a
source. If the two disagree, the .md wins.

DATA CONVENTION: touches no price data. Reads one markdown file, writes one HTML.

Usage:  .venv\Scripts\python.exe scripts\render_record_html.py
Output: docs/Project Record — Full Chronological History.html  (overwritten)

Key detail: heading ids use GitHub-style anchors so in-doc links resolve. After
writing, every internal anchor is checked and the script EXITS 1 if any is
broken -- a twin with dead links is worse than no twin, because it looks
navigable and is not.
"""
import os
import re
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC_NAME = "Project Record — Full Chronological History"
SRC = os.path.join(ROOT, "docs", DOC_NAME + ".md")
OUT = os.path.join(ROOT, "docs", DOC_NAME + ".html")

SCROLL_MARGIN_TOP = "25vh"


def gh_slugify(value, separator):
    """GitHub-compatible slug. Per-space replace (no collapsing) so an em-dash
    keeps its double hyphen, matching anchors written in the .md."""
    s = value.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = s.replace(" ", separator)
    return s


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{
    --bg: #0d1117; --fg: #c9d1d9; --muted: #8b949e; --link: #58a6ff;
    --border: #30363d; --table-alt: #161b22; --code-bg: #161b22; --accent: #1f6feb;
  }}
  @media (prefers-color-scheme: light) {{
    :root {{
      --bg: #ffffff; --fg: #1f2328; --muted: #59636e; --link: #0969da;
      --border: #d0d7de; --table-alt: #f6f8fa; --code-bg: #f6f8fa; --accent: #0969da;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    background: var(--bg); color: var(--fg); margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 16px; line-height: 1.6;
  }}
  .topbar {{
    position: sticky; top: 0; z-index: 10; background: var(--bg);
    border-bottom: 1px solid var(--border); padding: 10px 20px;
    font-size: 14px; color: var(--muted);
  }}
  main {{ max-width: 960px; margin: 0 auto; padding: 24px 20px 120px; }}
  h1, h2, h3, h4 {{ line-height: 1.25; margin-top: 1.6em; scroll-margin-top: {scroll}; }}
  h1 {{ border-bottom: 1px solid var(--border); padding-bottom: .3em; }}
  h2 {{ border-bottom: 1px solid var(--border); padding-bottom: .25em; }}
  a {{ color: var(--link); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  code {{
    background: var(--code-bg); padding: .15em .35em; border-radius: 4px;
    font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: .88em;
  }}
  pre {{
    background: var(--code-bg); border: 1px solid var(--border); border-radius: 6px;
    padding: 12px; overflow-x: auto;
  }}
  pre code {{ background: none; padding: 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; display: block; overflow-x: auto; }}
  th, td {{ border: 1px solid var(--border); padding: 6px 12px; text-align: left; }}
  tr:nth-child(even) {{ background: var(--table-alt); }}
  blockquote {{
    border-left: 3px solid var(--accent); margin: 1em 0; padding: .2em 1em;
    color: var(--fg); background: var(--table-alt);
  }}
  hr {{ border: none; border-top: 1px solid var(--border); margin: 2.5em 0; }}
  del {{ color: var(--muted); }}
</style>
</head>
<body>
<div class="topbar">{topbar}</div>
<main>
{body}
</main>
</body>
</html>
"""


def render(src, out, title, topbar):
    """Render one markdown file to a self-contained HTML file.
    Fails loudly (exit 1) on broken anchors."""
    with open(src, encoding="utf-8") as f:
        text = f.read()

    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "nl2br"],
        extension_configs={"toc": {"slugify": gh_slugify}},
    )
    html = TEMPLATE.format(body=body, scroll=SCROLL_MARGIN_TOP,
                           title=title, topbar=topbar)

    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    hrefs = set(re.findall(r'href="#([^"]+)"', html))
    ids = set(re.findall(r'id="([^"]+)"', html))
    broken = sorted(hrefs - ids)
    print("Wrote %s (%s bytes)" % (out, format(os.path.getsize(out), ",")))
    print("internal links: %d  heading ids: %d  broken: %d"
          % (len(hrefs), len(ids), len(broken)))
    for b in broken:
        print("  BROKEN ->", b)
    if broken:
        sys.exit(1)


def main():
    render(SRC, OUT,
           title="Project Record — Swing Trading",
           topbar=('Project Record · Swing Trading · DERIVED from the .md '
                   '(regenerate after every append; the .md wins on conflict)'))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
