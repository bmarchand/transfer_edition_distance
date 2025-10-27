import sys
import json

species_tree = sys.argv[-2]
gene_tree = sys.argv[-1]

with open(gene_tree) as f:
    gene_tree_root = json.load(f)

queue = [gene_tree_root]

transfers = []

while len(queue) > 0:
    node = queue.pop()
    try:
        child0 = node["_child0"]
        child1 = node["_child1"]
        if child0["transferred"]==1:
#            print("transfer between ",node["reconc"],"and",child0["reconc"]," at ", node["tstamp"], child0["tstamp"])
            transfers.append((node["reconc"],child0["reconc"],node["tstamp"],child0["tstamp"]))
        if child1["transferred"]==1:
#            print("transfer between ",node["reconc"],"and",child1["reconc"]," at ", node["tstamp"], child1["tstamp"])
            transfers.append((node["reconc"],child1["reconc"],node["tstamp"],child1["tstamp"]))
        queue.append(child0)
        queue.append(child1)
    except KeyError:
        pass



adj = {}
parent = {}
list_species_edges = []
for line in open(species_tree).readlines()[1:]:
    u = int(line.split(" ")[0])
    v = int(line.split(" ")[1])
    parent[v] = u
    try:
        adj[u].append(v)
    except KeyError:
        adj[u] = [v]
    list_species_edges.append((u,v))

def correct_reconc(reconc, parent_dict):
    try:
        return reconc[0], reconc[1]
    except TypeError:
        return parent_dict[reconc], reconc

transfers = [(correct_reconc(reconc1, parent), correct_reconc(reconc2, parent), t1, t2) for reconc1, reconc2, t1, t2 in transfers]

transfers_per_edge = {}

for r1,r2,t1,t2 in transfers:
    try:
        transfers_per_edge[r1].append(t1)
        transfers_per_edge[r1] = sorted(transfers_per_edge[r1], key = lambda x : -x)
    except KeyError:
        transfers_per_edge[r1] = [t1]
    try:
        transfers_per_edge[r2].append(t2)
        transfers_per_edge[r2] = sorted(transfers_per_edge[r2], key = lambda x : -x)
    except KeyError:
        transfers_per_edge[r2] = [t2]

N = max([max(u,v) for u,v in list_species_edges])+1

#for k,val in transfers_per_edge.items():
#    print("transfers per edge", k, val)

attach_point_dict = {}
for u,v in list_species_edges:
    if (u,v) in transfers_per_edge.keys():
        # adding attachment points
        for k in range(len(transfers_per_edge[(u,v)])):
            attach_point_dict[(u,v),transfers_per_edge[(u,v)][k]] = N+k
            adj[N+k] = []

        # connecting them as a path
        for k in range(len(transfers_per_edge[(u,v)])-1):
            adj[N+k] = [N+k+1]
            parent[N+k+1] = N+k

        # connecting first and last
        last = N+len(transfers_per_edge[(u,v)]) - 1
        adj[u].append(N)
        adj[u] = [w for w in adj[u] if w!=v]
        adj[last].append(v)
        parent[N] = u
        parent[v] = last
    
        # update last
        N = last+1

nnodes = len(adj.keys())
nedges = sum([len(ngbh) for _,ngbh in adj.items()])+len(transfers)
print("nnodes","nedges",nnodes,nedges)
for u, ngbh in adj.items():
    for v in ngbh:
        print(u,v,"tree")

#print(attach_point_dict)

for r1,r2,t1,t2 in transfers:
    u = attach_point_dict[r1,t1]
    v = attach_point_dict[r2,t2]
    print(u,v,"transfer")

