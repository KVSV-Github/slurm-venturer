import pandas as pd

from slurm_venturer.lib.providers.DataProvider import DataProvider
from slurm_venturer.lib.utils import hash

class CSVProvider(DataProvider):

    def __init__(self, data_source):
        self.data_source = data_source

    def get_data(self, user):    
        data = pd.read_csv(self.data_source,
                        sep=",",
                        index_col="JobID"
            )

        if user != None:
            data = data[data["UID"] == hash(user)]

        return data