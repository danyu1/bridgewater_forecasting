import pandas as pd

data = [
    {"year":2022,"winner":"Norway"},
    {"year":2018,"winner":"Norway"},
    {"year":2014,"winner":"Russia"},
    {"year":2010,"winner":"Canada"},
    {"year":2006,"winner":"Germany"},
    {"year":2002,"winner":"Germany"},
    {"year":1998,"winner":"Germany"},
    {"year":1994,"winner":"Russia"}
]

df = pd.DataFrame(data)
counts = df["winner"].value_counts().to_dict()
total = len(df)
base_rates = {k: v/total for k,v in counts.items()}
recent = df[df["year"]>=2010]["winner"].value_counts().to_dict()
recent_total = len(df[df["year"]>=2010])
recent_rates = {k: v/recent_total for k,v in recent.items()}

print("Base rates 1994-2022:", base_rates)
print("Base rates 2010-2022:", recent_rates)
