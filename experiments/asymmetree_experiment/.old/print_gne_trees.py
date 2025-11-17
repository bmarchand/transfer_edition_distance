#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json


# In[3]:


with open('simulation_output/simulated_gene_trees/simulated_tree100leaves.json') as f:
    tree = json.load(f)


# In[6]:


def pprint(tree, depth):
    print(depth*" ",tree['label'],tree['event'],tree['reconc'],tree['tstamp'])
    if "_child0" in tree.keys():
        pprint(tree['_child0'],depth+1)
        pprint(tree['_child1'],depth+1)


# In[5]:


pprint(tree,0)


# In[ ]:




