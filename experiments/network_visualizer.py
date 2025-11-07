import networkx as nx
import matplotlib.pylab as plt
import sys
from networkx.drawing.nx_pydot import graphviz_layout

fname = sys.argv[-1]

tree_in_adj = {}
tree_out_adj = {}
transfers = []

G = nx.DiGraph()

for line in open(fname).readlines()[1:]:
    u = line.split(" ")[0]
    v = line.split(" ")[1]
    kind = line.split(" ")[2].rstrip('\n')

    G.add_edge(u,v,kind=kind)

    if kind=='tree':
        try:
            tree_in_adj[v].append(u)
        except KeyError:
            tree_in_adj[v] = [u]
        try:
            tree_out_adj[u].append(v)
        except KeyError:
            tree_out_adj[u] = [v]

    if kind=='transfer':
        transfers.append((u,v))

T = nx.Graph()
for u in tree_out_adj.keys():
    for v in tree_out_adj[u]:
        T.add_edge(u,v)

pos = graphviz_layout(T, prog="twopi")

nx.draw_networkx_nodes(G,pos,node_size=3)
nx.draw_networkx_labels(G,pos,font_size=8)
nx.draw_networkx_edges(G, pos, edgelist=[(u,v) for (u,v) in G.edges if G[u][v]['kind']=='tree'],edge_color="tab:blue")
nx.draw_networkx_edges(G, pos, edgelist=[(u,v) for (u,v) in G.edges if G[u][v]['kind']=='transfer'],edge_color="tab:red")

plt.show()
