import pandas as pd, csv
S = "/home/samuel/trp2-delivery-challenge/analysis/out/"
D = "/home/samuel/trp2-delivery-challenge/data/"
rows = list(csv.reader(open(D + "lumen_fact_sheet.csv")))
i = [k for k, r in enumerate(rows) if r and r[0] == "Studio ID"][0]
st = pd.DataFrame([r[:6] for r in rows[i+1:] if r and r[0].startswith("S")], columns=rows[i][:6])
st["renew"] = pd.to_datetime(st["Agreement renewal date"])
print("owners", st.Owner.nunique(), "multi-studio owners", st.Owner.value_counts()[lambda s: s > 1].to_dict())
print("renewals by month", st.renew.dt.to_period("M").value_counts().sort_index().to_dict())
mar = st[st.renew == "2027-03-31"]; print("MARCH 2027:", len(mar), mar[["Studio", "Owner", "Country"]].values.tolist())
comp = pd.read_csv(D + "owner_complaints.csv"); print("complaining studios renew:", st[st.Studio.isin(comp.Studio)][["Studio", "Owner", "Agreement renewal date"]].values.tolist())
c = pd.read_csv(S + "c.csv"); l = pd.read_csv(S + "l.csv")
for name, m in [("March studios", st.Studio.isin(mar.Studio)), ("others", ~st.Studio.isin(mar.Studio))]:
    ss = st[m].Studio; cc = c[c.Studio.isin(ss)]; ll = l[l.Studio.isin(ss)]
    bad = cc.Topic.isin(["Complaint", "Asked for a person"]).sum()
    print(name, "studios", len(ss), "leads", len(ll), "msgs", len(cc), "dups", int(cc.same_as_prev.sum()), "complaint/person msgs", bad,
          "wrong-ch msgs", int(((cc["Channel the lead used"] == "SMS") & (cc["Channel Ivy replied on"] == "Email")).sum()), "bought", int((ll["Furthest stage"] == "Membership purchased").sum()))
# money
life_us = 99 + 13 * 149; roy = 0.07 * life_us
print(f"\nmember lifetime revenue (US, 14 mo, 1 intro + 13 full) ${life_us}; Lumen 7% royalty ${roy:.0f}")
print("tech fee/month 40x$500 =", 40 * 500, "| Ivy cost/month 6000 | March studios fee/month", len(mar) * 500)
print("8 members/4wks -> royalty over lifetime", round(8 * roy), "| owner gross from those", 8 * life_us)
