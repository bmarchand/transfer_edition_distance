import json
import time
import os
from ted_module import transfer_edition_distance
import pandas as pd

reference_results = {} 

try:
    df = pd.read_csv("benchmark_results_reference.csv")
    for line in df.itertuples():
        reference_results[(line.fname1, line.fname2)] = line.runtime, line.distance
except:
    pass
print(reference_results)

max_N = 1000000             # no limit
num_of_networks = 500

network_size = {}
nleaves = {}

random_network_dir = "level_k_lgt_generator/random_lgt_networks/"

def list_leaves(fname):
    out_ngbh = {}
    for line in open(fname).readlines()[1:]:
        u = line.split(' ')[0]
        v = line.split(' ')[1].rstrip('\n')

        try:
            out_ngbh[u]
        except KeyError:
            out_ngbh[u] = []
        try:
            out_ngbh[v]
        except KeyError:
            out_ngbh[v] = []

        out_ngbh[u].append(v)

    return sorted([int(u) for u, ngbh in out_ngbh.items() if len(ngbh)==0])

import json
with open("level_k_lgt_generator/level_dict.json") as f:
    level_dict = json.load(f)


for fname in os.listdir(random_network_dir):
    if fname=="folder.keep":
        continue
    first_line = open(random_network_dir+fname).readlines()[0]
    nvertices = first_line.split(' ')[2]
    network_size[fname] = int(nvertices)
    nleaves[fname] = len(list_leaves(random_network_dir+fname))

def extract_info(fname):
    n = fname.split('_')[1][1:]
    alpha = fname.split('_')[2][5:]
    beta = fname.split('_')[3][4:]
    return n,alpha,beta

names1 = []
names2 = []

nsteps1 = []
nsteps2 = []

alphas1 = []
alphas2 = []

betas1 = []
betas2 = []

levels1 = []
levels2 = []

nnodes_network1 = []
nnodes_network2 = []

nleaves_network1 = []
nleaves_network2 = []

ntransfers_network1 = []
ntransfers_network2 = []

runtime = []

distance = []

print("starting to run things")
print(level_dict)

for fname1 in os.listdir(random_network_dir):
    if fname1=="folder.keep":
        continue
    for fname2 in os.listdir(random_network_dir):
        if fname2=="folder.keep":
            continue


        nleaves1 = nleaves[fname1] 
        nleaves2 = nleaves[fname2]

        nnodes1 = network_size[fname1]
        nnodes2 = network_size[fname2]

        if nleaves1==nleaves2 and nnodes1 < max_N and nnodes2 < max_N:
            print(fname1,fname2)

            L1 = open(random_network_dir+fname1).readlines()[1:]
            L2 = open(random_network_dir+fname2).readlines()[1:]
            L1 = [l.rstrip('\n') for l in L1]
            L2 = [l.rstrip('\n') for l in L2]

            t0 = time.time()
            d = transfer_edition_distance(L1,L2)
            runtime.append(time.time() - t0)
            distance.append(d)

            try:
                print(d,reference_results[(fname1,fname2)][1])
                assert(d==reference_results[(fname1,fname2)][1])
            except KeyError:
                pass

            nnodes_network1.append(network_size[fname1])
            nnodes_network2.append(network_size[fname2])

            nleaves_network1.append(nleaves1)
            nleaves_network2.append(nleaves2)

            ntransfers1 = len([l for l in open(random_network_dir+fname1).readlines()[1:] if l.find("transfer") >= 0])
            ntransfers2 = len([l for l in open(random_network_dir+fname2).readlines()[1:] if l.find("transfer") >= 0])

            ntransfers_network1.append(ntransfers1)
            ntransfers_network2.append(ntransfers2)

            names1.append(fname1)
            names2.append(fname2)

            n1,alpha1,beta1 = extract_info(fname1)
            n2,alpha2,beta2 = extract_info(fname2)

            levels1.append(level_dict['random_lgt_networks/'+fname1])
            levels2.append(level_dict['random_lgt_networks/'+fname2])

            nsteps1.append(n1)
            nsteps2.append(n2)

            alphas1.append(alpha1)
            alphas2.append(alpha2)

            betas1.append(beta1)
            betas2.append(beta2)

d = {
    'fname1' : names1,
    'fname2' : names2,
    'nsteps1' : nsteps1,
    'nsteps2' : nsteps2,
    'alphas1' : alphas1,
    'alphas2' : alphas2,
    'betas1' : betas1,
    'betas2' : betas2,
    'levels1' : levels1,
    'levels2' : levels2,
    'nnodes_network1' : nnodes_network1,
    'nnodes_network2' : nnodes_network2,
    'nleaves_network1' : nleaves_network1,
    'nleaves_network2' : nleaves_network2,
    'ntransfers_network1' : ntransfers_network1,
    'ntransfers_network2' : ntransfers_network2,
    'distance': distance,
    'runtime' : runtime
        }

df = pd.DataFrame(data=d)
print(df)
df.to_csv("benchmark_results.csv")
