import pandas as pd
S = "/home/samuel/trp2-delivery-challenge/analysis/out/"
D = "/home/samuel/trp2-delivery-challenge/data/"
c = pd.read_csv(S + "c.csv", parse_dates=["ts"]); l = pd.read_csv(D + "leads.csv", parse_dates=["Created"])
pd.set_option("display.width", 250, "display.max_colwidth", 200, "display.max_rows", 300)
ca = ["Toronto","Vancouver","Calgary","Edmonton","Ottawa","Montreal","Victoria","Halifax"]
c["CA"] = c.Studio.apply(lambda s: any(x in s for x in ca)); l["CA"] = l.Studio.apply(lambda s: any(x in s for x in ca))
p = c[c.Topic == "Pricing"]
print("Pricing: US studios given CA$:", (~p.CA & p["Ivy's message"].str.contains("CA\\$")).sum(),
      "| CA studios given US $149:", (p.CA & p["Ivy's message"].str.contains("are \\$149")).sum(),
      "| CA studios given CA$169 (intro still $99):", (p.CA & p["Ivy's message"].str.contains("CA\\$169")).sum(),
      "| CA studios any $99 intro:", (p.CA & p["Ivy's message"].str.contains("for \\$99")).sum(), "| CA pricing msgs", p.CA.sum())
print(p[p["Ivy's message"].str.contains("CA\\$")][["Studio","Lead's message"]].value_counts().to_string())
print("\nwho asked 'How much is it per month in Canada?':"); print(p[p["Lead's message"].str.contains("Canada")][["Studio","Ivy's message"]].to_string())

first = c.sort_values("ts").groupby("Lead ID").first().reset_index()
l = l.merge(first[["Lead ID", "ts", "Channel Ivy replied on", "Topic"]].rename(columns={"ts": "first_ivy", "Topic": "first_topic"}), on="Lead ID")
l["resp_min"] = (l.first_ivy - l.Created).dt.total_seconds() / 60
print("\nfirst response minutes", l.resp_min.describe().round(1).to_dict())
order = ["No reply", "Replied", "Trial booked", "Trial attended", "Membership purchased"]
l["rank"] = l["Furthest stage"].map({s: i for i, s in enumerate(order)})
l["replied"] = l["rank"] >= 1; l["booked"] = l["rank"] >= 2; l["bought"] = l["rank"] == 4
n = len(l)
print("\nFUNNEL:", {s: int((l["rank"] >= i).sum()) for i, s in enumerate(order)}, "n", n)
print("reply+ %", round(l.replied.mean()*100, 1), "booked+ %", round(l.booked.mean()*100, 1), "bought %", round(l.bought.mean()*100, 1))
l["wrong_channel"] = (l["Channel the lead used"] == "SMS") & (l["Channel Ivy replied on"] == "Email")
anywrong = c[(c["Channel the lead used"] == "SMS") & (c["Channel Ivy replied on"] == "Email")]["Lead ID"].unique()
l["any_wrong"] = l["Lead ID"].isin(anywrong)
dupl = c[c.same_as_prev]["Lead ID"].unique(); l["dup"] = l["Lead ID"].isin(dupl)
for col in ["Channel the lead used", "wrong_channel", "any_wrong", "dup", "Source", "CA", "first_topic"]:
    print("\n", l.groupby(col).agg(n=("replied", "size"), reply=("replied", "mean"), booked=("booked", "mean"), bought=("bought", "mean")).round(3).to_string())
print("\nSMS leads first reply on email by source:"); print(pd.crosstab(l[l["Channel the lead used"]=="SMS"].Source, l[l["Channel the lead used"]=="SMS"].wrong_channel))
w = c[(c["Channel the lead used"] == "SMS")]
print("\nSMS msgs replied by email by topic:"); print(pd.crosstab(w.Topic, w["Channel Ivy replied on"]))
print("by week:"); print(pd.crosstab(w.ts.dt.to_period("W"), w["Channel Ivy replied on"]))
l.to_csv(S + "l.csv", index=False)
