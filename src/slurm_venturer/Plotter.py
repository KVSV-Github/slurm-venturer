import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

class Plotter:
    def __init__(self, results, folder):
        self.results = results
        self.folder = folder

    def distribution(
        self,
        data,
        *,
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