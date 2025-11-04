"""
    This script creates the "ground truth" unordered weighted network.
"""
import sys
import json

species_tree = sys.argv[-2] # gr file
gene_tree = sys.argv[-1]    # json file

with open(gene_tree) as f:
    gene_tree_root = json.load(f)

queue = [gene_tree_root]

transfers = []

# building a list of transfers. 1 transfer = two 'reconc' (species tree edge or species tree leaf)
# and two time stamps
while len(queue) > 0:
    node = queue.pop()
    try:
        child0 = node["_child0"]
        child1 = node["_child1"]
        if child0["transferred"]==1:
            transfers.append((node["reconc"],child0["reconc"]))
        if child1["transferred"]==1:
            transfers.append((node["reconc"],child1["reconc"]))
        queue.append(child0)
        queue.append(child1)
    except KeyError:
        pass

# reading species tree file
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
    """
    putting all reconc into the same format.
    Indeed, some of them are edges of the species tree (lists),
    others are single leaves (integers). They are all converted
    into tuples coding for an edge of the species tree.
    """
    try:
        return reconc[0], reconc[1]
    except TypeError:
        if reconc in parent_dict.keys():
            return parent_dict[reconc], reconc
        else: #only happens in the rare case of a transfer involving root
            return reconc, reconc

transfers = [(correct_reconc(reconc1, parent), correct_reconc(reconc2, parent)) for reconc1, reconc2 in transfers]

edges_with_transfer = set([])

for r1,r2 in transfers:
    edges_with_transfer.add(r1)
    edges_with_transfer.add(r2)

# next available label
N = max([max(u,v) for u,v in list_species_edges])+1

# adding new vertices (attachment points) to the graph.
attach_point_dict = {}
for u,v in list_species_edges:
    if (u,v) in edges_with_transfer:
        attach_point_dict[(u,v)] = N
        adj[N] = []

        adj[u].append(N)
        adj[u] = [w for w in adj[u] if w!=v]
        adj[N].append(v)
        parent[N] = u
        parent[v] = N
    
        N += 1

# computing weight
weight = {}
for r1, r2 in transfers:
    try:
        weight[(r1,r2)] += 1
    except KeyError:
        weight[(r1,r2)] = 1

nnodes = len(adj.keys())
nedges = sum([len(ngbh) for _,ngbh in adj.items()])+len(transfers)
print("nnodes","nedges",nnodes,nedges)
for u, ngbh in adj.items():
    for v in ngbh:
        print(u,v,"tree")

#print(attach_point_dict)

#special case of root:
for r1,r2 in transfers:
    if r1[0]==r1[1]:
        attach_point_dict[r1] = r1[0]
    if r2[0]==r2[1]:
        attach_point_dict[r2] = r2[0]

for (r1,r2), w in weight.items():
    u = attach_point_dict[r1]
    v = attach_point_dict[r2]
    print(u,v,"transfer",w)

