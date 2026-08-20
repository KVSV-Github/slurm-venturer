from pytest import skip, approx
from slurm_venturer.lib.utils import slurm_seconds

class TestSlurmSeconds:
    def test_one_day(self):
        inp = "1-00:00:00"
        assert approx(slurm_seconds(inp)) == 86400

    def test_14ish_hours(self):
        inp = "14:53:56"
        assert approx(slurm_seconds(inp)) == 53636

    def test_few_minutes(self):
        inp = "00:06:02"
        assert approx(slurm_seconds(inp)) == 362

    def test_zero(self):
        inp = "00:00:00"
        assert approx(slurm_seconds(inp)) == 0