import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import sys

arg = sys.argv[-1]
if arg=="small":
    df = pd.read_csv("benchmark_results_small.csv")
else:
    df = pd.read_csv("benchmark_results_complete.csv")

points_per_alphabeta = {}

for index, row in df.iterrows():
    if row.fname1.split('_')[1]!="alphabeta" or row.fname2.split('_')[1]!="alphabeta":
        continue
    alpha = row.alphas1
    beta = row.betas1
    if (alpha,beta) not in points_per_alphabeta.keys():
        points_per_alphabeta[(alpha,beta)] = {}

    if row.nnodes_network1 not in points_per_alphabeta[(alpha,beta)].keys():
        points_per_alphabeta[(alpha,beta)][row.nnodes_network1] = []

    if not np.isnan(row.runtime):
        points_per_alphabeta[(alpha,beta)][row.nnodes_network1].append(row.runtime)

fig, ax = plt.subplots(figsize=(7,3.5))
for alphabeta, data in points_per_alphabeta.items():
    xs = sorted(data.keys())
    means = [np.mean(data[key]) for key in xs]
    stds = [np.std(data[key])/np.sqrt(len(data[key])) for key in xs]

    plt.errorbar(xs, means, yerr=stds, fmt='o-', capsize=5,label="(alpha,beta) = "+str(alphabeta))

plt.yscale('log')
plt.xlabel('number of vertices in networks',fontsize=12)
plt.ylabel('computation time (seconds)',fontsize=12)
plt.legend()
plt.savefig("rtime_against_n_various_alphabeta.pdf",bbox_inches='tight')
plt.show()
