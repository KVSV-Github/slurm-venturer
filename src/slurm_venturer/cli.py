import pandas as pd
from datetime import datetime
from pathlib import Path
import typer
from rich.console import Console

from slurm_venturer.CSVProvider import CSVProvider
from slurm_venturer.SacctProvider import SacctProvider
from slurm_venturer.Results import Results
from slurm_venturer.Plotter import Plotter

app = typer.Typer(
    help="Slurm efficiency metrics."
)
console = Console()

banner = r"""
  ___ _                 __   __       _                    
 / __| |_  _ _ _ _ __   \ \ / /__ _ _| |_ _  _ _ _ ___ _ _ 
 \__ \ | || | '_| '  \   \ V / -_) ' \  _| || | '_/ -_) '_|
 |___/_|\_,_|_| |_|_|_|   \_/\___|_||_\__|\_,_|_| \___|_|                                             
"""

@app.command()
def main(
    user: str | None = typer.Option(
        None,
        "--user",
        "-u",
        help="Filter results by given UID. If none is provided, data from all users is processed."
        ),
    save_data: bool = typer.Option(
        False,
        "--save-data",
        help="Use sacct to retrieve data, and then save to a file."
    ),
    data_path: Path = typer.Option(
        Path("./data"),
        "--data-path",
        help="If you use the --save-data flag, then this will specify which file to save the data to. Otherwise, this is file from where the data is loaded."
    ),
    out_path: Path = typer.Option(
        Path("./results/"),
        "--out",
        "-o",
        help="Specify the results folder."
    )
):
    console.print(banner, style="bold blue")
    console.print("Slurm efficiency metrics.", style="dim")

    provider = None
    if save_data:
        provider = SacctProvider()
    else:
        provider = CSVProvider(data_path)
    
    data = provider.get_data(user)
    results = Results(data)

    folder = out_path / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder.mkdir(parents=True, exist_ok=True)

    plotter = Plotter(results, folder)

    plotter.distribution(
        results.cpu_util,
        title="Slurm CPU Utilisation",
        xlabel="CPU Utilisation")

    plotter.distribution(
        results.time_util,
        title="Slurm Time Utilisation",
        xlabel="Time Utilisation")

    if save_data:
        data.to_csv(data_path)

if __name__ == "__main__":
    app()