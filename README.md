# SEPIA-paper-final
SEPIA (Simulation-based Evaluation Of PriorIzation Algorithms)

- __helper_scripts/make_violinplots.py__ - creates 9 violin plot figures in ```figures/```, each with with 2 violin plots. Each figure represents an experimental condition, and each of the 2 plots represent either ProACT or HIV-TRACE.

```
usage: [METRIC]
 METRIC			The number of the metric you want to generate violin plots for with the data
```

- __figures/__ - holds figures used in the SEPIA paper, including the violin plots

The SEPIA manuscript utilizes the simulated data used in the ProACT manuscript:

https://github.com/niemasd/ProACT-Paper-Final/tree/master/simulations

Note that SEPIA can use *any* dataset produced by [FAVITES](https://github.com/niemasd/FAVITES): we just happened to reuse this dataset in the SEPIA manuscript. SEPIA itself is completely generalizable to any simulation conditions.
