import sys
import copy

num_reconc = int(sys.argv[-3])
species_tree_gr = sys.argv[-2]
ranger_dtl_out = sys.argv[-1]

species_tree_adj = {}
parent = {}
for line in open(species_tree_gr).readlines()[1:]:
    u = int(line.split(" ")[0])
    v = int(line.split(" ")[1])
    parent[v] = u
    if u in species_tree_adj.keys():
        species_tree_adj[u].append(v)
    else:
        species_tree_adj[u] = [v]
    if v not in species_tree_adj.keys():
        species_tree_adj[v] = []

weighted_transfers = {}  # associates to a pair of nodes the number of times it is used

for j in range(num_reconc):
    for line in open(ranger_dtl_out+str(j)).readlines():
        if line.find("Transfer,") >= 0:
            source = int(line.split(" ")[-4].rstrip(','))
            dest = int(line.split(" ")[-1].rstrip('\n'))
            try:
                weighted_transfers[(source,dest)] += 1/float(num_reconc)
            except KeyError:
                weighted_transfers[(source,dest)] = 1/float(num_reconc)

#print(species_tree_adj, source,dest)

subdivided = {} # associates to a node the subdivided vertex
# on the edge between it and its parent.

N = max(species_tree_adj.keys())+1

transfer_edges = []

for u,v in weighted_transfers.keys():
    if u in subdivided.keys():
        w = subdivided[u]
    else:
        species_tree_adj[N] = [u]
        parent[N] = parent[u]
        species_tree_adj[parent[u]] = [x for x in species_tree_adj[parent[u]] if x!= u]
        species_tree_adj[parent[u]].append(N)
        w = copy.copy(N)
        subdivided[u] = w
        N += 1

    if v in subdivided.keys():
        x = subdivided[v]
    else:
        species_tree_adj[N] = [v]
        parent[N] = parent[v]
        species_tree_adj[parent[v]] = [y for y in species_tree_adj[parent[v]] if y!= v]
        species_tree_adj[parent[v]].append(N)
        x = copy.copy(N)
        subdivided[v] = x
        N += 1

    transfer_edges.append((w,x,weighted_transfers[(u,v)]))

nnodes = len(species_tree_adj.keys())
nedges = 0
for key, value in species_tree_adj.items():
    for ngbh in value:
        nedges += 1
nedges += len(transfer_edges)

print("nnodes","nedges",nnodes,nedges)

for key, value in species_tree_adj.items():
    for ngbh in value:
        print(key, ngbh, "tree")

for w,x,weight in transfer_edges:
    print(w,x,"transfer",weight)
