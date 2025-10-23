from tralda.datastructures.Tree import Tree
import asymmetree.treeevolve   as te
from asymmetree.genome import GenomeSimulator
from asymmetree.seqevolve import SubstModel, IndelModel

#//////////////////////////////////////////////////////////////
#       Species tree with 5 leaves
#//////////////////////////////////////////////////////////////
#Simulate species trees with the innovations model
S = te.species_tree_n(5,innovation=True,planted=False)

# specify models for sequence evolution
subst_model = SubstModel('a', 'JTT')

#Simulate gene trees with low duplication rates
# initiate GenomeSimulator instance
gs = GenomeSimulator(S, outdir='../asymmetree_trees/more_5_50/S5/')

# simulate 250 gene trees along the species tree S (and write them to file)
gs.simulate_gene_trees(10, dupl_rate=1.0, loss_rate=0.5,
                       base_rate=('gamma', 1.0, 1.0),
                       prohibit_extinction='per_species')

# simulate sequences along the gene trees
gs.simulate_sequences(subst_model,
                      het_model=None,
                      length_distr=('constant', 500))

#Print trees
nhx_file = open("../asymmetree_trees/more_5_50/S5/species_tree.nhx","w")
nhx_file.write(S.to_newick())
nhx_file.close()


#/////////////////////////////////////////////////////////////
#     Species tree with 10 leaves
#/////////////////////////////////////////////////////////////

#Simulate species trees with the innovations model
S = te.species_tree_n(10,innovation=True,planted=False)

#Simulate gene trees with low duplication rates
# initiate GenomeSimulator instance
gs = GenomeSimulator(S, outdir='../asymmetree_trees/more_5_50/S10/')

# simulate 250 gene trees along the species tree S (and write them to file)
gs.simulate_gene_trees(250, dupl_rate=1.0, loss_rate=0.5,
                       base_rate=('gamma', 1.0, 1.0),
                       prohibit_extinction='per_species')

# simulate sequences along the gene trees
gs.simulate_sequences(subst_model,
                      het_model=None,
                      length_distr=('constant', 500))


nhx_file = open('../asymmetree_trees/more_5_50/S10/species_tree.nhx',"w")
nhx_file.write(S.to_newick())
nhx_file.close()


#/////////////////////////////////////////////////////////////
#     Species tree with 25 leaves
#/////////////////////////////////////////////////////////////

#Simulate species trees with the innovations model
S = te.species_tree_n(25,innovation=True,planted=False)

#Simulate gene trees with low duplication rates
# initiate GenomeSimulator instance
gs = GenomeSimulator(S, outdir='../asymmetree_trees/more_5_50/S25/')

# simulate 250 gene trees along the species tree S (and write them to file)
gs.simulate_gene_trees(250, dupl_rate=1.0, loss_rate=0.5,
                       base_rate=('gamma', 1.0, 1.0),
                       prohibit_extinction='per_species')

# simulate sequences along the gene trees
gs.simulate_sequences(subst_model,
                      het_model=None,
                      length_distr=('constant', 500))


nhx_file = open('../asymmetree_trees/more_5_50/S25/species_tree.nhx',"w")
nhx_file.write(S.to_newick())
nhx_file.close()



#/////////////////////////////////////////////////////////////
#     Species tree with 50 leaves
#/////////////////////////////////////////////////////////////

#Simulate species trees with the innovations model
S = te.species_tree_n(50,innovation=True,planted=False)

# specify models for sequence evolution
subst_model = SubstModel('a', 'JTT')

#Simulate gene trees with low duplication rates
# initiate GenomeSimulator instance
gs = GenomeSimulator(S, outdir='../asymmetree_trees/more_5_50/S50/')

# simulate 250 gene trees along the species tree S (and write them to file)
gs.simulate_gene_trees(250, dupl_rate=1.0, loss_rate=0.5,
                       base_rate=('gamma', 1.0, 1.0),
                       prohibit_extinction='per_species')

# simulate sequences along the gene trees
gs.simulate_sequences(subst_model,
                      het_model=None,
                      length_distr=('constant', 500))


nhx_file = open('../asymmetree_trees/more_5_50/S50/species_tree.nhx',"w")
nhx_file.write(S.to_newick())
nhx_file.close()
