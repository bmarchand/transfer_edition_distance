import asymmetree.treeevolve as te
from asymmetree.tools.PhyloTreeTools import to_newick


#Simulate species trees with the innovations model
nleaves = 100
S = te.species_tree_n(nleaves,innovation=True,planted=False)

# storing the species tree
S.serialize("simulation_output/species_tree"+str(nleaves)+"leaves.json")
newick = to_newick(S,distance=False)
newick_file = open("simulation_output/species_tree"+str(nleaves)+".nhx","w")
print(newick,file=newick_file)


tree_simulator = te.GeneTreeSimulator(S)
tree = tree_simulator.simulate(dupl_rate=1.0, loss_rate=0.5, hgt_rate=0.1)

tree.serialize("simulation_output/simulated_gene_trees/simulated_tree"+str(nleaves)+"leaves.json")
newick = to_newick(tree, distance=False)
newick_file = open("simulation_output/simulated_gene_trees/simulated_tree"+str(nleaves)+"leaves.nhx","w")
print(newick,file=newick_file)

