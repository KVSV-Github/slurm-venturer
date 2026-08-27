from pytest import skip, approx
from slurm_venturer.lib.utils import slurm_memory_gb
import pandas as pd

class TestParseMemory:
    def test_identity(self):
        assert slurm_memory_gb("32G") == 32

    def test_null(self):
        assert pd.isna(slurm_memory_gb(""))

    def test_kb(self):
        assert approx(slurm_memory_gb("6815808K")) == 6.815808

    def test_mb(self):
        assert approx(slurm_memory_gb("6505M")) == 6.505