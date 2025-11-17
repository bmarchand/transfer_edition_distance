import os

species_tree_edges = []
node_set = set([])
for line in open("species_tree.gr").readlines()[1:]:
    species_tree_edges.append((line.split(" ")[0], line.split(" ")[1]))
    node_set.add(line.split(" ")[0])
    node_set.add(line.split(" ")[1])

integer_map = {}
for k, node in enumerate(sorted(list(node_set))):
    integer_map[node] = k

for method in ["fitch","genesis","sankoff"]:
    transfer_weight = {}

    for network in os.listdir("networks/"):
        print(network)
        if network.split("_")[1].split(".")[0]==method:
            for line in open("networks/"+network).readlines()[1:]:
                if line.split(" ")[2].rstrip('\n')=="transfer":
                    species1 = line.split(" ")[0]
                    species2 = line.split(" ")[1]
                    try:
                        transfer_weight[(species1,species2)] += 1
                    except KeyError:
                        transfer_weight[(species1,species2)] = 1
                    
    with open("aggregated_network_"+method+".gr","w") as f:
        print("nnodes","nedges",len(node_set),len(species_tree_edges)+len(transfer_weight.keys()),file=f)
        for s1,s2 in species_tree_edges:
            print(s1,s2,"tree",file=f)
        for key, value in transfer_weight.items():
            print(key[0],key[1],"transfer",value,file=f)

    with open("aggregated_network_integer"+method+".gr","w") as f:
        print("nnodes","nedges",len(node_set),len(species_tree_edges)+len(transfer_weight.keys()),file=f)
        for s1,s2 in species_tree_edges:
            print(integer_map[s1],integer_map[s2],"tree",file=f)
        for key, value in transfer_weight.items():
            print(integer_map[key[0]],integer_map[key[1]],"transfer",value,file=f)
