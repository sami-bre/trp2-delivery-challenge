"""One-tab CSV version of the Task 4 scoring sheet, for upload to Google Drive (Drive converts it to a Sheet).

Summary formulas at the top count the score rows below. The multi-tab version is build_task4_sheet.py.
Run: python3 -I analysis/build_task4_csv.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "analysis/out"
OUT = OUT_DIR / "task4_scoring_sheet.csv"
MODELS = [("Inkling 2 Mini (new)", "inkling"), ("GPT-5.6 Luna (control)", "luna")]
IVY = {"C1": 16, "C2": 14, "C3": 18, "C4": 16, "All": 9, "C1C2C4": 11, "handoffs": 0}
DATA_HEADER = ["Model", "Eval ID", "Lead's message", "Model reply", "Needed a handoff?", "Model's handoff flag",
               "C1 Handoff", "C1 reason", "C2 Facts", "C2 reason", "C2 judge runs passing",
               "C4 Answers", "C4 reason", "C4 judge runs passing", "C1+C2+C4 all pass", "Hand check"]

data = []
for label, name in MODELS:
    replies = {r["Eval ID"]: r for r in csv.DictReader(open(OUT_DIR / f"{name}_replies.csv"))}
    for s in csv.DictReader(open(OUT_DIR / f"{name}_scores.csv")):
        data.append([label, s["Eval ID"], s["Lead's message"], s["Reply"],
                     "No" if s["C1 reason"] == "no handoff needed" else "Yes", replies[s["Eval ID"]]["Handoff flag"],
                     s["C1 handoff"], s["C1 reason"], s["C2 facts"], s["C2 reason"],
                     s["C2 judge votes (pass)"].replace("/", " of "),
                     s["C4 answers"], s["C4 reason"], s["C4 judge votes (pass)"].replace("/", " of "),
                     None, s["Hand check"]])

top = [
    ["New model test: scoring summary"],
    ["Same 20 conversations (Eval set tab) and the same eval as Task 3. Scored 25 Nov 2026. "
     "Ivy's numbers come from the Task 3 scoring sheet (TRP2 W0 - Ivy Eval Scoring Sheet)."],
    [],
    ["Criterion", "Ivy", MODELS[0][0], MODELS[1][0], "Out of"],
    "C1", "C2", "C3", "C4", "All", "C1C2C4",
    [],
    ["Handoffs", "Ivy", MODELS[0][0], MODELS[1][0], "Out of"],
    "handoffs", "extra",
    [],
    ["Models"],
    ["New model: Inkling 2 Mini (thinkingmachines/inkling-2-mini), released 20 Nov 2026 (Thinking Machines announcement; listed on OpenRouter 21 Nov). "
     "$0.075 in / $0.30 out per million tokens."],
    ["Control: GPT-5.6 Luna (openai/gpt-5.6-luna), July 2026, so it was available before Ivy launched. Same prompt "
     "as the new model. It shows how much of any gain comes from the instructions rather than a newer model."],
    ["Judge for facts and answers: GLM-5.3-Flash (z-ai/glm-5.3-flash), 3 runs per reply, majority."],
    [],
    ["Method and limits"],
    ["We were not given Ivy's prompt or model. Ivy's live replies look templated: 367 messages are about 13 fixed "
     "texts with the name and studio swapped in."],
    ["Both models got the same rebuilt prompt (analysis/ivy_prompt.md in the repo): the full fact sheet plus the "
     "lead's name, channel and message. No hints from the eval were added."],
    ["The sending system, not the model, chooses SMS or email, so C3 does not apply to the models."],
    ["Neither model had studio class schedules or the booking system, which Ivy has. This affects E11 and E18."],
    ["Every fail was checked by hand. Hand changes are in the Hand check column."],
    [],
    DATA_HEADER,
]
first = len(top) + 1
last = first + len(data) - 1
rng = lambda col: f"${col}${first}:${col}${last}"


def count(model, *pairs):
    cond = "".join(f',{rng(c)},"{v}"' for c, v in pairs)
    return f'=COUNTIFS({rng("A")},"{model}"{cond})'


def model_cells(*pairs):
    return [count(m, *pairs) for m, _ in MODELS]


rows_by_key = {
    "C1": ["C1. Hands off to staff when it must", IVY["C1"], *model_cells(("G", "Pass")), 20],
    "C2": ["C2. Facts match the fact sheet", IVY["C2"], *model_cells(("I", "Pass")), 20],
    "C3": ["C3. Replies on the lead's channel", IVY["C3"], "Not the model's choice", "Not the model's choice", 20],
    "C4": ["C4. Answers the question", IVY["C4"], *model_cells(("L", "Pass")), 20],
    "All": ["All criteria that apply", IVY["All"], *model_cells(("O", "Pass")), 20],
    "C1C2C4": ["C1, C2 and C4 only (like for like)", IVY["C1C2C4"], *model_cells(("O", "Pass")), 20],
    "handoffs": ["Handoffs done when one was needed", IVY["handoffs"], *model_cells(("E", "Yes"), ("G", "Pass")),
                 f'=COUNTIFS({rng("A")},"{MODELS[0][0]}",{rng("E")},"Yes")'],
    "extra": ["Sent to staff when not needed (model's flag)", "Not recorded", *model_cells(("E", "No"), ("F", "Yes")),
              f'=COUNTIFS({rng("A")},"{MODELS[0][0]}",{rng("E")},"No")'],
}
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    for row in top:
        w.writerow(rows_by_key[row] if isinstance(row, str) else row)
    for i, row in enumerate(data, start=first):
        row[14] = f'=IF(AND(G{i}="Pass",I{i}="Pass",L{i}="Pass"),"Pass","Fail")'
        w.writerow(row)
print(OUT, OUT.stat().st_size)
