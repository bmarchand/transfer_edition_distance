# Tree-based networks projects

Definitions
Messy project: https://github.com/AliLopSan/ptns/tree/main
Clean project: https://github.com/AliLopSan/Genesis-Sankoff/tree/main

##	Pre-requirements
Things you want to install before running anything
 - Asymmetree: https://github.com/david-schaller/AsymmeTree
 - Tralda: https://github.com/david-schaller/tralda/

## Genesis project
###	Data source and description
1) Species Tree was generated using the NCBI Taxonomy database.
 - Full list of species with IDs to crossreference between databases can be found here: https://github.com/AliLopSan/ptns/blob/main/real_data/interphylum_species_50.csv
 - Newick string as given by NCBI taxonomy database can be found here: https://github.com/AliLopSan/ptns/blob/main/real_data/inter_phylum.phy
 - I also have pickled the species tree object for ease of use with Asymmetree: https://github.com/AliLopSan/Genesis-Sankoff/blob/main/data/genesis_labeling_analysis/input_data/species_tree_ultra.pkl
2) 180 KOs (input characters). They correspond to functions related to antibiotic resistance.
Full list can be found here: https://github.com/AliLopSan/ptns/blob/main/real_data/ARG_related_KOs.csv

## 	Interesting results (Your input)
In: https://github.com/AliLopSan/Genesis-Sankoff/tree/main/results
You will find the three labeling methods:
 - Fitch Labeling analysis
 - Genesis Labeling analysis
 - Sankoff Labeling analysis
 - 
Each one (and their cost variants) contains two important files: 
 - **FA_info_full_labeling_method**: Full info on first appearances (changes from 0 to 1) per character. There are three columns (character, number of first appearances, full list of first appearances ). In theory, greedily connecting this list of first appearances per character yields a PTN or a homoplasy-free scenario. See article for details :)
 - **labeling method_hw_info**: List of found transfer highways. Transfer highways are pairs of nodes in the species tree that appear in the first appearance list described above for many characters.  The form of this file is (endpoint1, endpoint2, weight) where weight indicates the number of characters that share the highway.

