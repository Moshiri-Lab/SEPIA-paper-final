"""
Version 1 of make_violinplots.py, using SEPIA.py

This script creates 9 violin plot figures in the specified FIGURES_DIR, each with with 2 violin plots.
Each figure represents an experimental condition, and each of the 2 plots represent either ProACT
or HIV-TRACE. To use the script, run "make_violinplots1.py [METRIC_CHOICE]".
"""

from subprocess import check_output
import sys

import matplotlib.pyplot as plt
from seaborn import violinplot
import pandas as pd
import scipy.stats as stats 


# CONSTANTS  ------------------------------------------------------------------------------------------------

# Parameters of choice
START_TIME = 9
METRIC_CHOICE = sys.argv[1] # Keyboard input for metric

# EXPERIMENTS = ['SAMPLE-FIRSTART_ARTRATE-4']
EXPERIMENTS = ['SAMPLE-FIRSTART_ARTRATE-4','SAMPLE-FIRSTART_ARTRATE-2','SAMPLE-FIRSTART_ARTRATE-1',
'SAMPLE-FIRSTART_STOPRATE-0.25x','SAMPLE-FIRSTART_STOPRATE-0.5x','SAMPLE-FIRSTART_STOPRATE-2x',
'SAMPLE-FIRSTART_STOPRATE-4x','SAMPLE-FIRSTART_EXPDEGREE-20','SAMPLE-FIRSTART_EXPDEGREE-30']

# Directories to access
SIMS_DIR = 'simulations/'
FIGURES_DIR = 'figs/'
# File names/formatting
TRANSMISSIONFMT = ".transmissions.txt.gz"
CONTACTNETFMT = '.contacts.txt.gz'
PROACTFMT = ".time9.ft.mv.proact.txt.gz"
HIVTRACEFMT = ".time9.tn93.hivtrace.growth.ordering.txt.gz"
INTERMEDIATEFILE = "intermediate_file_violinplot.txt" # file where output of compute efficacy is saved
algorithms = [PROACTFMT, HIVTRACEFMT]

# Strings/colors for formatting graphs
algorithmNames = { PROACTFMT : "ProACT", HIVTRACEFMT : "HIV-TRACE" }
colors = { "ProACT" : '#000080', "HIV-TRACE" : '#ffb500'}
FONT = "Georgia"

x_labels = {
'SAMPLE-FIRSTART_ARTRATE-1': r' $3$',
'SAMPLE-FIRSTART_ARTRATE-2': r' $2$',
'SAMPLE-FIRSTART_ARTRATE-4': r' $1$',
'SAMPLE-FIRSTART_STOPRATE-0.25x': r' $4$',
'SAMPLE-FIRSTART_STOPRATE-0.5x': r' $5$',
'SAMPLE-FIRSTART_STOPRATE-2x': r' $6$',
'SAMPLE-FIRSTART_STOPRATE-4x': r' $7$',
'SAMPLE-FIRSTART_EXPDEGREE-20': r' $8$',
'SAMPLE-FIRSTART_EXPDEGREE-30': r' $9$',
'SAMPLE-END_ARTRATE-1': r' $E_{d}=10$, $\lambda_{+}=1$, $\lambda_{-}=1x$ (End)',
'SAMPLE-END_ARTRATE-2': r' $E_{d}=10$, $\lambda_{+}=2$, $\lambda_{-}=1x$ (End)',
'SAMPLE-END_ARTRATE-4': r' $E_{d}=10$, $\lambda_{+}=4$, $\lambda_{-}=1x$ (End)',
}

"""
x_labels = {
'SAMPLE-FIRSTART_ARTRATE-1': r' $E_{d}=10$, $\lambda_{+}=1$, $\lambda_{-}=1x$',
'SAMPLE-FIRSTART_ARTRATE-2': r' $E_{d}=10$, $\lambda_{+}=2$, $\lambda_{-}=1x$',
'SAMPLE-FIRSTART_ARTRATE-4': r' $E_{d}=10$, $\lambda_{+}=4$, $\lambda_{-}=1x$',
'SAMPLE-FIRSTART_STOPRATE-0.25x': r' $E_{d}=10$, $\lambda_{+}=1$, $\lambda_{-}=0.25x$',
'SAMPLE-FIRSTART_STOPRATE-0.5x': r' $E_{d}=10$, $\lambda_{+}=1$, $\lambda_{-}=0.5x$',
'SAMPLE-FIRSTART_STOPRATE-2x': r' $E_{d}=10$, $\lambda_{+}=1$, $\lambda_{-}=2x$',
'SAMPLE-FIRSTART_STOPRATE-4x': r' $E_{d}=10$, $\lambda_{+}=1$, $\lambda_{-}=4x$',
'SAMPLE-FIRSTART_EXPDEGREE-20': r' $E_{d}=20$, $\lambda_{+}=1$, $\lambda_{-}=1x$',
'SAMPLE-FIRSTART_EXPDEGREE-30': r' $E_{d}=30$, $\lambda_{+}=1$, $\lambda_{-}=1x$',
'SAMPLE-END_ARTRATE-1': r' $E_{d}=10$, $\lambda_{+}=1$, $\lambda_{-}=1x$ (End)',
'SAMPLE-END_ARTRATE-2': r' $E_{d}=10$, $\lambda_{+}=2$, $\lambda_{-}=1x$ (End)',
'SAMPLE-END_ARTRATE-4': r' $E_{d}=10$, $\lambda_{+}=4$, $\lambda_{-}=1x$ (End)',
}
"""


