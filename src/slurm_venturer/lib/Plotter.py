import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd

from slurm_venturer.lib.utils import create_folder

class Plotter:
    def __init__(self, folder):
        self.folder = folder

    def distribution(self, data, *,
        title,
        xlabel,
        bins=100,
        percentage=True,
    ):
        fig, ax = plt.subplots()

        ax.hist(data, bins=bins)

        if percentage:
            ax.xaxis.set_major_formatter(PercentFormatter(1.0))

        ax.set_xlabel(xlabel)
        ax.set_ylabel("Number of jobs")
        ax.set_title(title)

        fig.tight_layout()
        fig.savefig(create_folder(self.folder / "histograms") / f"{title}.png")
        plt.close(fig)

    def heatmap(self, data, jobcount, *,
        title,
        xlabel,
        ylabel,
        cbarlabel
    ):
        fig, ax = plt.subplots()
        im = ax.imshow(data, cmap="coolwarm", aspect="auto")

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                value = str(jobcount.iloc[i, j])

                ax.text(
                    j, i,
                    f"{value}",
                    ha="center",
                    va="center"
                )

        ax.set_xticks(
            range(len(data.columns)),
            data.columns
        )
        ax.set_yticks(
            range(len(data.index)),
            data.index
        )

        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.set_title(title)

        fig.tight_layout()
        fig.savefig(create_folder(self.folder / "heatmaps") / f"{title}.png")
        plt.close(fig)

    def scatter(self, x, y, *, title, xlabel, ylabel):
        fig, ax = plt.subplots()
        ax.scatter(x, y, linewidth=0, s=2)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(create_folder(self.folder / "scatters") / f"{title}.png")
        plt.close(fig)
