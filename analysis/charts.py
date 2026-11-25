"""Charts for the submission document. Writes PNGs to charts/.

Run: cd /tmp && uv run --quiet --with matplotlib python -I /home/samuel/trp2-delivery-challenge/analysis/charts.py
Numbers come from data/ and analysis/out/ (see notes/data-findings.md).
"""
import csv
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "charts"
OUT.mkdir(exist_ok=True)

SURFACE, INK, INK_2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA, YELLOW, MAGENTA = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"
NEUTRAL = "#b5b3ac"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "text.color": INK, "axes.labelcolor": INK_2,
    "xtick.color": INK_2, "ytick.color": INK_2, "axes.edgecolor": AXIS,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
})


def style(ax, grid_axis="x"):
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    ax.spines["left" if grid_axis == "x" else "bottom"].set_color(AXIS)
    ax.spines["bottom" if grid_axis == "x" else "left"].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def titles(fig, title, subtitle):
    fig.text(0.02, 0.97, title, fontsize=15, fontweight="bold", va="top", color=INK)
    fig.text(0.02, 0.905, subtitle, fontsize=11, va="top", color=INK_2)


def save(fig, name, source):
    fig.text(0.02, 0.02, source, fontsize=9, color=MUTED)
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)
    print(OUT / name)


def read(path):
    return list(csv.DictReader(open(ROOT / path)))


def funnel():
    leads = read("data/leads.csv")
    order = ["No reply", "Replied", "Trial booked", "Trial attended", "Membership purchased"]
    rank = {s: i for i, s in enumerate(order)}
    n = len(leads)
    steps = [("All leads", 0), ("Replied to Ivy", 1), ("Booked a trial", 2), ("Attended the trial", 3),
             ("Bought a membership", 4)]
    counts = [sum(rank[l["Furthest stage"]] >= r for l in leads) for _, r in steps]

    fig, ax = plt.subplots(figsize=(10, 5.2))
    fig.subplots_adjust(left=0.22, right=0.95, top=0.78, bottom=0.14)
    y = list(range(len(steps)))[::-1]
    colors = [NEUTRAL, BLUE, NEUTRAL, NEUTRAL, ORANGE]
    ax.barh(y, counts, height=0.55, color=colors)
    ax.set_yticks(y, [s for s, _ in steps])
    for yi, c in zip(y, counts):
        ax.text(c + 4, yi, f"{c}  ({c / n:.1%})" if c != n else f"{c}", va="center", fontsize=11, color=INK)
    ax.text(counts[1] + 70, y[1], "← what the dashboard calls \"conversion\"", va="center", fontsize=10, color=INK_2)
    ax.text(counts[4] + 70, y[4], "← paid members, the number owners care about", va="center", fontsize=10, color=INK_2)
    ax.set_xlim(0, 400)
    ax.set_xlabel("Leads")
    style(ax, "x")
    titles(fig, "The dashboard's 31% is replies. Only 3.2% of leads bought.",
           "Furthest stage reached by each of the 250 leads, 19 Oct – 15 Nov 2026")
    save(fig, "1_funnel.png", "Source: Lumen Data Extract, Leads tab")


def vendor_vs_real():
    convos = read("data/conversations.csv")
    topics = Counter(c["Topic"] for c in convos)
    groups = [
        ("Class schedule & location", ["Class schedule", "Studio location"], BLUE),
        ("Pricing & policies", ["Pricing", "Cancellation and freeze"], ORANGE),
        ("Trial booking", ["Trial booking"], AQUA),
        ("Follow-ups", ["Follow-up"], YELLOW),
        ("Complaints & requests for a person", ["Complaint", "Asked for a person"], MAGENTA),
    ]
    raw = list(csv.reader(open(ROOT / "data/vendor_eval.csv")))
    header = next(i for i, r in enumerate(raw) if r and r[0] == "Test ID")
    vendor = Counter(r[1] for r in raw[header + 1:] if r and r[0].startswith("T"))
    total_v, total_r = sum(vendor.values()), len(convos)
    rows = [("Vendor's 50 test questions", {g: sum(vendor[t] for t in ts) for g, ts, _ in groups}, total_v),
            ("Real lead messages (429)", {g: sum(topics[t] for t in ts) for g, ts, _ in groups}, total_r)]

    fig, ax = plt.subplots(figsize=(10, 4.4))
    fig.subplots_adjust(left=0.25, right=0.97, top=0.76, bottom=0.28)
    for yi, (label, vals, total) in zip([1, 0], rows):
        left = 0
        for g, _, color in groups:
            share = vals[g] / total
            if share:
                ax.barh(yi, share, left=left, height=0.5, color=color, edgecolor=SURFACE, linewidth=2)
                if share >= 0.06:
                    ink = INK if color == YELLOW else "#ffffff"
                    ax.text(left + share / 2, yi, f"{share:.0%}", ha="center", va="center", fontsize=10,
                            color=ink, fontweight="bold")
                else:
                    ax.text(left + share / 2, yi + 0.36, f"{share:.0%}", ha="center", va="center", fontsize=10,
                            color=INK)
            left += share
    ax.set_yticks([1, 0], [r[0] for r in rows])
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    style(ax, "x")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in groups]
    fig.legend(handles, [g for g, _, _ in groups], loc="lower left", bbox_to_anchor=(0.02, 0.06), ncol=3,
               frameon=False, fontsize=10)
    titles(fig, "The 92% test covered topics that are 28% of real traffic.",
           "Topic mix of the vendor's quality test vs Ivy's real conversations")
    save(fig, "2_vendor_vs_real.png", "Source: Lumen Data Extract, Vendor eval and Conversations tabs")


