import pandas as pd
import io
import subprocess

from slurm_venturer.lib.clean_data import clean_data
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
        "--format=JobID,UID,JobName,ElapsedRaw,TimelimitRaw,TotalCPU,CPUTimeRAW,Planned,NNodes,NCPUS,MaxRSS,ReqMem",
        user_flag,
        "-P"
        ], stdout=subprocess.PIPE, text=True)
    
        
        
        data = pd.read_csv(io.StringIO(res.stdout),
                        sep="|",
                        index_col="JobID"
            )


        data = clean_data(data)
        
        

        return data