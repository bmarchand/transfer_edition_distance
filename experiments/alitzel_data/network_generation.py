#!/usr/bin/env python
# coding: utf-8

# # How to generate tree-based networks
# This notebook generates three tree-based networks 

# In[1]:


import pandas as pd
import ast
import numpy as np
from treebased import TB_Network
import matrix as mx
import pickle as pkl
import tools as ts


# ## General Input for all three methods
# Regardless of the method, you will need a species tree and a KO list. The species tree and the KO list is the same for all methods. The KO list is cut because creating the 180 matrix from requests from the KEGG database on one shot was too long. This is artisanal paralellism :P
# 
# ### General Input data
# 
# All analysis folders contain the same input data. We'll gra Fitch just because :)
# The input matrix is a matrix already built from the KEGG orthology database by using the function"generate_from_KEGG_v1" from "matrix.py" in the source files.

# In[5]:


#All analysis folders contain the same input data. 
#We'll grab Fitch just because it's the first
input_path = "../data/fitch_labeling_analysis/input_data/"

#Import Species Tree
sname = input_path + "species_tree_ultra.pkl"
f = open(sname,"rb")
S = pkl.load(f)
f.close()

#Import KO list
koname = input_path + "ARG_related_KOs.csv"
KO_df = pd.read_csv(koname)
KOs_list = list(KO_df['RF_KO'])
matrix = [KOs_list[i:i+45] for i in range(0,len(KOs_list),45)]

#Testing with the first chunk of the matrix
i = 0
chunk = matrix[i]
mname = "../data/KO_matrices/interphylum_matrix_chunk_" + str(i) + ".pkl" 
file = open(mname,"rb")
m = pkl.load(file)
file.close()


# ### Fitch network
# In this network, no cost matrix is required. 

# In[6]:


#Initialize Fitch network
fitch_Network = TB_Network(S.root)
fitch_Network.init_base_from_tralda(S,len(chunk))

#Assigns characters to the leaves
for leaf in fitch_Network.leaves():
    leaf.chars = m[leaf.label]

#Computes the Fitch labeling
fitch_Network.fitch_labeling()

#Gets list of first-appearances
Fitch_FAs = fitch_Network.get_fas_by_state_change()


# ### Important! cost matrix required for Sankoff and Genesis

# In[ ]:


#Event transition cost for Sankoff and Genesis
loss_cost = 1.0
transfer_cost = 1.0


# ### Sankoff network

# In[3]:


#Initialize Sankoff network
san_Network = TB_Network(S.root)
san_Network.init_base_from_tralda(S,len(chunk))

for leaf in san_Network.leaves():
    leaf.chars = m[leaf.label]

san_Network.sankoff_labeling(loss_cost,transfer_cost)

#Gets list of first-appearances
Sankoff_FAs = san_Network.get_fas_by_state_change()


# ### Genesis network

# In[4]:


#Initialize Genesis network
gen_Network = TB_Network(S.root)
gen_Network.init_base_from_tralda(S,len(chunk))

#Assign characters to leaves
for leaf in gen_Network.leaves():
    leaf.chars = m[leaf.label]

gen_Network.genesis_labeling(loss_cost,transfer_cost)


# ## How to get a greedy list of first appearances
# 
# It suffices to run the following function. This function sorts the first appearances acoording to a suitable timing, which is what a greedy algorithm that joins them would do :)

# In[10]:


#How to get a sorted list of first appearances
def get_greedy_FA_list(Network,ko_list):
    def _sort_fas(fa_list):
            return(sorted(fa_list, key = lambda x:x.tstamp,reverse=True))
    fa_set  = []
    fa_dict = Network.get_fas_by_state_change()

    for char in fa_dict:
        fas = list(fa_dict[char])
        fa_dict[char] = _sort_fas(fas)
        fa_set.append(fa_dict[char])
    df = pd.DataFrame()
    df['characters'] = ko_list
    df['fa_list'] = fa_set
    return(df)

#IDs of the involved KOs (cause we separated them into chunks)
KOs = KOs_list[i:i+45]

Fitch_data = get_greedy_FA_list(fitch_Network,KOs)
Sankoff_data = get_greedy_FA_list(san_Network,KOs)
Genesis_data = get_greedy_FA_list(gen_Network,KOs)


print("For Fitch:")
print(Fitch_data.head())
Fitch_data.to_csv("fitch_network.csv")

print("For Sankoff:")
print(Sankoff_data.head())
Sankoff_data.to_csv("sankoff_network.csv")

print("For Genesis:")
print(Genesis_data.head())
Genesis_data.to_csv("genesis_network.csv")


