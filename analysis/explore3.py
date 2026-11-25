import pandas as pd, re
S = "/home/samuel/trp2-delivery-challenge/analysis/out/"
D = "/home/samuel/trp2-delivery-challenge/data/"
c = pd.read_csv(S + "c.csv", parse_dates=["ts"]); l = pd.read_csv(D + "leads.csv", parse_dates=["Created"])
pd.set_option("display.width", 250, "display.max_colwidth", 230, "display.max_rows", 300)
ca = {"Toronto","Vancouver","Calgary","Edmonton","Ottawa","Montreal","Victoria","Halifax"}
c["CA"] = c.Studio.apply(lambda s: any(x in s for x in ca))
c["tmpl"] = c.apply(lambda r: r["Ivy's message"].replace(r["Studio"], "<STUDIO>").replace(r["Lead name"].split()[0], "<NAME>"), axis=1)
print("IVY TEMPLATES per topic (count, edited share)")
g = c.groupby(["Topic", "tmpl"]).agg(n=("tmpl", "size"), edited=("Staff edited Ivy's draft", lambda s: (s == "Yes").mean())).reset_index()
print(g.sort_values(["Topic", "n"], ascending=[True, False]).to_string())
print("\nCanada studios quoted USD $ w/o CA$:", ((c.CA) & c["Ivy's message"].str.contains(r"(?<!CA)\$\d") ).sum(), "of CA msgs", c.CA.sum())
print(c[(c.CA) & c["Ivy's message"].str.contains(r"(?<!CA)\$\d")].groupby("Topic").size())
