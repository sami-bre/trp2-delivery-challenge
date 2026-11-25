"""Generate replies to the 20 Eval set conversations with a given model, using the rebuilt Ivy prompt.

Usage:
  python3 -I analysis/generate.py <openrouter model id> <out.csv>
Output keeps the Eval set columns and adds "Model reply", "Handoff flag", and
"Reply channel" = "system" (the channel is chosen by Ivy's sending system, not the model).
"""
import csv, json, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))
from grade import load_key  # noqa: E402


def full_fact_sheet():
    rows = list(csv.reader(open(ROOT / "data/lumen_fact_sheet.csv")))
    return "\n".join(" | ".join(c for c in r if c) for r in rows if any(r))


def lead_name(staff_reply):
    m = re.match(r"Hi (\w+)", staff_reply)
    return m.group(1) if m else "there"


def ask(key, model, system, user):
    body = json.dumps({
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                resp = json.load(r)
            text = resp["choices"][0]["message"]["content"]
            return json.loads(text[text.find("{"): text.rfind("}") + 1]), resp.get("usage", {})
        except Exception as e:
            err = e
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"{model} call failed: {err}")


def main(model, out):
    key = load_key()
    system = (ROOT / "analysis/ivy_prompt.md").read_text().format(fact_sheet=full_fact_sheet())
    rows = list(csv.DictReader(open(ROOT / "data/eval_set.csv")))
    tokens = 0
    for r in rows:
        lead_msg = r["Lead's message"]
        user = (f"Lead's name: {lead_name(r['Reply staff actually sent'])}\n"
                f"Studio: not recorded\n"
                f"Channel the lead used: {r['Channel the lead used']}\n"
                f"Lead's message: {lead_msg}")
        result, usage = ask(key, model, system, user)
        tokens += usage.get("total_tokens", 0)
        r["Model reply"] = result["reply"]
        r["Handoff flag"] = "Yes" if result.get("handoff_to_staff") else "No"
        r["Reply channel"] = "system"
        print(r["Eval ID"], r["Handoff flag"], result["reply"][:100].replace("\n", " "), flush=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print("total tokens", tokens)


if __name__ == "__main__":
    main(*sys.argv[1:3])
