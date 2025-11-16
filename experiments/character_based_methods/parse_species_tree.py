import pickle as pkl
f = open("species_tree_ultra.pkl","rb")
S = pkl.load(f)
f.close()


file = open("species_tree.gr",'w')

lines_to_print = []
vertex_set = set([])
nedges = 0

for u,v in S.edges():
    nedges += 1
    print(u.label,v.label)
    vertex_set.add(u)
    vertex_set.add(v)
    lines_to_print.append(" ".join([u.label,v.label,"tree"]))


nvertices = len(vertex_set)

print("nvertices nedges",nvertices, nedges,file=file)
for line in lines_to_print:
    print(line, file=file)


