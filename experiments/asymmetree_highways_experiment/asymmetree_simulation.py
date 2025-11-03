import asymmetree.treeevolve as te
import sys
from asymmetree.tools.PhyloTreeTools import to_newick
import random

nruns = int(sys.argv[-4])
ngenetrees_per_run = int(sys.argv[-3])
nhighways = int(sys.argv[-2])
nleaves = int(sys.argv[-1])

def get_transfer_highwayset(S, nhighways):
    L = list(S.edges()) # this list is in topological order
    possible_highways = []
    for i in range(len(L)):
        for j in range(len(L)):
            if i < j:
                u,v = L[i]
                w,x = L[j]
                possible_highways.append(((u.label,v.label),(w.label,x.label)))

#    return possible_highways
    return random.sample(possible_highways, nhighways)

def correct_reconc(reconc, parent_dict):
    if type(reconc)==tuple:
        return reconc
    else:
        return parent_dict[reconc], reconc

def is_valid(tree, transfer_highways, parent_dict):
    for u,v in tree.edges():
        if v.transferred:
            if u.reconc==1 or v.reconc==1:
                return False
            reconc_u = correct_reconc(u.reconc,parent_dict)
            reconc_v = correct_reconc(v.reconc,parent_dict)
            if not (reconc_u,reconc_v) in transfer_highways:
                return False
#    print("returning True")
    return True

def get_parent_dict(S):
    parent = {}
    for u,v in S.edges():
        parent[v.label] = u.label
    return parent

for cnt in range(nruns):
    #Simulate species trees with the innovations model
    S = te.species_tree_n(nleaves,innovation=True,planted=False)
    
    # storing the species tree
    S.serialize("simulation_output/simulated_species_trees/species_tree"+str(nleaves)+"leaves_"+str(cnt)+".json")
    newick = to_newick(S,distance=False)
    newick_file = open("simulation_output/simulated_species_trees/species_tree"+str(nleaves)+"leaves_"+str(cnt)+".nhx","w")
    print(newick,file=newick_file)

    H = get_transfer_highwayset(S, nhighways)
    with open("simulation_output/simulated_species_trees/highway_"+str(nleaves)+"_"+str(cnt)+".hway","w") as f:
        for u,v in H:
            print(u[0],u[1],v[0],v[1],file=f)

    parent = get_parent_dict(S)

    cnt2 = 0
    while cnt2 < ngenetrees_per_run:

        tree_simulator = te.GeneTreeSimulator(S)
        tree = tree_simulator.simulate(dupl_rate=1.0, loss_rate=0.5, hgt_rate=0.2)
        tree = te.prune_losses(tree)

        if is_valid(tree, H, parent):
            tree.serialize("simulation_output/simulated_gene_trees/simulated_tree"+str(nleaves)+"leaves_"+str(cnt)+"_"+str(cnt2)+".json")
            newick = to_newick(tree, distance=False)
            newick_file = open("simulation_output/simulated_gene_trees/simulated_tree"+str(nleaves)+"leaves_"+str(cnt)+"_"+str(cnt2)+".nhx","w")
            print(newick,file=newick_file)
            cnt2 += 1
    
