import pandas as pd
S = "/home/samuel/trp2-delivery-challenge/analysis/out/"
D = "/home/samuel/trp2-delivery-challenge/data/"
c = pd.read_csv(S + "c.csv", parse_dates=["ts"]); l = pd.read_csv(S + "l.csv", parse_dates=["Created"])
pd.set_option("display.width", 250, "display.max_colwidth", 120, "display.max_rows", 300)
c = c.merge(l[["Lead ID", "Furthest stage", "Source"]], on="Lead ID")
def stage_by(mask, label):
    print(label, c[mask]["Furthest stage"].value_counts().to_dict())
stage_by(c.Topic == "Follow-up", "follow-up recipients:")
stage_by(c["Ivy's message"].str.startswith("You're booked"), "'You're booked' recipients:")
stage_by(c["Ivy's message"].str.startswith("Thanks for coming in"), "'Thanks for coming in' recipients:")
stage_by(c["Lead's message"].isin(["Yes please", "Thursday works. 6pm?", "Tomorrow at 7am please"]), "leads who sent 'yes/time' msgs:")
stage_by(c.Topic.isin(["Complaint", "Asked for a person"]), "complaint/person leads:")
stop = c[c["Lead's message"].str.startswith("Stop sending")]
for lid, t in zip(stop["Lead ID"], stop.ts):
    later = c[(c["Lead ID"] == lid) & (c.ts > t)]
    print("STOP", lid, "later msgs:", later[["ts", "Topic"]].values.tolist())
print("\nmsgs per lead", c.groupby("Lead ID").size().value_counts().sort_index().to_dict())
print("msgs per lead by stage", c.groupby("Lead ID").agg(n=("ts", "size"), st=("Furthest stage", "first")).groupby("st").n.mean().round(2).to_dict())
print("\nstage by created week"); print(pd.crosstab(l.Created.dt.to_period("W"), l["Furthest stage"]))
print("\nedited share by stage", c.groupby("Furthest stage")["Staff edited Ivy's draft"].apply(lambda s: round((s == "Yes").mean(), 2)).to_dict())
print("edited by studio (top/bottom)"); e = c.groupby("Studio")["Staff edited Ivy's draft"].apply(lambda s: (s == "Yes").mean()).sort_values(); print(e.round(2).head(5).to_dict(), e.round(2).tail(5).to_dict())
big = c[c.same_as_prev & (c.gap_s > 60)]; print("\nnon-instant dup:", big[["Lead ID", "gap_s", "Lead's message", "Topic"]].to_string())
print("hour of Ivy msgs", c.ts.dt.hour.value_counts().sort_index().to_dict())
print("purchases:", l[l["Furthest stage"] == "Membership purchased"][["Lead ID", "Studio", "Source", "Channel the lead used", "first_topic"]].to_string())
