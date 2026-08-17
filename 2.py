import pandas as pd

def load_flights(path):
    return pd.read_excel(path)

def filter_gdl_flights(df):
    departures = df[df["DEP"] == "GDL"]
    arrivals = df[df["DST"] == "GDL"]
    result = pd.concat([departures, arrivals])
    result = result.sort_values(by=["MATRICULA", "DATE", "TIME"])
    return result

def build_sequences(df):
    records = []
    for ac in df["MATRICULA"].unique():
        ac_df = df[df["MATRICULA"] == ac].sort_values("TIME").reset_index(drop=True)
        for i in range(len(ac_df)-1):
            current = ac_df.iloc[i]
            nxt = ac_df.iloc[i+1]
            if current["DST"] == "GDL":
                records.append({
                    "MATRICULA": ac,
                    "FLT_IN": current["FLT"],
                    "ARRIVAL": current["ARR"],
                    "DEPARTURE": nxt["DEP_TIME"]
                })
    return pd.DataFrame(records)
