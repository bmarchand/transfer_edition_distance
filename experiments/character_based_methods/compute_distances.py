from ted_module import transfer_edition_distance_unordered
import pandas as pd
import os
import time

runtime = []
distance = []
files1 = []
files2 = []

dir_networks = "./networks/"

cnt = 0 
relabel = {}
for fname in os.listdir(dir_networks):
    for line in open(dir_networks+fname).readlines()[1:]:
        u = line.split(' ')[0]
        v = line.split(' ')[1].rstrip('\n')
        try:
            relabel[u]
        except KeyError:
            relabel[u] = str(cnt)
        cnt += 1
        try:
            relabel[v]
        except KeyError:
            relabel[v] = str(cnt)
        cnt += 1

def list_leaves(fname):
    out_ngbh = {}
    for line in open(fname).readlines()[1:]:
        u = line.split(' ')[0]
        v = line.split(' ')[1]
        kind = line.split(' ')[2].rstrip('\n')

        if kind=='transfer':
            continue
        try:
            out_ngbh[u]
        except KeyError:
            out_ngbh[u] = []
        try:
            out_ngbh[v]
        except KeyError:
            out_ngbh[v] = []

        out_ngbh[u].append(v)

    return sorted([u for u, ngbh in out_ngbh.items() if len(ngbh)==0])


for fname1 in os.listdir("./networks/"):
    for fname2 in os.listdir("./networks/"):
        print(fname1, fname2)
        assert(list_leaves(dir_networks+fname1)==list_leaves(dir_networks+fname2))
        lines1 = open(dir_networks+fname1).readlines()[1:]
        lines2 = open(dir_networks+fname2).readlines()[1:]
        lines1 = [l.rstrip('\n') for l in lines1]
        lines2 = [l.rstrip('\n') for l in lines2]
        lines1 = [" ".join([relabel[l.split(" ")[0]],relabel[l.split(" ")[1]],l.split(" ")[2]]) for l in lines1]
        lines2 = [" ".join([relabel[l.split(" ")[0]],relabel[l.split(" ")[1]],l.split(" ")[2]]) for l in lines2]

        t0 = time.time()
        d = transfer_edition_distance_unordered(lines1,lines2)
        runtime.append(time.time()-t0)
        distance.append(d)
        
        files1.append(fname1)
        files2.append(fname2)

d = {
    'fname1' : files1,
    'fname2' : files2,
    'distance': distance,
    'runtime' : runtime
        }

df = pd.DataFrame(data=d)
print(df)
df.to_csv("results_alitzel_data_experiment1.csv")
