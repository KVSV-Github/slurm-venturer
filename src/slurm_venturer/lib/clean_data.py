from slurm_venturer.lib.utils import slurm_seconds, slurm_memory_gb
from slurm_venturer.lib.utils import hash

def clean_data(data):
    data = data[data["ElapsedRaw"] > 0]

    # Get the job ID without the step suffix
    data["JobIDRoot"] = data["JobID"].str.split(".").str[0]

    # Convert MaxRSS before aggregating
    data["MaxRSS"] = data["MaxRSS"].map(slurm_memory_gb)

    # Get maximum MaxRSS across all steps for each job
    maxrss = data.groupby("JobIDRoot")["MaxRSS"].max()

    data = data[data["Planned"].notna()] # Removes job steps

    data["MaxRSS"] = data["JobIDRoot"].map(maxrss)

    data["TimelimitRaw"] *= 60 # is in minutes for whatever reason
    data["TotalCPU"] = data["TotalCPU"].map(slurm_seconds)
    data["Planned"] = data["Planned"].map(slurm_seconds)

    data["REQMEM"] = data["REQMEM"].map(slurm_memory_gb)
        
    data["JobName"] = data["JobName"].map(hash)
    data["UID"] = data["UID"].map(hash)
    data["sbatch"] = data["TimelimitRaw"].notna()

    return data