"""Score replies to the Eval set against the Task 3 criteria.

C1 hands off when it must   -> code (rules from the fact sheet's policies)
C2 facts match fact sheet   -> LLM judge, majority of RUNS calls
C3 replies on lead's channel -> code
C4 answers the question     -> LLM judge, majority of RUNS calls

Usage:
  python3 -I analysis/grade.py <replies.csv> <reply column> <reply channel column> <out.csv>
Ivy:   python3 -I analysis/grade.py data/eval_set.csv "Ivy's draft" "Channel of Ivy's draft" analysis/out/ivy_scores.csv
"""
import csv, json, re, sys, time, urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = "z-ai/glm-5.3-flash"
RUNS = 3

NEEDS_HANDOFF = re.compile(
    r"charged|refund|bill\b|billing|injur|talk to|speak to|call me|call back|manager|human|real person|stop sending|stop messaging",
    re.I)
NEEDS_STAFF = re.compile(
    r"charged|refund|bill\b|billing|injur|talk to|speak to|call me|call back|manager|human|real person", re.I)
HANDS_OFF = re.compile(
    r"pass(ed)? (this|it|your request) (to|along)|let our .* know|asked our .* to|will (call|contact)|'ll (call|contact)"
    r"|flagged|won't message|stop sending", re.I)
SALES_PITCH = re.compile(r"free (first )?class|free trial|intro month|book you|save you a spot|what day works", re.I)


def load_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("OPENROUTER_API_KEY missing from .env")


def fact_sheet_text():
    rows = list(csv.reader(open(ROOT / "data/lumen_fact_sheet.csv")))
    start = next(i for i, r in enumerate(rows) if r and r[0] == "Prices")
    end = next(i for i, r in enumerate(rows) if r and r[0] == "Studios and franchise agreements")
    return "\n".join(" | ".join(c for c in r if c) for r in rows[start:end] if any(r))


def check_handoff(lead_msg, reply):
    reply = reply.replace("’", "'")
    if not NEEDS_HANDOFF.search(lead_msg):
        return True, "no handoff needed"
    if not HANDS_OFF.search(reply):
        return False, "needed a handoff to staff but the reply does not pass it on"
    if SALES_PITCH.search(reply):
        return False, "handed off but still includes a sales pitch"
    return True, "handed off to staff"


JUDGE_PROMPT = """You are checking one reply sent by Lumen Studios to a new lead. Lumen is a chain of yoga and fitness studios.

FACT SHEET (the only source of truth for prices and policies):
{facts}

Assume US prices unless the lead mentions a Canadian city or Canada.

LEAD'S MESSAGE: {lead}
REPLY BEING CHECKED: {reply}
REPLY A STAFF MEMBER SENT (a guide to a good answer, not the source of truth; the reply being checked
does not need to include details that are missing from the fact sheet): {staff}

Judge two things:
facts_pass: true if every price, offer and policy stated in the reply matches the fact sheet.
  False if any stated fact contradicts the fact sheet or is made up. Leaving a fact out is not a failure.
  Class times are not in the fact sheet; accept times that match the staff reply.
answers_pass: true if the reply directly answers what the lead asked or asked for.
  False if it ignores the question, gives a generic line, or only pushes a booking.

Reply with JSON only:
{{"facts_pass": true/false, "facts_reason": "<one short sentence>", "answers_pass": true/false, "answers_reason": "<one short sentence>"}}"""


def judge(key, facts, lead, reply, staff):
    body = json.dumps({
        "model": MODEL,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "user", "content": JUDGE_PROMPT.format(facts=facts, lead=lead, reply=reply, staff=staff)}],
    }).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                text = json.load(r)["choices"][0]["message"]["content"]
            return json.loads(text[text.find("{"): text.rfind("}") + 1])
        except Exception as e:
            err = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"judge call failed: {err}")


def majority(votes):
    passes = sum(v for v, _ in votes)
    verdict = passes * 2 > len(votes)
    reason = next(r for v, r in votes if v == verdict)
    return verdict, reason, f"{passes}/{len(votes)}"


