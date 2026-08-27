# Slurm Venturer

A tool for analysing the efficiency of slurm clusters. Similar to seff, but for aggregate jobs over a period of time.

## Description

Allows any user with access to the `sacct` command in Slurm to collect data on jobs from all users, or one specific user. Creates graphs to show:
- Distribution of time allocated to jobs
- Distribution of job run time
- Distribution of job CPU efficiency
- Distribution of job memory usage
- [Scheduling Coefficient Matrix](https://www.archer2.ac.uk/support-access/status.html#:~:text=Queue%20length%20data,-The)
- Wall Time Wastage Matrix (same layout as scheduling coefficient, but shows [time allocated] - [time elapsed])

These should prove useful to examine the nature of jobs on a cluster. Because downloading and analysing (creating graphs) is split into two commands, this tool is also useful for getting data from `sacct` in a format that can easily be parsed by something along the lines of `pd.readcsv()`, for any specific research that needs to be done.

Job names and user IDs are hashed in order to anonymise data that may be sensitive. This tool works specifically on jobs that successfully finished with the state "COMPLETED".

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
