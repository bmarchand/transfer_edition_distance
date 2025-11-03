import pandas as pd
import numpy as np
import matplotlib.pylab as plt

df = pd.read_csv("benchmark_results.csv")

points_per_alphabeta = {}

for index, row in df.iterrows():
    alpha = row.alphas1
    beta = row.betas1
    if (alpha,beta) not in points_per_alphabeta.keys():
        points_per_alphabeta[(alpha,beta)] = {}

    if row.nnodes_network1 not in points_per_alphabeta[(alpha,beta)].keys():
        points_per_alphabeta[(alpha,beta)][row.nnodes_network1] = []

    if not np.isnan(row.runtime):
        points_per_alphabeta[(alpha,beta)][row.nnodes_network1].append(row.runtime)

for alphabeta, data in points_per_alphabeta.items():
    xs = sorted(data.keys())
    means = [np.mean(data[key]) for key in xs]
    stds = [np.std(data[key])/np.sqrt(len(data[key])) for key in xs]

    plt.errorbar(xs, means, yerr=stds, fmt='o-', capsize=5,label="(alpha,beta) = "+str(alphabeta))

plt.yscale('log')
plt.xlabel('number of nodes in networks')
plt.ylabel('computation time (seconds)')
plt.legend()
plt.savefig("rtime_against_n_various_alphabeta.pdf"
plt.show()
