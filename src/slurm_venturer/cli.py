import subprocess
import pandas as pd
import io
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from datetime import datetime
import os

def main():
    print("Slurm Venturer")
    res = subprocess.run(["sacct",
    "-S", "today",
    "-E", "now",
    "--state=COMPLETED,TIMEOUT",
    "--format=JobID,ElapsedRaw,TimelimitRaw",
    "--allusers",
    "-P"
    ], stdout=subprocess.PIPE, text=True)

    
    
    data = pd.read_csv(io.StringIO(res.stdout),
                sep="|",
                index_col="JobID"
                )
    data.dropna(inplace=True)
    data = data[data["ElapsedRaw"] > 0]
    data["TimelimitRaw"] *= 60 # is in minutes for whatever reason
    data["utilisation"] = data["ElapsedRaw"] / data["TimelimitRaw"]
    print(data)

    folder = "results/" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(os.path.dirname(folder), exist_ok=True)

    plt.hist([data["utilisation"]], bins=20)
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1.0))

    plt.xlabel("Utilisation")
    plt.ylabel("Number of jobs")
    plt.title("Slurm job time utilisation")

    plt.savefig(folder + "time_distrib.png")