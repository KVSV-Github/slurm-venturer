import pandas as pd
import io
import subprocess
import hashlib

from slurm_venturer.lib.utils import slurm_seconds
from slurm_venturer.lib.providers.DataProvider import DataProvider

class SacctProvider(DataProvider):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_data(self, user):
        user_flag = "--allusers"
        if user != None: user_flag = f"--uid={user}"
        res = subprocess.run(["sacct",
        "-S", self.start,
        "-E", self.end,
        "--reason=None",
        "--state=COMPLETED",
        "--format=JobID,UID,JobName,ElapsedRaw,TimelimitRaw,TotalCPU,CPUTimeRAW,Planned,NNodes,NCPUS",
        user_flag,
        "-P"
        ], stdout=subprocess.PIPE, text=True)
    
        
        
        data = pd.read_csv(io.StringIO(res.stdout),
                        sep="|",
                        index_col="JobID"
            )

        # print(f"Dropping {data.isna().sum().sum()} empty rows...")
        # data.dropna(inplace=True)


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