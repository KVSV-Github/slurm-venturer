class Results:
    def __init__(self, data):
        self.data = data

    @property
    def time_util(self):
        return self.data["ElapsedRaw"] / self.data["TimelimitRaw"]

    @property
    def cpu_util(self):
        return self.data["TotalCPU"] / self.data["CPUTimeRAW"]
