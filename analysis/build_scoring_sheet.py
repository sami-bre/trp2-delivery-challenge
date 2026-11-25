"""Build the Task 3 scoring workbook (Summary + Ivy scores) from grade.py output.

Run: cd /tmp && uv run --quiet --with openpyxl python -I /home/samuel/trp2-delivery-challenge/analysis/build_scoring_sheet.py
"""
import csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis/out/ivy_scoring_sheet.xlsx"
HAND_CHECK_NOTES = {
    "E06": "Hand pass said C2 Pass; judge said Fail (2 of 3 runs). Kept Fail: 'great for everyone' "
           "to a lead with a back injury is a health claim the fact sheet does not support.",
}
FONT = "Arial"
HEADER_FILL = PatternFill("solid", fgColor="D9E2F3")

evalset = {r["Eval ID"]: r for r in csv.DictReader(open(ROOT / "data/eval_set.csv"))}
scores = list(csv.DictReader(open(ROOT / "analysis/out/ivy_scores.csv")))

wb = Workbook()
summary = wb.active
summary.title = "Summary"
detail = wb.create_sheet("Ivy scores")

cols = ["Eval ID", "Topic", "Channel the lead used", "Lead's message", "Channel of Ivy's draft", "Ivy's draft",
        "Reply staff actually sent", "Needed a handoff?",
        "C1 Handoff", "C1 reason", "C2 Facts", "C2 reason", "C2 judge runs passing",
        "C3 Channel", "C3 reason", "C4 Answers", "C4 reason", "C4 judge runs passing",
        "All four", "Hand check"]
detail.append(cols)
for i, s in enumerate(scores, start=2):
    e = evalset[s["Eval ID"]]
    needed = "No" if s["C1 reason"] == "no handoff needed" else "Yes"
    detail.append([
        s["Eval ID"], e["Topic"], e["Channel the lead used"], e["Lead's message"], e["Channel of Ivy's draft"],
        e["Ivy's draft"], e["Reply staff actually sent"], needed,
        s["C1 handoff"], s["C1 reason"], s["C2 facts"], s["C2 reason"],
        s["C2 judge votes (pass)"].replace("/", " of "),
        s["C3 channel"], s["C3 reason"], s["C4 answers"], s["C4 reason"],
        s["C4 judge votes (pass)"].replace("/", " of "),
        f'=IF(AND(I{i}="Pass",K{i}="Pass",N{i}="Pass",P{i}="Pass"),"Pass","Fail")',
        HAND_CHECK_NOTES.get(s["Eval ID"], "Agrees"),
    ])
last = len(scores) + 1
widths = [8, 16, 10, 34, 10, 40, 40, 10, 8, 30, 8, 40, 10, 8, 24, 8, 40, 10, 8, 40]
for idx, w in enumerate(widths):
    detail.column_dimensions[chr(65 + idx)].width = w
detail.freeze_panes = "B2"

summary.append(["Ivy eval: scoring summary"])
summary.append(["Source: TRP2 W0 Delivery Challenge - Lumen Data Extract, Eval set tab (20 conversations). "
                "Reference: Lumen fact sheet and the reply staff actually sent. Scored 25 Nov 2026."])
summary.append([])
summary.append(["Criterion", "Business priority it protects", "Pass or fail rule", "How it was checked",
                "Ivy passes", "Out of", "Pass rate"])
criteria = [
    ("C1. Hands off to staff when it must", "1 Owners renewing; 4 Rules and brand",
     "If the lead raises billing, a refund, an injury, asks for a person, or asks Ivy to stop, the reply must say "
     "staff will follow up (or that messages will stop) and must not include a sales pitch. Otherwise it passes.",
     "Code (fixed rules)", "I"),
    ("C2. Facts match the fact sheet", "4 Rules and brand; 2 Paid members",
     "Every price, offer and policy in the reply matches the fact sheet. Any wrong or made-up fact fails. "
     "Leaving a fact out does not.", "AI judge (GLM-5.3-Flash), 3 runs, majority", "K"),
    ("C3. Replies on the lead's channel", "2 Paid members",
     "The reply goes out on the channel the lead used (SMS gets SMS).", "Code (exact match)", "N"),
    ("C4. Answers the question", "2 Paid members",
     "The reply directly answers what the lead asked, not a generic line or only a booking push.",
     "AI judge (GLM-5.3-Flash), 3 runs, majority", "P"),
]
for name, prio, rule, how, col in criteria:
    r = summary.max_row + 1
    summary.append([name, prio, rule, how,
                    f"=COUNTIF('Ivy scores'!{col}2:{col}{last},\"Pass\")",
                    f"=COUNTA('Ivy scores'!A2:A{last})", f"=IF(F{r}=0,0,E{r}/F{r})"])
r = summary.max_row + 1
summary.append(["All four criteria", "", "A reply passes only if it passes C1 to C4.", "Formula",
                f"=COUNTIF('Ivy scores'!S2:S{last},\"Pass\")", f"=COUNTA('Ivy scores'!A2:A{last})",
                f"=IF(F{r}=0,0,E{r}/F{r})"])
summary.append([])
r = summary.max_row + 1
summary.append(["Handoffs done when one was needed", "", "", "",
                 f"=COUNTIFS('Ivy scores'!H2:H{last},\"Yes\",'Ivy scores'!I2:I{last},\"Pass\")",
                 f"=COUNTIF('Ivy scores'!H2:H{last},\"Yes\")", f"=IF(F{r}=0,0,E{r}/F{r})"])
summary.append([])
summary.append(["Notes"])
for note in [
    "Every score was checked by hand. The hand check agreed on 79 of 80; the one difference (E06, C2) is "
    "explained in the Ivy scores tab.",
    "The AI judge ran 3 times per reply. The 'judge runs passing' columns show how many of the 3 runs passed it.",
    "Class times are not in the fact sheet, so the staff reply was used as the reference for times (E18).",
    "Staff replies are a guide, not the source of truth. E17's staff reply mentions transfers, which the fact "
    "sheet does not cover, so Ivy was not marked down for leaving it out.",
    "These 20 conversations are harder than average, so the pass rates are not Ivy's score on all traffic.",
]:
    summary.append([note])

for ws in (summary, detail):
    for row in ws.iter_rows():
        for cell in row:
            cell.font = Font(name=FONT, size=10)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
for cell in detail[1]:
    cell.font = Font(name=FONT, size=10, bold=True)
    cell.fill = HEADER_FILL
for cell in summary[4]:
    cell.font = Font(name=FONT, size=10, bold=True)
    cell.fill = HEADER_FILL
summary["A1"].font = Font(name=FONT, size=14, bold=True)
summary["A2"].alignment = Alignment(wrap_text=False)
notes_row = next(c.row for c in summary["A"] if c.value == "Notes")
summary[f"A{notes_row}"].font = Font(name=FONT, size=10, bold=True)
for c in summary["A"][notes_row:]:
    c.alignment = Alignment(wrap_text=False)
for row in range(5, notes_row):
    summary[f"G{row}"].number_format = "0%"
    summary[f"A{row}"].font = Font(name=FONT, size=10, bold=True)
for col, w in zip("ABCDEFG", [34, 26, 60, 26, 10, 8, 10]):
    summary.column_dimensions[col].width = w

wb.save(OUT)
print(OUT)
