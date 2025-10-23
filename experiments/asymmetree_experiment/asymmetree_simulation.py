import asymmetree.treeevolve   as te

#Simulate species trees with the innovations model
nleaves = 100
S = te.species_tree_n(nleaves,innovation=True,planted=False)

tree_simulator = te.GeneTreeSimulator(S)
tree = tree_simulator.simulate(dupl_rate=1.0, loss_rate=0.5, hgt_rate=0.1)
tree.serialize("simulation_output/tree_simulator_object/example_tree.json")

##Simulate gene trees with low duplication rates
## initiate GenomeSimulator instance
#gs = GenomeSimulator(S, outdir='simulation_output')
#
## simulate gene trees along the species tree S (and write them to file)
#ntrees = 100
#gs.simulate_gene_trees(ntrees, dupl_rate=1.0, loss_rate=0.5,
#                       base_rate=('gamma', 1.0, 1.0),
#                       prohibit_extinction='per_species')
#
