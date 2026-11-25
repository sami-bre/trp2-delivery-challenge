"""Build the Task 4 scoring workbook: Summary + one scores tab each for Inkling 2 Mini and GPT-5.6 Luna.

Ivy's numbers are copied from the Task 3 scoring sheet, which holds Ivy's per-reply scores.
Run: cd /tmp && uv run --quiet --with openpyxl python -I /home/samuel/trp2-delivery-challenge/analysis/build_task4_sheet.py
"""
import csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "analysis/out"
OUT = OUT_DIR / "task4_scoring_sheet.xlsx"
FONT = "Arial"
HEADER_FILL = PatternFill("solid", fgColor="D9E2F3")
IVY_SOURCE = "Source: Task 3 scoring sheet (TRP2 W0 - Ivy Eval Scoring Sheet), Summary tab"
IVY = {"C1": 16, "C2": 14, "C3": 18, "C4": 16, "All": 9, "C1C2C4": 11, "handoffs": 0}

TABS = [("Inkling 2 Mini scores", "inkling"), ("GPT-5.6 Luna scores", "luna")]
COLS = ["Eval ID", "Lead's message", "Model reply", "Needed a handoff?", "Model's handoff flag",
        "C1 Handoff", "C1 reason", "C2 Facts", "C2 reason", "C2 judge runs passing",
        "C3 Channel", "C4 Answers", "C4 reason", "C4 judge runs passing", "All criteria that apply", "Hand check"]
WIDTHS = [8, 32, 46, 10, 10, 8, 28, 8, 38, 10, 14, 8, 38, 10, 10, 36]

wb = Workbook()
summary = wb.active
summary.title = "Summary"
last = 21

for title, name in TABS:
    ws = wb.create_sheet(title)
    ws.append(COLS)
    replies = {r["Eval ID"]: r for r in csv.DictReader(open(OUT_DIR / f"{name}_replies.csv"))}
    for i, s in enumerate(csv.DictReader(open(OUT_DIR / f"{name}_scores.csv")), start=2):
        ws.append([
            s["Eval ID"], s["Lead's message"], s["Reply"],
            "No" if s["C1 reason"] == "no handoff needed" else "Yes", replies[s["Eval ID"]]["Handoff flag"],
            s["C1 handoff"], s["C1 reason"], s["C2 facts"], s["C2 reason"], s["C2 judge votes (pass)"].replace("/", " of "),
            "Not the model's choice", s["C4 answers"], s["C4 reason"], s["C4 judge votes (pass)"].replace("/", " of "),
            f'=IF(AND(F{i}="Pass",H{i}="Pass",L{i}="Pass"),"Pass","Fail")', s["Hand check"],
        ])
    for idx, w in enumerate(WIDTHS):
        ws.column_dimensions[chr(65 + idx)].width = w
    ws.freeze_panes = "B2"


def per_tab(template):
    return [template.format(t=f"'{t}'") for t, _ in TABS]


summary.append(["New model test: scoring summary"])
summary.append(["Same 20 conversations (Eval set tab) and the same eval as Task 3. Scored 25 Nov 2026."])
summary.append([])
summary.append(["Criterion", "Ivy", "Inkling 2 Mini (new)", "GPT-5.6 Luna (control)", "Out of"])
for label, ivy, tmpl in [
    ("C1. Hands off to staff when it must", IVY["C1"], f"=COUNTIF({{t}}!F2:F{last},\"Pass\")"),
    ("C2. Facts match the fact sheet", IVY["C2"], f"=COUNTIF({{t}}!H2:H{last},\"Pass\")"),
    ("C3. Replies on the lead's channel", IVY["C3"], "Not the model's choice"),
    ("C4. Answers the question", IVY["C4"], f"=COUNTIF({{t}}!L2:L{last},\"Pass\")"),
    ("All criteria that apply", IVY["All"], f"=COUNTIF({{t}}!O2:O{last},\"Pass\")"),
    ("C1, C2 and C4 only (like for like)", IVY["C1C2C4"], f"=COUNTIF({{t}}!O2:O{last},\"Pass\")"),
]:
    summary.append([label, ivy, *per_tab(tmpl), 20])
summary.append([])
summary.append(["Handoffs", "Ivy", "Inkling 2 Mini (new)", "GPT-5.6 Luna (control)", "Out of"])
summary.append(["Handoffs done when one was needed", IVY["handoffs"],
                *per_tab(f"=COUNTIFS({{t}}!D2:D{last},\"Yes\",{{t}}!F2:F{last},\"Pass\")"),
                f"=COUNTIF('{TABS[0][0]}'!D2:D{last},\"Yes\")"])
summary.append(["Sent to staff when not needed (model's flag)", "Not recorded",
                *per_tab(f"=COUNTIFS({{t}}!E2:E{last},\"Yes\",{{t}}!D2:D{last},\"No\")"),
                f"=COUNTIF('{TABS[0][0]}'!D2:D{last},\"No\")"])
summary.append([IVY_SOURCE])
summary.append([])
summary.append(["Models"])
for note in [
    "New model: Inkling 2 Mini (thinkingmachines/inkling-2-mini), released 20 Nov 2026 (Thinking Machines announcement; listed on OpenRouter 21 Nov). "
    "Price $0.075 in / $0.30 out per million tokens.",
    "Control: GPT-5.6 Luna (openai/gpt-5.6-luna), July 2026, so it was available before Ivy launched. Same prompt as "
    "the new model. It shows how much of any gain comes from the instructions rather than a newer model.",
    "Judge for facts and answers: GLM-5.3-Flash (z-ai/glm-5.3-flash), 3 runs per reply, majority.",
]:
    summary.append([note])
summary.append([])
summary.append(["Method and limits"])
for note in [
    "We were not given Ivy's prompt or model. Ivy's live replies look templated: 367 messages are about 13 fixed "
    "texts with the name and studio swapped in.",
    "Both models got the same rebuilt prompt (analysis/ivy_prompt.md in the repo): the full fact sheet plus the "
    "lead's name, channel and message. No hints from the eval were added.",
    "The sending system, not the model, chooses SMS or email, so C3 does not apply to the models.",
    "Neither model had studio class schedules or the booking system, which Ivy has. This affects E11 and E18.",
    "Every fail was checked by hand. Hand changes are in the Hand check column of each tab.",
]:
    summary.append([note])

for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            cell.font = Font(name=FONT, size=10)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    if ws is not summary:
        for cell in ws[1]:
            cell.font = Font(name=FONT, size=10, bold=True)
            cell.fill = HEADER_FILL
summary["A1"].font = Font(name=FONT, size=14, bold=True)
for c in summary["A"]:
    if c.value in ("Criterion", "Handoffs"):
        for cell in summary[c.row]:
            cell.font = Font(name=FONT, size=10, bold=True)
            cell.fill = HEADER_FILL
    elif c.value in ("Models", "Method and limits"):
        c.font = Font(name=FONT, size=10, bold=True)
    elif c.value and summary[f"B{c.row}"].value is None:
        c.alignment = Alignment(wrap_text=False)
for col, w in zip("ABCDE", [44, 14, 22, 24, 8]):
    summary.column_dimensions[col].width = w

wb.save(OUT)
print(OUT)
