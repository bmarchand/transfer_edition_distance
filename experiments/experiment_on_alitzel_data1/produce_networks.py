import pandas as pd

for method in ["fitch","sankoff","genesis"]:
    df = pd.read_csv(method+"_input_data.csv")
    
    species_set = set([])
    
    for line in open('species_tree.gr').readlines()[1:]:
        species_set.add(line.split(' ')[0])
        species_set.add(line.split(' ')[1].rstrip('\n:'))
    
    print("species_set", species_set)
    
    for row in df.itertuples():
        print(row.characters,row.fa_list)
        species_list = []
        print(row.fa_list,len(row.fa_list))
        if row.fa_list=="[]":
            continue
        for species in row.fa_list[1:-1].split(','):
            species = species.replace(' ','')
            species = species.replace("<TN:","")
            species = species.replace(">","")
            species_list.append(species)
            assert(species in species_set) 
    
        transfer_edges = []
        for k in range(len(species_list)-1):
            transfer_edges.append(" ".join([species_list[k],species_list[k+1],"transfer"]))
    
        species_tree_lines = open("species_tree.gr").readlines()
        nvertices = species_tree_lines[0].split(' ')[2]
        nedges = int(species_tree_lines[0].split(' ')[3].rstrip('\n'))
    
        nedges += len(transfer_edges)
    
        f = open("networks/"+"_".join([row.characters,method])+".gr","w")
        print(" ".join(["nvertices","nedges",nvertices,str(nedges)]), file=f)
        for line in species_tree_lines[1:]:
            print(line,end="", file=f)
        for transfer in transfer_edges:
            print(transfer,file=f)
        f.close()


## consistency checks
print("consistency checks...")
import os
for fname in os.listdir("networks/"):
    edge_set = set([])
    for line in open("networks/"+fname).readlines()[1:]:
        u = line.split(' ')[0]
        v = line.split(' ')[1].rstrip('\n')
        assert((u,v) not in edge_set)
        edge_set.add((u,v))
print("done")
