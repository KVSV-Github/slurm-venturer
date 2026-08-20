import pandas as pd
from datetime import datetime
from pathlib import Path
import typer
from rich.console import Console

from slurm_venturer.lib.utils import run_with_spinner
from slurm_venturer.cli_text import app_help, banner, help_text
from slurm_venturer.lib.providers.CSVProvider import CSVProvider
from slurm_venturer.lib.providers.SacctProvider import SacctProvider
from slurm_venturer.lib.Results import Results
from slurm_venturer.lib.Plotter import Plotter

app = typer.Typer(
    help=app_help,
    no_args_is_help=True
)
console = Console()

@app.callback(invoke_without_command=True)
def main():
    console.print(banner, style="bold blue")
    console.print(app_help + "\n", style="dim")

@app.command(help=help_text["download"])
def download(
    user: str | None = typer.Option(
        None,
        "--user",
        "-u",
        help=help_text["user"]
    ),
    out_path: Path = typer.Option(
        ...,
        "--out",
        "-o",
        help=help_text["out"]
    ),
    start: str = typer.Option(
        "today",
        "--start",
        "-s",
        help=help_text["start"]
    ),
    end: str = typer.Option(
        "now",
        "--end",
        "-e",
        help=help_text["end"]
    )
):
    provider = SacctProvider(start, end)
    data = run_with_spinner("Getting accounting data...", provider.get_data, user)

    folder = out_path / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder.mkdir(parents=True, exist_ok=True)

    data.to_csv(folder / "data.csv")
    console.print(f"Downloaded {len(data.index)} job(s)!", style="bright_green")

@app.command(help=help_text["analyse"])
def analyse(
    user: str | None = typer.Option(
        None,
        "--user",
        "-u",
        help=help_text["user"]
    ),
    data_path: Path = typer.Option(
        ...,
        "--data",
        help=help_text["data"]
    ),
    out_path: Path = typer.Option(
        Path("./results/"),
        "--out",
        "-o",
        help=help_text["out"]
    )
):
    provider = CSVProvider(data_path)
    data = provider.get_data(user)
    results = Results(data)

    folder = out_path / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    plotter = Plotter(folder)

    plotter.distribution(
        results.cpu_util,
        title="Slurm CPU Utilisation",
        xlabel="CPU Utilisation")
    
    # plotter.distribution(
    #     results.time_util_hrplus,
    #     title="Slurm Time Utilisation (1hr+ elapsed)",
    #     xlabel="Time Utilisation")

    # plotter.distribution(
    #     results.time_util_lesshr,
    #     title="Slurm Time Utilisation (<1hr elapsed)",
    #     xlabel="Time Utilisation")

    # plotter.distribution(
    #     results.time_util,
    #     title="Slurm Time Utilisation",
    #     xlabel="Time Utilisation")

    plotter.distribution(
        results.time_alloc_hrs,
        title="Slurm Time Allocated",
        bins=24,
        percentage=False,
        xlabel="Hours")

    plotter.distribution(
        results.time_elapsed_hrs,
        title="Slurm Time Elapsed",
        percentage=False,
        xlabel="Hours")

    coeff, counts = results.scheduling_coeff
    plotter.heatmap(
        coeff, counts,
        title="Scheduling Coefficient Matrix (numbers are #jobs)",
        cbarlabel="Scheduling Coefficient",
        ylabel="Runtime in hrs",
        xlabel="#nodes")

    coeff, counts = results.time_util_matrix
    plotter.heatmap(
        coeff, counts,
        title="Wall Clock Wastage Matrix (numbers are #jobs)",
        cbarlabel="Hours wasted",
        ylabel="Runtime",
        xlabel="#nodes")

    plotter.scatter(
        results.time_alloc_hrs, results.time_wasted_hrs,
        title="Time Wastage compared to Queueing",
        ylabel="Wall Clock Allocation Wasted",
        xlabel="Time Spent Queueing")

    # plotter.heatmap(
    #     results.usage_matrix,
    #     xlabel="#nodes",
    #     title="Queue time by runtime and nodes",
    #     cbarlabel="Average queue time"
    # )

    console.print(f"Results saved in {folder}.", style="bright_green")

if __name__ == "__main__":
    app()