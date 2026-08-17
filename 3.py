import pandas as pd

def calculate_overnight_windows(df):
    records = []
    for _, row in df.iterrows():
        arrival = pd.to_datetime(row["ARRIVAL"])
        departure = pd.to_datetime(row["DEPARTURE"])
        hours = (departure - arrival).total_seconds()/3600
        records.append({**row.to_dict(),"OVERNIGHT_HRS": round(hours,2)})
    return pd.DataFrame(records)
