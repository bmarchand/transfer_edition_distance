import pickle as pkl
import sys
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

network_name = sys.argv[-1]

f = open("species_tree_ultra.pkl","rb")
S = pkl.load(f)
f.close()

x_scale = .1
y_scale = .1

G = nx.DiGraph()

vertices = set([])
for u,v in S.edges():
    vertices.add(u)
    vertices.add(v)
    G.add_edge(u,v)

pos = graphviz_layout(G, prog="twopi")

f = open(network_name.split(".")[0]+".tex","w")

print("\\documentclass{standalone}", file=f)
print("\\usepackage{tikz}", file=f)
print("\\begin{document}", file=f)
print("\\begin{tikzpicture}", file=f)
for u in vertices:
    print("\\node[fill=black,circle] ("+u.label+") at ("+str(x_scale*pos[u][0])+","+str(y_scale*pos[u][1])+") {};",file=f)
for u,v in S.edges():
    print("\\draw[line width=10pt,red] ("+u.label+") -- ("+v.label+");",file=f)

for line in open(network_name).readlines():
    if line.find("transfer") >= 0:
        u = line.split(" ")[0] 
        v = line.split(" ")[1]
        weight = float(line.split(" ")[-1].rstrip("\n"))
        print("\\draw[line width="+str(weight)+"pt,->] ("+u+") -- ("+v+");", file=f)
print("\\end{tikzpicture}", file=f)
print("\\end{document}", file=f)


