import sys
import json

fname = sys.argv[-1]

with open(fname) as f:
    tree = json.load(f)

adj = {}

queue = [tree]

while len(queue) > 0:
    node = queue.pop()
    try:
        child0 = node["_child0"]
        child1 = node["_child1"]
        try:
            adj[node["label"]].append(child0["label"])
        except KeyError:
            adj[node["label"]] = [child0["label"]]
        try:
            adj[node["label"]].append(child1["label"])
        except KeyError:
            adj[node["label"]] = [child1["label"]]

        queue.append(child0)
        queue.append(child1)
    except KeyError:
        pass

list_edges = []
for node, ngbh in adj.items():
    for node2 in ngbh:
        list_edges.append((node,node2))
print("nnodes","nedges",len(adj.keys()),len(list_edges))
for u,v in list_edges:
    print(u,v,"tree")
