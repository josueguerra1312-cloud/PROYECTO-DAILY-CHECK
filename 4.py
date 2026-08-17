import pandas as pd

def load_tasks(path):
    return pd.read_excel(path)

def classify_window(hours):
    return "TRANSIT CHECK" if hours <= 4 else "DAILY CHECK"

def assign_tasks(windows_df, tasks_df):
    output=[]
    for _, flight in windows_df.iterrows():
        work=tasks_df.copy()
        work["MATRICULA"]=flight["MATRICULA"]
        work["OVERNIGHT_HRS"]=flight["OVERNIGHT_HRS"]
        work["CHECK_TYPE"]=classify_window(flight["OVERNIGHT_HRS"])
        output.append(work)
    return pd.concat(output, ignore_index=True)
