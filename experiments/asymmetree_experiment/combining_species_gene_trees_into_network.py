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
            print("transfer between ",node["reconc"],"and",child0["reconc"], node["tstamp"], child0["tstamp"])
            transfers.append((node["reconc"],child0["reconc"],node["tstamp"],child0["tstamp"]))
        if child1["transferred"]==1:
            print("transfer between ",node["reconc"],"and",child1["reconc"], node["tstamp"], child1["tstamp"])
            transfers.append((node["reconc"],child1["reconc"],node["tstamp"],child1["tstamp"]))
        queue.append(child0)
        queue.append(child1)
    except KeyError:
        pass

tree_adj = {}
parent = {}
for line in open(species_tree).readlines()[1:]:
    u = int(line.split(" ")[0])
    v = int(line.split(" ")[1])
    parent[v] = u
    try:
        tree_adj[u].append(v)
    except KeyError:
        tree_adj[u] = [v]

def subdivision(tree_adj, parent, timestamp, newtime, u,v):

    # what is the next available integer ?
    all_vertices = set(tree_adj.keys())
    for _,ngbh in tree_adj.items():
        for w in ngbh:
            all_vertices.add(w)
    N = max(all_vertices)


    # where do we insert it ?
    parent_of_new = parent[v]
    while parent_of_new in timestamp.keys() and timestamp[parent_of_new] > newtime:
        parent_of_new = parent[parent_of_new]

    tree_adj[u].append(N+1)
    tree_adj[u] = [w for w in tree_adj[u] if w!=v]
    tree_adj[N+1] = [v]
    parent[N+1] = u
    parent[v] = N+1
    return tree_adj, parent, N+1

print(tree_adj)
print(transfers)

transfer_edge_list = []

for e1, e2 in transfers:
    try:
        tree_adj, parent, x = subdivision(tree_adj, parent, e1[0], e1[1])
    except:
        tree_adj, parent, x = subdivision(tree_adj, parent, parent[e1], e1)
    try:
        tree_adj, parent, y = subdivision(tree_adj, parent, e2[0], e2[1])
    except:
        tree_adj, parent, y = subdivision(tree_adj, parent, parent[e2], e2)

    transfer_edge_list.append((x,y))

nnodes = len(tree_adj.keys())
nedges = sum([len(ngbh) for _,ngbh in tree_adj.items()])
print("nnodes","nedges",nnodes,nedges)
for u, ngbh in tree_adj.items():
    for v in ngbh:
        print(u,v,"tree")
for x,y in transfer_edge_list:
    print(x,y,"transfer")




