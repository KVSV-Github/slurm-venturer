import hashlib
from slurm_venturer.lib.utils import slurm_seconds

def clean_data(data):
    data = data[data["ElapsedRaw"] > 0]
    data = data[data["Planned"].notna()]

    data["TimelimitRaw"] *= 60 # is in minutes for whatever reason
    data["TotalCPU"] = data["TotalCPU"].map(slurm_seconds)
    data["Planned"] = data["Planned"].map(slurm_seconds)
        
    data["JobName"] = data["JobName"].apply(
        lambda x:
            hashlib.md5(x.encode()).hexdigest()
    )
    data["sbatch"] = data["TimelimitRaw"].notna()

    return data