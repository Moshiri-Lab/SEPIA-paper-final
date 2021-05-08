# SEPIA-paper-final
SEPIA (Simulation-based Evaluation Of PriorIzation Algorithms)

## Overview of Contents
- __[`helper_scripts/make_violinplots.py`](helper_scripts/make_violinplots.py)__ - creates 9 violin plot figures in ```figures/```, each with with 2 violin plots. Each figure represents an experimental condition, and each of the 2 plots represent either ProACT or HIV-TRACE.

```
usage: [METRIC]
 METRIC			The number of the metric you want to generate violin plots for with the data
```

- __[`figures/`](figures)__ - holds figures used in the SEPIA paper, including the violin plots

## Reproducing the SEPIA Paper Results
The SEPIA manuscript utilizes the simulated data used in the ProACT manuscript:

https://github.com/niemasd/ProACT-Paper-Final/tree/master/simulations

Note that SEPIA can use *any* dataset produced by [FAVITES](https://github.com/niemasd/FAVITES): we just happened to reuse this dataset in the SEPIA manuscript. SEPIA itself is completely generalizable to any simulation conditions.

To redo the analyses conducted in the SEPIA manuscript as well as to reproduce the figures in the manuscript, simply do the following:

1. Download and extract a [zip](https://github.com/niemasd/ProACT-Paper-Final/archive/refs/heads/master.zip) of the [ProACT-Paper-Final repo](https://github.com/niemasd/ProACT-Paper-Final)
2. Download [`SEPIA.py`](https://github.com/Niema-Lab/SEPIA/blob/master/SEPIA.py) and place it within the extracted folder
3. Download [`make_violinplots.py`](helper_scripts/make_violinplots.py) and place it within the extracted folder
4. Run [`make_violinplots.py`](helper_scripts/make_violinplots.py): `python3 make_violinplots.py <metric>`
    * To automate running on all metrics: `for m in $(seq 1 6) ; do python3 make_violinplots.py $m ; done`
