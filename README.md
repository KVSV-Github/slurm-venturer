# Slurm Venturer

A tool for analysing the efficiency of slurm clusters. Similar to seff, but for aggregate jobs over a period of time.

## Installation

Clone the repo and run `pip install -e .` from the root folder. This will install the tool and add it to your path. You can test this by running `slurm-venturer`. You should see some help text.

## Usage

For more information run `slurm-venturer COMMAND --help`.

|Command|Description|
|-|-|
|`slurm-venturer download [options]` |Download, parse, and save accounting data from slurm.
|`slurm-venturer analyse [options]` |Create graphs and analytical results from data file.|

## Examples

Download data from the last 7 days, and then create graphs.

```bash
$ slurm-venturer download -s now-7days --out ./data/
$ slurm-venturer analyse --data ./data/[timestampedfolder]/data.csv
```

## Gallery

![Scheduling Coefficient Matrix](/images/heatmaps/Scheduling%20Coefficient%20Matrix.png)
![Wall Clock Wastage Matrix](/images/heatmaps/Wall%20Clock%20Wastage%20Matrix.png)
![CPU Utilisation](/images/histograms/Slurm%20CPU%20Utilisation.png)
![Job Time Allocated](/images/histograms/Slurm%20Time%20Allocated.png)
![Job Time Elapsed](/images/histograms/Slurm%20Time%20Elapsed.png)

## Contributors

- Robert Kvasov