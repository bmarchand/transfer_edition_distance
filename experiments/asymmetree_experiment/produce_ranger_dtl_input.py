import sys
import json

species_newick = sys.argv[-2]
gene_tree_json = sys.argv[-1]
print(species_newick)
print(gene_tree_json)

label_per_species_leaf = {}

with open(gene_tree_json) as f:
    gene_tree_root = json.load(f)

queue = [gene_tree_root]

while len(queue) > 0:
    node = queue.pop()
    try:
        child0 = node["_child0"]
        child1 = node["_child1"]
        queue.append(child0)
        queue.append(child1)

    except KeyError:
        if node["event"]!="L":
            try:
                label_per_species_leaf[node["reconc"]].append(node["label"])
            except KeyError:
                label_per_species_leaf[node["reconc"]] = [node["label"]]

new_label = {}

for key,value in label_per_species_leaf.items():
    for k, v in enumerate(value):
        new_label[v] =str(key)+"_"+str(k)

print("label_per_species_leaf", label_per_species_leaf)
print("new label", new_label)

#TODO pop double losses

def newick_export(node):
    print(node["label"])
    try:
        child0 = node["_child0"]
        child1 = node["_child1"]

        if child0["event"]=="L":
            return newick_export(child1)
        if child1["event"]=="L":
            return newick_export(child0)

        return "("+newick_export(child0)+","+newick_export(child1)+")"

    except KeyError:
        assert(node["event"]!="L")
        return new_label[node["label"]]

gene_tree_newick = newick_export(gene_tree_root)+";"
species_newick_line = open(species_newick).readlines()[0].rstrip('\n')
print(species_newick_line)
print(gene_tree_newick)

