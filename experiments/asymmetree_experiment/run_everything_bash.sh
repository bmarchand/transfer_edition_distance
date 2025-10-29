#!/bin/bash
NRUNS=$1
NLEAVES=$2
echo "simulation"
python3 asymmetree_simulation.py $NRUNS $NLEAVES
echo "json to gr (species trees)"
for ((i=0; i<NRUNS;i++)); do python3 asymmetree_json_to_gr.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.json > simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr; done
echo "getting true networks"
for ((i=0; i<NRUNS;i++)); do python3 combining_species_gene_trees_into_network.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr simulation_output/simulated_gene_trees/simulated_tree${NLEAVES}leaves_${i}.json > networks/network_${NLEAVES}leaves_${i}.gr; done
for ((i=0; i<NRUNS;i++)); do python3 combining_species_gene_trees_into_unordered_network.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr simulation_output/simulated_gene_trees/simulated_tree${NLEAVES}leaves_${i}.json > networks/network_${NLEAVES}leaves_${i}_unordered.gr; done
echo "producing ranger dtl input"
for ((i=0; i<NRUNS;i++)); do python3 produce_ranger_dtl_input.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.nhx simulation_output/simulated_gene_trees/simulated_tree${NLEAVES}leaves_${i}.json > ranger_dtl_input/ranger_dtl_input_${NLEAVES}leaves_${i}.newick; done
echo "running rangerDTL"
for ((i=0; i<NRUNS;i++)); do ./Ranger-DTL.linux -i ranger_dtl_input/ranger_dtl_input_${NLEAVES}leaves_${i}.newick -o ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}.out; done
echo "reconstruct network predicted by rangerDTL"
for ((i=0; i<NRUNS;i++)); do python3 ranger_dtl_reconstruct_network.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}.out > ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}.gr; done
