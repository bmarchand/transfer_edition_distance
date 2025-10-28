import sys
import json

species_tree = sys.argv[-2] # gr file
gene_tree = sys.argv[-1]    # json fil

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
            transfers.append((node["reconc"],child0["reconc"],node["tstamp"],child0["tstamp"]))
        if child1["transferred"]==1:
            transfers.append((node["reconc"],child1["reconc"],node["tstamp"],child1["tstamp"]))
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
        return parent_dict[reconc], reconc

transfers = [(correct_reconc(reconc1, parent), correct_reconc(reconc2, parent), t1, t2) for reconc1, reconc2, t1, t2 in transfers]

# will store a set of timestamps per edge of the species tree.
# converted to a sorted list afterwards. Note that
# there may be several transfers per time stamp (especially 
# at leaves)
transfers_per_edge = {}

for r1,r2,t1,t2 in transfers:
    try:
        transfers_per_edge[r1].add(t1)
    except KeyError:
        transfers_per_edge[r1] = set([t1])
    try:
        transfers_per_edge[r2].add(t2)
    except KeyError:
        transfers_per_edge[r2] = set([t2])

for key, value in transfers_per_edge.items():
    transfers_per_edge[key] = sorted(list(value),key=lambda x : -x)

# next available label
N = max([max(u,v) for u,v in list_species_edges])+1

# adding new vertices (attachment points) to the graph.
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

