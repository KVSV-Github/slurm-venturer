import pandas as pd
from rich.progress import Progress, SpinnerColumn, TextColumn
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

def run_with_spinner(msg, func, *args, **kwargs):
    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
    ) as progress:
        progress.add_task(msg, total=None)
        return func(*args, **kwargs)

def create_folder(folder):
    folder.mkdir(parents=True, exist_ok=True)
    return folder