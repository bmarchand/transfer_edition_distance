import asymmetree.treeevolve as te
import sys
from asymmetree.tools.PhyloTreeTools import to_newick

nruns = int(sys.argv[-1])
nleaves = int(sys.argv[-2])

for cnt in range(nruns):
    #Simulate species trees with the innovations model
    nleaves = 5
    S = te.species_tree_n(nleaves,innovation=True,planted=False)
    
    # storing the species tree
    S.serialize("simulation_output/simulated_species_trees/species_tree"+str(nleaves)+"leaves_"+str(cnt)+".json")
    newick = to_newick(S,distance=False)
    newick_file = open("simulation_output/simulated_species_trees/species_tree"+str(nleaves)+"leaves_"+str(cnt)+".nhx","w")
    print(newick,file=newick_file)
    
    
    tree_simulator = te.GeneTreeSimulator(S)
    tree = tree_simulator.simulate(dupl_rate=1.0, loss_rate=0.5, hgt_rate=0.1)
    
    tree.serialize("simulation_output/simulated_gene_trees/simulated_tree"+str(nleaves)+"leaves_"+str(cnt)+".json")
    newick = to_newick(tree, distance=False)
    newick_file = open("simulation_output/simulated_gene_trees/simulated_tree"+str(nleaves)+"leaves_"+str(cnt)+".nhx","w")
    print(newick,file=newick_file)
    
