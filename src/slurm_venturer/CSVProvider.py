import pandas as pd
from slurm_venturer.DataProvider import DataProvider

class CSVProvider(DataProvider):

    def __init__(self, data_source):
        self.data_source = data_source

    def get_data(self, user):    
        data = pd.read_csv(self.data_source,
                        sep=",",
                        index_col="JobID"
            )

        data = data[data["UID"] == user]

        return data