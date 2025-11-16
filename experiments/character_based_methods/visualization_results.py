import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import os
import numpy as np

df = pd.read_csv("results_alitzel_data_experiment1.csv")


N = len(os.listdir("./networks/"))

data = np.zeros((N,N))

keys = [s.split('.')[0] for s in os.listdir("./networks/")]
keys = sorted(["_".join([s.split('_')[1],s.split('_')[0]]) for s in keys])

print(keys)

results_dict = {}

for row in df.itertuples(): 
    print(row)
    fname1 = row.fname1.split('.')[0]
    fname1 = "_".join([fname1.split('_')[1],fname1.split('_')[0]])

    fname2 = row.fname2.split('.')[0]
    fname2 = "_".join([fname2.split('_')[1],fname2.split('_')[0]])

    results_dict[(fname1,fname2)] = int(row.distance)

for k1, fname1 in enumerate(keys):
    for k2, fname2 in enumerate(keys):
        data[k1,k2] = results_dict[(fname1,fname2)]

sns.heatmap(data,xticklabels=keys,yticklabels=keys,cbar_kws={"label":"distance value"})
plt.show()
