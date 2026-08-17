import pandas as pd

def export_daily_check(df, output_file):
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="DAILY_CHECK", index=False)
