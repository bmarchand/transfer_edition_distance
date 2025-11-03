import sys

species_tree = sys.argv[-2] # gr file
hway_file = sys.argv[-1]

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

transfers = []
transferred_edges = set([])
for line in open(hway_file).readlines():
    u = int(line.split(" ")[0])
    v = int(line.split(" ")[1])
    w = int(line.split(" ")[2])
    x = int(line.split(" ")[3].rstrip('\n'))
    transfers.append(((u,v),(w,x)))
    transferred_edges.add((u,v))
    transferred_edges.add((w,x))

# next available label
N = max([max(u,v) for u,v in list_species_edges])+1

# adding new vertices (attachment points) to the graph.
attach_point_dict = {}
for u,v in list_species_edges:
    if (u,v) in transferred_edges:
        attach_point_dict[(u,v)] = N
        adj[N] = []

        adj[u].append(N)
        adj[u] = [w for w in adj[u] if w!=v]
        adj[N].append(v)
        parent[N] = u
        parent[v] = N
    
        N += 1

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

for r1,r2 in transfers:
    u = attach_point_dict[r1]
    v = attach_point_dict[r2]
    print(u,v,"transfer")