def model_test():
    scores = {name: read(f"analysis/out/{name}_scores.csv") for name in ["ivy", "inkling", "luna"]}
    series = [("Ivy today", "ivy", NEUTRAL), ("Inkling 2 Mini (new, Nov 2026)", "inkling", BLUE),
              ("GPT-5.6 Luna (older, July 2026)", "luna", ORANGE)]

    def like_for_like(rows):
        return sum(all(r[k] == "Pass" for k in ["C1 handoff", "C2 facts", "C4 answers"]) for r in rows)

    criteria = [("Hands off\nwhen it must", "C1 handoff"), ("Facts match\nthe fact sheet", "C2 facts"),
                ("Answers the\nquestion", "C4 answers"), ("All three\npass", None)]
    fig, ax = plt.subplots(figsize=(10, 5.4))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.76, bottom=0.27)
    width = 0.24
    for i, (label, key, color) in enumerate(series):
        vals = [like_for_like(scores[key]) if c is None else sum(r[c] == "Pass" for r in scores[key])
                for _, c in criteria]
        xs = [x + (i - 1) * (width + 0.02) for x in range(len(criteria))]
        ax.bar(xs, vals, width=width, color=color, label=label)
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.3, str(v), ha="center", fontsize=10, color=INK)
        needed = [r for r in scores[key] if r["C1 reason"] != "no handoff needed"]
        done = sum(r["C1 handoff"] == "Pass" for r in needed)
        ax.text(xs[0], 1.0, f"{done}/{len(needed)}", ha="center", fontsize=11,
                color=INK if color == NEUTRAL else "#ffffff", fontweight="bold")
    ax.set_xticks(range(len(criteria)), [c for c, _ in criteria])
    ax.set_ylim(0, 21)
    ax.set_ylabel("Replies passing, out of 20")
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
    style(ax, "y")
    fig.legend(loc="lower left", bbox_to_anchor=(0.06, 0.06), ncol=3, frameon=False, fontsize=10)
    titles(fig, "Same instructions: the older model beat the new one.",
           "20 hard conversations, scored with the Task 3 eval. Both models got the same rebuilt prompt.\n"
           "Inside the first bars: how many of the 4 leads who needed staff each one handed off.")
    save(fig, "3_model_test.png", "Source: analysis/out/*_scores.csv. Channel (C3) is set by the sending system, so it is left out.")


def wrong_channel():
    leads = read("analysis/out/l.csv")
    sms = [l for l in leads if l["Channel the lead used"] == "SMS"]
    groups = [("First reply by SMS", [l for l in sms if l["wrong_channel"] == "False"], BLUE),
              ("First reply by email", [l for l in sms if l["wrong_channel"] == "True"], ORANGE)]

    fig, ax = plt.subplots(figsize=(10, 4.2))
    fig.subplots_adjust(left=0.22, right=0.95, top=0.72, bottom=0.2)
    for yi, (label, g, color) in zip([1, 0], groups):
        replied = sum(l["Furthest stage"] != "No reply" for l in g)
        bought = sum(l["Furthest stage"] == "Membership purchased" for l in g)
        rate = replied / len(g)
        ax.barh(yi, rate, height=0.5, color=color)
        ax.text(rate + 0.01, yi, f"{rate:.0%} replied  ·  {bought} bought  ({len(g)} leads)", va="center",
                fontsize=11, color=INK)
    ax.set_yticks([1, 0], [g[0] for g in groups])
    ax.set_xlim(0, 0.7)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.set_xlabel("Share of SMS leads who replied to Ivy")
    style(ax, "x")
    titles(fig, "SMS leads answered by email rarely replied, and none bought.",
           "The 150 leads who wrote by SMS, split by the channel of Ivy's first reply")
    save(fig, "4_wrong_channel.png", "Source: Lumen Data Extract, Leads and Conversations tabs")


if __name__ == "__main__":
    funnel()
    vendor_vs_real()
    model_test()
    wrong_channel()
