from datetime import datetime

def hhmm_to_minutes(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
    dt = datetime.strptime(str(value), "%H:%M")
    return dt.hour * 60 + dt.minute
