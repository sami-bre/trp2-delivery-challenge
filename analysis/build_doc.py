"""Build one HTML file from answers/task1-7.md for upload to Google Drive (Drive converts HTML to a Google Doc).

Run: cd /tmp && uv run --quiet --with markdown python -I /home/samuel/trp2-delivery-challenge/analysis/build_doc.py <out.html>
Charts are linked from the public repo (raw.githubusercontent.com) so Drive can fetch them.
"""
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
RAW = "https://raw.githubusercontent.com/sami-bre/trp2-delivery-challenge/main/charts/"
REPO = "https://github.com/sami-bre/trp2-delivery-challenge"
SHEET3 = "https://docs.google.com/spreadsheets/d/1swOqkOm-SPvSRQUXH1KW1kdcVENunuYkuYDdfRfuBBg/edit"
SHEET4 = "https://docs.google.com/spreadsheets/d/1gvSU125wbeGCd8qIVgLh1RerCHJqZw5G6wfDX7GhxBA/edit"
CHARTS = {
    2: [("1_funnel.png", "Chart: the dashboard's 31% is replies; 3.2% of leads bought"),
        ("4_wrong_channel.png", "Chart: SMS leads answered by email rarely replied, and none bought")],
    3: [("2_vendor_vs_real.png", "Chart: topic mix of the vendor's test vs real conversations")],
    4: [("3_model_test.png", "Chart: same instructions, the older model beat the new one")],
}


def fix_lists(text):
    out, prev = [], ""
    for line in text.split("\n"):
        is_item = re.match(r"^(\d+\.|-)\s", line) is not None
        prev_item = re.match(r"^(\d+\.|-)\s", prev) is not None
        if is_item and prev.strip() and not prev_item:
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def demote(text):
    return re.sub(r"^(#+) ", lambda m: "#" * (len(m.group(1)) + 1) + " ", text, flags=re.M)


def to_html(text):
    html = markdown.markdown(fix_lists(demote(text)), extensions=["tables", "nl2br"])
    html = html.replace("<table>", '<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse">')
    return html.replace("<th>", '<th style="background-color:#d9e2f3;text-align:left">')


parts = [
    "<h1>TRP2 Week 0 Delivery Challenge: Lumen Studios and Ivy</h1>",
    "<p>Seven tasks, in order. Word counts are shown under each written part.</p>",
    f'<p><b>Links:</b> <a href="{SHEET3}">Task 3 scoring sheet</a> · <a href="{SHEET4}">Task 4 scoring sheet</a> · '
    f'<a href="{REPO}">Code, prompt and data (GitHub)</a></p>',
]
for n in range(1, 8):
    html = to_html((ROOT / f"answers/task{n}.md").read_text())
    imgs = "".join(
        f'<p><img src="{RAW}{f}" alt="{alt}" width="620"></p>' for f, alt in CHARTS.get(n, []))
    parts.append(html + imgs)
Path(sys.argv[1]).write_text("<html><body>" + "\n".join(parts) + "</body></html>")
print(sys.argv[1], Path(sys.argv[1]).stat().st_size)
