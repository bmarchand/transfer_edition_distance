#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib
## from phylonetwork import PhyloNetwork
import networkx as nx
#import phylonetwork
import pylab as plt
import random,numpy
import itertools
from networkx.drawing.nx_agraph import graphviz_layout


# In[2]:


import warnings
import matplotlib.cbook
#warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


# In[3]:


def last_node(net):
    return max(net.nodes())


# In[4]:


def speciate(net,leaf):
    l = last_node(net)
    net.add_edge(leaf,l+1,edge_type='tree')
    net.add_edge(leaf,l+2,edge_type='tree')


# In[5]:


def lgt(net,leaf1,leaf2):
    net.add_edge(leaf1,leaf2,edge_type='transfer')
    l = last_node(net)
    net.add_edge(leaf1,l+1,edge_type='tree')
    net.add_edge(leaf2,l+2,edge_type='tree')


# In[6]:


def draw(net):
    positions = nx.drawing.nx_agraph.graphviz_layout(net, prog="dot")
    # nx.draw(net, pos=graphviz_layout(net),prog='dot',args="-Grankdir=LR", with_labels=True)
    nx.draw(net,positions,with_labels=True)
    plt.show()


# In[7]:


def leaves(net):
    return [u for u in net.nodes() if net.out_degree(u)==0]


# In[8]:


def non_trivial_blobs(net):
    blobs = list(nx.biconnected_components(nx.Graph(net)))
    return [bl for bl in blobs if len(bl) > 2]


# In[9]:


def internal_blobs(net):
    internal_nodes = set([u for u in net.nodes() if net.out_degree(u)>0])
    blobs = list(nx.biconnected_components(nx.Graph(net)))
    blobs = [bl for bl in blobs if len(bl) > 2]
    nodes_in_blobs = set().union(*blobs)
    nodes_not_in_blobs = internal_nodes - nodes_in_blobs
    blobs.extend([set([u]) for u in nodes_not_in_blobs])
    return blobs


# In[10]:


def compute_hash(net):
    mapping_blobs = {}
    blobs = internal_blobs(net)
    for blob in blobs:
        for node in blob:
            mapping_blobs[node] = blob

    mapping = {}
    for l in leaves(net):
        parent = list(net.predecessors(l))[0]
        mapping[l] = mapping_blobs[parent]
    return mapping


# In[11]:


def internal_and_external_pairs(net):
    lvs = leaves(net)
    pairs = [(l1,l2) for l1 in lvs for l2 in lvs if l1 != l2]
    mapping = compute_hash(net)
    internal_pairs = []
    external_pairs = []
    for pair in pairs:
        if mapping[pair[0]] == mapping[pair[1]]:
            internal_pairs.append(pair)
        else:
            external_pairs.append(pair)
    return internal_pairs, external_pairs


# In[12]:


def random_leaf(net):
    return random.choice(leaves(net))


# In[13]:


def random_pair(net,wint,wext):
    int_pairs, ext_pairs = internal_and_external_pairs(net)
    return random.choices(int_pairs+ext_pairs, weights=[wint]*len(int_pairs)+[wext]*len(ext_pairs))[0]


# In[14]:

def export_network(network, filename):
    f = open(filename,'w')

    leaf_list = leaves(network)
    nnodes = network.order()

    mapping = {}
    for k,u in enumerate(leaf_list):
        mapping[u] = k
    for k,u in enumerate(network.nodes):
        if u not in leaf_list:
            mapping[u] = nnodes+k


    network = nx.relabel_nodes(network, mapping)

    print("nvertices nedges",network.order(),network.size(),file=f)
    for u,v,edge_type in network.edges(data='edge_type'):
        print(u,v,edge_type,file=f)
    f.close()

def simulation(num_steps,prob_lgt,wint,wext,seed=None):
    if seed:
        random.seed(seed+1) # +1 is in case seed=0
    net = nx.DiGraph()
    net.add_edge(1,2,edge_type='tree')
    net.add_edge(1,3,edge_type='tree')
    for i in range(num_steps):
        event = random.choices(['spec','lgt'],[1-prob_lgt, prob_lgt])[0]
        #event = numpy.random.choice(['spec','lgt'],p=[1-prob_lgt, prob_lgt])
        if event == 'spec':
            l = random.choice(leaves(net))
            speciate(net,l)
        else:
            pair = random_pair(net,wint,wext)
            lgt(net,pair[0],pair[1])
    return net


# In[15]:


def reticulations(G):
    return [v for v in G.nodes() if G.in_degree(v)==2]
def local_level(G,bicc):
    rets=list(set(reticulations(G)).intersection(bicc)) # reticulations present in the blob
    if len(rets)==0:
        return 0
    else:
        bicc_edges=[e for e in G.edges() if ((e[0] in bicc)&(e[1]in bicc))]
        end_nodes=[e[1] for e in bicc_edges]
        return len([ret for ret in rets if ret in end_nodes]) 


# In[16]:

if __name__=="__main__":
    number_of_experiments = 50
    values_of_n = range(20,150,10)
    values_of_alpha = [0.1,0.3,0.5,0.7]
    values_of_beta = [0.01,0.1,1,10]
    stats_level = {}
    stats_numblobs = {}
    
    level_dict = {}
    
    def file_name(n,alpha,beta,cnt):
        return "random_lgt_networks/network_n"+str(n)+"_alpha"+str(alpha)+"_beta"+str(beta)+"_"+str(cnt)+'.gr'
    
    seed_n = 2024
    
    for (n, alpha, beta) in itertools.product(values_of_n, values_of_alpha, values_of_beta):
        print(n,alpha,beta)
        levels = []
        numblobs = []
        for cnt in range(number_of_experiments):
            resG = simulation(n, alpha, 1, beta, seed=seed_n)
            seed_n *= 2
            seed_n += 1
            bic_comp=list(nx.biconnected_components(nx.Graph(resG)))
            rets_x_bicc=[local_level(resG,b) for b in bic_comp]
            level=max(rets_x_bicc)
            level_dict[file_name(n,alpha,beta,cnt)] = level
            export_network(resG,file_name(n,alpha,beta,cnt))
            levels.append(level)
            sparse=[1 for x in rets_x_bicc if x!=0]
            numblobs.append(sum(sparse))
    
    import json
    with open("level_dict.json","w") as f:
        json.dump(level_dict, f)
