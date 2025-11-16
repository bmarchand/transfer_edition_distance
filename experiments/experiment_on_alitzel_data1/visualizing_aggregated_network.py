import pickle as pkl
import sys
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

#network_name = sys.argv[-1]
network_names = ["aggregated_network_fitch.gr","aggregated_network_genesis.gr","aggregated_network_sankoff.gr"]

f = open("species_tree_ultra.pkl","rb")
S = pkl.load(f)
f.close()

x_scale = .01
y_scale = .01
shift = 10
weight_threshold = 4

G = nx.DiGraph()

vertices = set([])
for u,v in S.edges():
    vertices.add(u)
    vertices.add(v)
    G.add_edge(u,v)

pos = graphviz_layout(G, prog="twopi")

f = open("all_three_networks.tex","w")

print("\\documentclass{standalone}", file=f)
print("\\usepackage{tikz}", file=f)
print("\\begin{document}", file=f)
print("\\begin{tikzpicture}", file=f)

labels = ["Basic","Genesis","Sankoff"]

for k, network_name in enumerate(network_names):

    print("\\begin{scope}[shift={("+str(k*shift)+",0)}]",file=f)

    for u in vertices:
        print("\\node[fill=black,circle,inner sep=1pt] ("+u.label+") at ("+str(x_scale*pos[u][0])+","+str(y_scale*pos[u][1])+") {};",file=f)
    for u,v in S.edges():
        print("\\draw[line width=1pt,red] ("+u.label+") -- ("+v.label+");",file=f)

    for line in open(network_name).readlines():
        if line.find("transfer") >= 0:
            u = line.split(" ")[0] 
            v = line.split(" ")[1]
            weight = float(line.split(" ")[-1].rstrip("\n"))
            if weight > weight_threshold:
                print("\\draw[line width="+str(0.25*weight)+"pt,->] ("+u+") -- ("+v+");", file=f)

    
    print("\\node at (5,-1) {\\Huge\\bfseries "+labels[k]+"};",file=f)
    print("\\end{scope}",file=f)

print("\\end{tikzpicture}", file=f)
print("\\end{document}", file=f)


