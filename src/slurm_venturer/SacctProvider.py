import pandas as pd
import io
import subprocess
import hashlib

from slurm_venturer.utils import slurm_seconds
from slurm_venturer.DataProvider import DataProvider

class SacctProvider(DataProvider):
    def get_data(self, user):
        user_flag = "--allusers"
        if user != None: user_flag = f"--uid={user}"
        res = subprocess.run(["sacct",
        "-S", "today",
        "-E", "now",
        "--state=COMPLETED",
        "--format=JobID,UID,JobName,ElapsedRaw,TimelimitRaw,TotalCPU,CPUTimeRAW",
        user_flag,
        "-P"
        ], stdout=subprocess.PIPE, text=True)
    
        
        
        data = pd.read_csv(io.StringIO(res.stdout),
                        sep="|",
                        index_col="JobID"
            )

        print(f"Dropping {data.isna().sum().sum()} empty rows...")
        data.dropna(inplace=True)
        data = data[data["ElapsedRaw"] > 0]


        
        data["JobName"] = data["JobName"].apply(
            lambda x:
                hashlib.md5(x.encode()).hexdigest()
        )
        data["TimelimitRaw"] *= 60 # is in minutes for whatever reason
        data["TotalCPU"] = data["TotalCPU"].map(slurm_seconds)

        return data