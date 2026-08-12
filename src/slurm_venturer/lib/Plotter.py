import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd

class Plotter:
    def __init__(self, results, folder):
        self.results = results
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
        fig.savefig(self.folder / f"{title}.png")
        plt.close(fig)

    def heatmap(self, data, jobcount, *,
        title,
        xlabel,
        ylabel,
        cbarlabel
    ):
        fig, ax = plt.subplots()
        im = ax.imshow(data, cmap="plasma", aspect="auto")

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
        fig.savefig(self.folder / f"{title}.png")
        plt.close(fig)
