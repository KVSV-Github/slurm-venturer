import pandas as pd
import numpy as np

class Results:
    def __init__(self, data):
        self.data = data
        self.sbatch_data = self.data[self.data["sbatch"]]
        self.timebins = [
            0,
            0.25 * 3600,
            0.5 * 3600,
            3600,
            3 * 3600,
            6 * 3600,
            12 * 3600,
            24 * 3600
        ]
        self.timelabels = [
            "0-15mins",
            "15-30mins",
            "30mins-1hr",
            "1-3hrs",
            "3-6hrs",
            "6-12hrs",
            "12-24hrs"
        ]
        self.nodebins = [
            1,
            2,
            3,
            4,
            8,
            16,
            32,
            float("inf")
        ]
        self.nodelabels = [
            "1",
            "2",
            "3",
            "4-7",
            "8-15",
            "16-31",
            "32+"
        ]

        self.runtime_bins = pd.cut(
            self.sbatch_data["ElapsedRaw"],
            bins=self.timebins,
            labels=self.timelabels,
            right=False
        )
        self.allocated_bins = pd.cut(
            self.sbatch_data["TimelimitRaw"],
            bins=self.timebins,
            labels=self.timelabels,
            right=False
        )
        self.node_bins = pd.cut(
            self.sbatch_data["NNodes"],
            bins=self.nodebins,
            labels=self.nodelabels,
            right=False
        )

    @property
    def time_util_matrix(self):
        data = self.sbatch_data.copy()
        data["util"] = (data["TimelimitRaw"] - data["ElapsedRaw"]) / 3600
        group = (
            data.assign(
                runtime_bins=self.runtime_bins,
                node_bin=self.node_bins
            )
            .groupby(["runtime_bins", "node_bin"], observed=False)["util"]
        )
        coeff = group.median().unstack()
        count = group.size().unstack(fill_value=0)

        return coeff, count

    # @property
    # def time_util_hrplus(self):
    #     data = self.sbatch_data[self.sbatch_data["ElapsedRaw"] >= 3600]
    #     return data["ElapsedRaw"] / data["TimelimitRaw"]

    # @property
    # def time_util_lesshr(self):
    #     data = self.sbatch_data[self.sbatch_data["ElapsedRaw"] < 3600]
    #     return data["ElapsedRaw"] / data["TimelimitRaw"]

    @property
    def scheduling_coeff(self):
        data = self.sbatch_data.copy()
        data["scheduling_coeff"] = data["ElapsedRaw"] / (data["ElapsedRaw"] + data["Planned"])
        group = (
            data.assign(
                runtime_bin=self.runtime_bins,
                node_bin=self.node_bins
            )
            .groupby(["runtime_bin", "node_bin"], observed=False)["scheduling_coeff"]
        )
        coeff = group.mean().unstack()
        count = group.size().unstack(fill_value=0)

        return coeff, count
    
    # @property
    # def time_util(self):
    #     return self.sbatch_data["ElapsedRaw"] / self.sbatch_data["TimelimitRaw"]

    @property
    def time_elapsed_hrs(self):
        return self.sbatch_data["ElapsedRaw"] / 3600

    @property
    def time_alloc_hrs(self):
        return self.sbatch_data["TimelimitRaw"] / 3600

    @property
    def time_queueing_hrs(self):
        return self.sbatch_data["Planned"] / 3600

    @property
    def time_wasted_hrs(self):
        return (self.sbatch_data["TimelimitRaw"] - self.sbatch_data["ElapsedRaw"]) / 3600

    @property
    def cpu_util(self):
        return self.sbatch_data["TotalCPU"] / self.sbatch_data["CPUTimeRAW"]

    @property
    def mem_util(self):
        return self.sbatch_data["MaxRSS"] / self.sbatch_data["ReqMem"]