def cached_judgements(out):
    """Earlier judge results for the same reply, so a rerun after a rule fix doesn't re-judge."""
    if not Path(out).exists():
        return {}
    return {(r["Eval ID"], r["Reply"]): r for r in csv.DictReader(open(out))}


def hand_overrides(out):
    path = ROOT / "analysis/hand_overrides.csv"
    if not path.exists():
        return {}
    return {(r["Eval ID"], r["Criterion"]): r for r in csv.DictReader(open(path)) if r["Scores file"] == Path(out).name}


def main(src, reply_col, channel_col, out):
    key, facts = load_key(), fact_sheet_text()
    rows = list(csv.DictReader(open(src)))
    cache, overrides = cached_judgements(out), hand_overrides(out)
    results = []
    for r in rows:
        lead, reply, staff = r["Lead's message"], r[reply_col], r["Reply staff actually sent"]
        c1, c1_reason = check_handoff(lead, reply)
        flag = r.get("Handoff flag")
        if flag and c1 and flag == "No" and NEEDS_STAFF.search(lead):
            c1, c1_reason = False, "reply text is fine but the handoff flag says No, so staff are never told"
        if r[channel_col] == "system":
            c3, c3_reason = None, "channel is chosen by the sending system, not the model"
        else:
            c3 = r["Channel the lead used"] == r[channel_col]
            c3_reason = "same channel" if c3 else f"lead used {r['Channel the lead used']}, reply sent by {r[channel_col]}"
        prev = cache.get((r["Eval ID"], reply))
        if prev:
            c2, c2_reason, c2_votes = prev["C2 facts"] == "Pass", prev["C2 reason"], prev["C2 judge votes (pass)"]
            c4, c4_reason, c4_votes = prev["C4 answers"] == "Pass", prev["C4 reason"], prev["C4 judge votes (pass)"]
        else:
            runs = [judge(key, facts, lead, reply, staff) for _ in range(RUNS)]
            c2, c2_reason, c2_votes = majority([(bool(j["facts_pass"]), j["facts_reason"]) for j in runs])
            c4, c4_reason, c4_votes = majority([(bool(j["answers_pass"]), j["answers_reason"]) for j in runs])
        hand_notes = []
        for crit in ["C2", "C4"]:
            o = overrides.get((r["Eval ID"], crit))
            if o:
                verdict = o["Verdict"] == "Pass"
                hand_notes.append(f"{crit} changed to {o['Verdict']} by hand: {o['Reason']}")
                if crit == "C2":
                    c2, c2_reason = verdict, "Hand check: " + o["Reason"]
                else:
                    c4, c4_reason = verdict, "Hand check: " + o["Reason"]
        results.append({
            "Eval ID": r["Eval ID"], "Topic": r["Topic"], "Lead's message": lead, "Reply": reply,
            "C1 handoff": "Pass" if c1 else "Fail", "C1 reason": c1_reason,
            "C2 facts": "Pass" if c2 else "Fail", "C2 reason": c2_reason, "C2 judge votes (pass)": c2_votes,
            "C3 channel": "N/A" if c3 is None else "Pass" if c3 else "Fail", "C3 reason": c3_reason,
            "C4 answers": "Pass" if c4 else "Fail", "C4 reason": c4_reason, "C4 judge votes (pass)": c4_votes,
            "All pass": "Pass" if all(c is not False for c in [c1, c2, c3, c4]) else "Fail",
            "Hand check": "; ".join(hand_notes) or "Agrees",
        })
        print(r["Eval ID"], *(results[-1][k] for k in ["C1 handoff", "C2 facts", "C3 channel", "C4 answers"]),
              c2_votes, c4_votes, flush=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader(); w.writerows(results)
    needed = sum(bool(NEEDS_HANDOFF.search(r["Lead's message"])) for r in rows)
    print(f"\nneeded handoff: {needed}")
    for k in ["C1 handoff", "C2 facts", "C3 channel", "C4 answers", "All pass"]:
        scored = [x for x in results if x[k] != "N/A"]
        print(k, f"{sum(x[k] == 'Pass' for x in scored)} / {len(scored)}" if scored else "N/A")


if __name__ == "__main__":
    main(*sys.argv[1:5])
