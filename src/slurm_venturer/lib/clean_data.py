from slurm_venturer.lib.utils import slurm_seconds, slurm_memory_gb
from slurm_venturer.lib.utils import hash

def clean_data(data):
    data = data[data["ElapsedRaw"] > 0]
    data = data[data["Planned"].notna()]

    data["TimelimitRaw"] *= 60 # is in minutes for whatever reason
    data["TotalCPU"] = data["TotalCPU"].map(slurm_seconds)
    data["Planned"] = data["Planned"].map(slurm_seconds)

    data["MaxRSS"] = data["MaxRSS"].map(slurm_memory_gb)
    data["REQMEM"] = data["REQMEM"].map(slurm_memory_gb)
        
    data["JobName"] = data["JobName"].map(hash)
    data["UID"] = data["JobName"].map(hash)
    data["sbatch"] = data["TimelimitRaw"].notna()

    return data