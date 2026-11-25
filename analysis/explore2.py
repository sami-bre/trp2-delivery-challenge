import pandas as pd
D = "/home/samuel/trp2-delivery-challenge/data/"
c = pd.read_csv(D + "conversations.csv"); l = pd.read_csv(D + "leads.csv")
c["ts"] = pd.to_datetime(c["Ivy sent at"]); l["created"] = pd.to_datetime(l["Created"])
pd.set_option("display.width", 250, "display.max_colwidth", 200, "display.max_rows", 300)
c = c.sort_values(["Lead ID", "ts"])
c["gap_s"] = c.groupby("Lead ID").ts.diff().dt.total_seconds()
c["same_as_prev"] = c["Ivy's message"] == c.groupby("Lead ID")["Ivy's message"].shift()
dup = c[c.same_as_prev]
print("DUPLICATES:", len(dup), "leads affected", dup["Lead ID"].nunique(), "gap stats", dup.gap_s.describe().to_dict())
print("dup by channel ivy", dup["Channel Ivy replied on"].value_counts().to_dict(), "by topic", dup.Topic.value_counts().to_dict())
print("dup by studio", dup.Studio.value_counts().to_dict())
print("dup by week", dup.ts.dt.to_period("W").value_counts().sort_index().to_dict())
print("all msgs by week", c.ts.dt.to_period("W").value_counts().sort_index().to_dict())
print("non-dup short gaps (<120s, diff text):", ((c.gap_s < 120) & ~c.same_as_prev).sum())

print("\nLEAD MESSAGES by topic")
print(c.groupby(["Topic", "Lead's message"]).size().to_string())

print("\nHANDED TO STAFF rows"); print(c[c["Handed to staff"] == "Yes"][["Lead ID","Studio","Topic","Lead's message","Ivy's message","Staff edited Ivy's draft"]].to_string())
print("\nASK PERSON / COMPLAINT rows")
print(c[c.Topic.isin(["Asked for a person", "Complaint"])][["Message ID","Lead ID","Lead name","Studio","ts","Lead's message","Ivy's message","Staff edited Ivy's draft","Handed to staff"]].to_string())
print("\nFOLLOW-UP rows"); print(c[c.Topic == "Follow-up"][["Lead ID","ts","gap_s","Lead's message","Ivy's message"]].head(30).to_string())
c.to_csv("/home/samuel/trp2-delivery-challenge/analysis/out/c.csv", index=False)
