import sys
import json

species_gr = sys.argv[-3]
species_newick = sys.argv[-2]
gene_tree_json = sys.argv[-1]

# parsing species tree
species_tree_adj = {}
species = set([])
for line in open(species_gr).readlines()[1:]:
    u = line.split(" ")[0]
    v = line.split(" ")[1]
    species.add(u)
    species.add(v)
    try:
        species_tree_adj[u].append(v)
    except KeyError:
        species_tree_adj[u] = [v]

# building a set of species tree leaves
species_leaves = set([])
for x in species:
    if x not in species_tree_adj.keys():
        species_leaves.add(int(x))


label_per_species_leaf = {}

with open(gene_tree_json) as f:
    gene_tree_root = json.load(f)

# pruning the losses out of the gene tree (may create degree-2 nodes)
# also, when reaching a leaf that is not a loss, associating it
# to its species tree leaf
queue = [gene_tree_root]

while len(queue) > 0:
    node = queue.pop()
    if "_child0" in node.keys():
        assert("_child1" in node.keys()) # no degree 2 nodes, hopefully
        child0 = node["_child0"]
        child1 = node["_child1"]

        queue.append(child0)
        queue.append(child1)
    
    else:
        assert(node["reconc"] in species_leaves)
        try:
            label_per_species_leaf[node["reconc"]].append(node["label"])
        except KeyError:
            label_per_species_leaf[node["reconc"]] = [node["label"]]


new_label = {}

for key,value in label_per_species_leaf.items():
    for k, v in enumerate(value):
        new_label[v] =str(key)+"_"+str(k)

def newick_export(node):
    if "_child0" in node.keys():
        assert("_child1" in node.keys())
        child0 = node["_child0"]
        child1 = node["_child1"]
        return "("+newick_export(child0)+","+newick_export(child1)+")"
    else:
        return new_label[node["label"]]

gene_tree_newick = newick_export(gene_tree_root)+";"
species_newick_line = open(species_newick).readlines()[0].rstrip('\n')
print(species_newick_line)
print(gene_tree_newick)

