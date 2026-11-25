import pandas as pd
D = "/home/samuel/trp2-delivery-challenge/data/"
c = pd.read_csv(D + "conversations.csv")
l = pd.read_csv(D + "leads.csv")
c["ts"] = pd.to_datetime(c["Ivy sent at"])
l["created"] = pd.to_datetime(l["Created"])
pd.set_option("display.width", 250, "display.max_colwidth", 120, "display.max_rows", 200)

print("conversations", c.shape, "leads", l.shape)
print("date range msgs", c.ts.min(), c.ts.max(), "leads", l.created.min(), l.created.max())
print("unique leads in convos", c["Lead ID"].nunique(), "leads w/o convo", (~l["Lead ID"].isin(c["Lead ID"])).sum(),
      "convo leads not in leads tab", (~c["Lead ID"].isin(l["Lead ID"])).sum())
for col in ["Topic", "Channel the lead used", "Channel Ivy replied on", "Staff edited Ivy's draft", "Handed to staff"]:
    print(c[col].value_counts(dropna=False), "\n")
print(pd.crosstab(c["Channel the lead used"], c["Channel Ivy replied on"], margins=True))
print(pd.crosstab(c["Staff edited Ivy's draft"], c["Handed to staff"], margins=True))
print(pd.crosstab(c["Topic"], c["Handed to staff"], margins=True))
print(pd.crosstab(c["Topic"], c["Staff edited Ivy's draft"], margins=True))
for col in ["Source", "Channel the lead used", "Furthest stage"]:
    print(l[col].value_counts(dropna=False), "\n")
print("studios convos", c.Studio.nunique(), "studios leads", l.Studio.nunique())
print("lead-msg uniq", c["Lead's message"].nunique(), "ivy-msg uniq", c["Ivy's message"].nunique())
