import pandas as pd
import numpy as np
import matplotlib.pylab as plt

df = pd.read_csv("benchmark_results.csv")

points_per_alpha = {}

for index, row in df.iterrows():
    alpha = row.alphas1
    if alpha not in points_per_alpha.keys():
        points_per_alpha[alpha] = {}

    if row.nnodes_network1 not in points_per_alpha[alpha].keys():
        points_per_alpha[alpha][row.nnodes_network1] = []

    if not np.isnan(row.runtime):
        points_per_alpha[alpha][row.nnodes_network1].append(row.runtime)

for alpha, data in points_per_alpha.items():
    xs = sorted(data.keys())
    means = [np.mean(data[key]) for key in xs]
    stds = [np.std(data[key])/np.sqrt(len(data[key])) for key in xs]

    plt.errorbar(xs, means, yerr=stds, fmt='o-', capsize=5,label="alpha = "+str(alpha))

plt.yscale('log')
plt.xlabel('number of nodes in networks')
plt.ylabel('computation time (seconds)')
plt.legend()
plt.show()