def calculateTauSimulation(transmissionFile: str, contactNetFile: str, experiment: str, intStr: str, algm: str) -> float:
	"""
	Helper method for calculating the Tau value for a certain simulation.

	Parameters
	----------
	transmissionFile - Name of file containing transmission data
	experiment - Name of the experimental condition
	intStr - The specific "number" associated with this simulation
	algm - Current algorithm being evaluated (such as ProACT/HIV-TRACE)
	"""

	# Form the names of required files
	inputFile = SIMS_DIR + experiment + "/" + intStr + algm

	# Run SEPIA with inputFile and outputFile

	bashCommand = "python SEPIA.py -m " + str(METRIC_CHOICE) + " -i " + inputFile + " -t " + transmissionFile + " -c " + contactNetFile + " -s " + str(START_TIME)
	return float(check_output(bashCommand.split()).decode().split('\t')[0])


# MAIN SCRIPT  -----------------------------------------------------------------------------------------

# Initializing our dataframe
cols = ['Experiment', 'Tau','Algorithm']
df = pd.DataFrame(columns = cols)


# Iterate through experiments
for experiment in EXPERIMENTS:

	# Iterate over algorithms, PROACT then HIV-TRACE
	for a in algorithms:

		# For plotting the violin for a in this experiment
		x = [] # Denotes which prioritization method was used per Tau-b value
		y = [] # Tau-b values

		# Iterate over all 20 simulations per experiment
		for i in range(1,21):

			# Convert i into a str for the file names
			intStr = ''
			if i < 10:
				intStr = "0" + str(i)
			else:
				intStr = str(i)

			fileFormatStr = SIMS_DIR + experiment + "/" + intStr
			transmissionFile = fileFormatStr + TRANSMISSIONFMT
			contactNetFile = fileFormatStr + CONTACTNETFMT

			# Calculate tau for this simulation w/ ProACT
			tau = calculateTauSimulation(transmissionFile, contactNetFile, experiment, intStr, a)

			temp = pd.DataFrame([[x_labels[experiment], tau, algorithmNames[a]]], columns= cols)
			df = df.append(temp)

		# End algorithm for-loop

	# End experiment for loop


# Make the violin plot for all simulations 
ax = violinplot(x="Experiment", y="Tau", hue="Algorithm", data=df, dodge=False, palette=colors)

# Format graph
#ax.set_xticklabels(ax.get_xticklabels(), horizontalalignment='right')
ax.set_ylim([-0.01, 0.15])
ax.set_xticklabels(ax.get_xticklabels())
plt.xticks(rotation=0)
ax.set_ylabel("Kendall's Tau-b", fontname=FONT, fontsize=13)
ax.set_xlabel("Simulation Number", fontname=FONT, fontsize=13)
plt.legend(prop={'family':FONT, 'size':12})
bottom, top = plt.ylim()
plt.ylim(top=(top + 0.022))  # adjust the top leaving bottom unchanged
plt.tight_layout()

# Save the fig automatically
fig = ax.get_figure(); fig.savefig(FIGURES_DIR + 'm' + str(METRIC_CHOICE) + '_tau' + '.pdf', format='pdf')
plt.clf() # Clear current figure window


# BASH CODE --------------------------------------------------------------------------------------------

# Example for how make_violinplot runs SEPIA.py
# python SEPIA.py -i simulations/SAMPLE-FIRSTART_ARTRATE-4/01.time9.ft.mv.proact.txt.gz -t simulations/SAMPLE-FIRSTART_ARTRATE-4/01.transmissions.txt.gz -s 9 -m 3.2 -o out.txt

# Bash for running all this script on all metrics
# for i in $(seq 1 2 3 4 5 6); do python make_violinplots.py $i; done
