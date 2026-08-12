import pandas as pd

def slurm_seconds(s):
    # Convert D-HH:MM:SS -> D days HH:MM:SS
    if "-" in s:
        days, rest = s.split("-", 1)
        s = f"{days} days {rest}"

    # Convert MM:SS.xxx -> 00:MM:SS.xxx
    parts = s.split(":")
    if len(parts) == 2:
        s = "00:" + s

    return pd.to_timedelta(s).total_seconds()