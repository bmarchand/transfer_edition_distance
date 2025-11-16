import newick

lines = open("species_tree.phy").readlines()
lines = [l.rstrip('\n') for l in lines]

newick_string = "".join(lines)

print(newick_string)

tree = newick.loads(newick_string)[0]

queue = [tree]

file = open("species_tree.gr",'w')

lines_to_print = []
nvertices = 0
nedges = 0
while len(queue) > 0:
    u = queue.pop()
    nvertices += 1
    for v in u.descendants:
        nedges += 1
        lines_to_print.append(" ".join([u.name,v.name,"tree"]))
        queue.append(v)

print("nvertices nedges",nvertices, nedges,file=file)
for line in lines_to_print:
    print(line, file=file)
