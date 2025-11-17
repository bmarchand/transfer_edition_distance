#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import matplotlib.patches as patches


# In[2]:


df = pd.read_csv("benchmark_results_fixed_n.csv")



# In[4]:


data_per_alpha_beta = {}


# In[5]:


for index, row in df.iterrows():
    if row.betas1!=row.betas2:
        continue
    alpha = row.alphas1
    beta = row.betas1
    if np.isnan(row.runtime):
        print("nan indeed")
        continue
    try:
        data_per_alpha_beta[(alpha,beta)].append(row.runtime)
    except KeyError:
        data_per_alpha_beta[(alpha,beta)] = [row.runtime]


# In[6]:


import seaborn as sns


# In[7]:


alphas = set([])
betas = set([])
for alpha,beta in data_per_alpha_beta.keys():
    alphas.add(alpha)
    betas.add(beta)



# In[8]:


alphas = sorted(list(alphas))
betas = sorted(list(betas))


# In[9]:


import numpy as np


# In[10]:


data = np.zeros((len(alphas),len(betas)))


# In[11]:


for k,alpha in enumerate(alphas):
    for l,beta in enumerate(betas):
        data[k,l] = np.mean([x for x in data_per_alpha_beta[(alpha,beta)] if not np.isnan(x)])


# In[34]:


data = pd.DataFrame(data,columns=betas,index=alphas)
#rect = patches.Rectangle((0.01, 0.01), 3.98, 3.98, linewidth=1, edgecolor='r', facecolor='none', angle=0)
fig, ax = plt.subplots(figsize=(7,3.5))
sns.heatmap(data,cmap="Blues",annot=True,annot_kws={"fontsize": 11},cbar_kws={"label":"average computation time (seconds)"})
#plt.gca().add_patch(rect)
plt.xlabel("beta",fontsize=11)
plt.ylabel("alpha",fontsize=11)
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
print(plt.gca().get_xlim())
plt.savefig("alpha_beta_fixed_n.pdf",bbox_inches="tight")
plt.show()
