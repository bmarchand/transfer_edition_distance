#..........................................
#...   Calculate simple LCA mapping    ....
#..........................................
# This algorithm is based on the procedure described
# in : http://www-labs.iro.umontreal.ca/~mabrouk/Publications/WABI12.pdf
# "AN optimal reconciliation algorithm for trees with polytomies"

import re
from copy import copy, deepcopy
from itertools import combinations_with_replacement
from tralda.datastructures.Tree import Tree
from asymmetree.tools.PhyloTreeTools import parse_newick, assign_missing_labels
from tralda.datastructures import LCA

#....................................................
# Functions for readng and printing newick files
#....................................................
def adjust_newick_rf(intree,fname):
    tree = copy(intree)
    for v in tree.postorder():
        if not v.is_leaf():
            if v.event == 'D':
                v.label = 'duplication'
            else:
                v.label = 'speciation'
    nhx_file = open(fname,"w")
    nhx_file.write(tree.to_newick())
    nhx_file.close()

def adjust_newick_parle(intree,fname):
    tree = copy(intree)
    for v in tree.postorder():
        new_tag = str(v.label) + "_" + v.event + "_" + str(v.reconc.label)
        v.label = new_tag

    nhx_file = open(fname,"w")
    nhx_file.write(tree.to_newick())
    nhx_file.close()

#.......................................................
# Transform RAxML newick to tralda
#.......................................................
def get_tralda_ML(fname):
    f = open(fname, "r")
    ML_newick = f.read()
    f.close()
    ml_tree = parse_newick(ML_newick)
    for n in ml_tree.postorder():
        if n.is_leaf():
            numbers = re.findall(r'\d+', n.label)
            numbers  = list(map(int, numbers))
            n.label  = numbers[1]
            n.reconc = int(numbers[2])
        n.event  = 'S'
    assign_missing_labels(ml_tree)
    return(ml_tree)

#..........................................................
# Calculate reconciliation map and labels
#..........................................................
def build_lca_map(G,S):
    def _all_pairs_lca(children,lca_S):
        species = set()
        for child in children:
            species.add(child.reconc)
        comparisons = list(combinations_with_replacement(species, 2))
        if len(comparisons) == 1:
            return(lca_S(comparisons[0][0],comparisons[0][1]))
        else:
            test_pair = comparisons.pop()
            current_lca = lca_S(test_pair[0],test_pair[1])
            flag = True
            while flag == True:
                pair = comparisons.pop()
                test_lca = lca_S(pair[0],pair[1])
                if lca_S.ancestor_not_equal(test_lca, current_lca):
                    current_lca = test_lca
                if len(comparisons) == 0:
                    flag = False
            return(current_lca)
    def _assign_event_label(node):
        species = set()
        children = [u.label for u in node.children]
        for child in node.children:
            species.add(child.reconc)
        if node.reconc in species:
            node.event = 'D'
        else:
            node.event = 'S'
    lca_S = LCA(S)
    for v in G.postorder():
        if v.is_leaf():
            v.reconc = lca_S(v.reconc,v.reconc)
        else:
            v.reconc = _all_pairs_lca(v.children,lca_S)
            _assign_event_label(v)


in_path = '/home/local/USHERBROOKE/lopa3401/Documents/WABI_2024_journal/RAxML_output/more_5_50/S5/best_scoring_ML_Tree/'
out_dir = '/home/local/USHERBROOKE/lopa3401/Documents/WABI_2024_journal/LCA_mapping_output/more_5_50/S5/'
stree = Tree.load("/home/local/USHERBROOKE/lopa3401/Documents/WABI_2024_journal/asymmetree_trees/more_5_50/S5/species_tree.json")
# S5 processing -----------------------------------------------------
for i in range (0,250):
    print("\t Running ",i," of 250 -------- S5 trees", end="\r")
    gtname  = in_path + "alignment" + str(i) + ".phylip.nhx"
    intree = get_tralda_ML(gtname)
    build_lca_map(intree,stree)

    #write result to newick files
    parle_name = out_dir + "n_parle_friendly/" + "rtree_" + str(i) + ".nhx"
    adjust_newick_parle(intree,parle_name)

    rf_name = out_dir + "n_rf_friendly/" + "rtree_" + str(i) + ".nhx"
    adjust_newick_rf(intree,rf_name)


#S10 processing  -----------------------------------------------------
path = '/home/local/USHERBROOKE/lopa3401/Documents/WABI_2024_journal/RAxML_output/more_5_50/S10/best_scoring_ML_Tree/'
out_dir = '/home/local/USHERBROOKE/lopa3401/Documents/WABI_2024_journal/LCA_mapping_output/more_5_50/S10/'
stree = Tree.load("/home/local/USHERBROOKE/lopa3401/Documents/WABI_2024_journal/asymmetree_trees/more_5_50/S10/species_tree.json")
for i in range (0,250):
    print("\t Running ",i," of 250 -------- S10 trees", end="\r")
    gtname  = path + "alignment" + str(i) + ".phylip.nhx"
    intree = get_tralda_ML(gtname)
    build_lca_map(intree,stree)

    #write result to newick files
    parle_name = out_dir + "n_parle_friendly/" + "rtree_" + str(i) + ".nhx"
    adjust_newick_parle(intree,parle_name)

    rf_name = out_dir + "n_rf_friendly/" + "rtree_" + str(i) + ".nhx"
    adjust_newick_rf(intree,rf_name)
