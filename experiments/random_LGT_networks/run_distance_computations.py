import json
import numpy as np
import subprocess
import time
import os
#from ted_module import transfer_edition_distance
import pandas as pd


network_size = {}
nleaves = {}

import sys
arg = sys.argv[-1]
small = True
if arg=="complete":
    small = False

random_network_dir = "generated_networks/"

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
with open("level_dict.json") as f:
    level_dict = json.load(f)


for fname in os.listdir(random_network_dir):
    if fname=="folder.keep":
        continue
    first_line = open(random_network_dir+fname).readlines()[0]
    nvertices = first_line.split(' ')[2]
    network_size[fname] = int(nvertices)
    nleaves[fname] = len(list_leaves(random_network_dir+fname))

def extract_info(fname):
    n = fname.split('_')[-4][1:]
    alpha = fname.split('_')[-3][5:]
    beta = fname.split('_')[-2][4:]
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

num_computations_per_alpha_and_n = {}
num_data_points = 100

print("starting to run things")
print(level_dict)

for fname1 in os.listdir(random_network_dir):
    if fname1=="folder.keep":
        continue
    for fname2 in os.listdir(random_network_dir):
        if fname2=="folder.keep":
            continue

        if fname1.split('_')[1]!=fname2.split('_')[1]:
            continue

        nleaves1 = nleaves[fname1] 
        nleaves2 = nleaves[fname2]

        nnodes1 = network_size[fname1]
        nnodes2 = network_size[fname2]

        if nleaves1==nleaves2:
            print("computing distance between",fname1,"and",fname2)

            L1 = open(random_network_dir+fname1).readlines()[1:]
            L2 = open(random_network_dir+fname2).readlines()[1:]
            L1 = [l.rstrip('\n') for l in L1]
            L2 = [l.rstrip('\n') for l in L2]

            n1,alpha1,beta1 = extract_info(fname1)
            n2,alpha2,beta2 = extract_info(fname2)

            if alpha1!=alpha2:
                continue
            if beta1!=beta2:
                continue
            if nnodes1!=nnodes2:
                continue

            command = "../../ted_module/target/release/ted_module".split(" ")
            command.append(random_network_dir+fname1)
            command.append(random_network_dir+fname2)

            t0 = time.time()

            try:
                output = subprocess.check_output(command)
                runtime.append(time.time() - t0)
                d = int(output.split(b" ")[3])
            except subprocess.CalledProcessError:
                print("timeout")
                d = np.nan
                runtime.append(np.nan)

            distance.append(d)

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


            levels1.append(level_dict[random_network_dir+fname1])
            levels2.append(level_dict[random_network_dir+fname2])

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
if small:
    df.to_csv("benchmark_results_small.csv")
else:
    df.to_csv("benchmark_results_complete.csv")
