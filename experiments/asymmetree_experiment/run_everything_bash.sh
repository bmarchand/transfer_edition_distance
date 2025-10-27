#!/bin/bash
NRUNS=10
NLEAVES=5
python3 asymmetree_simulation.py $NRUNS $NLEAVES
for ((i=0; i<NRUNS;i++)); do python3 asymmetree_json_to_gr.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.json > simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr; done
for ((i=0; i<NRUNS;i++)); do python3 asymmetree_json_to_gr.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.json > simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr; done
for ((i=0; i<NRUNS;i++)); do python3 combining_species_gene_trees_into_network.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr simulation_output/simulated_gene_trees/simulated_tree${NLEAVES}leaves_${i}.json > networks/network_${NLEAVES}leaves_${i}.gr; done
for ((i=0; i<NRUNS;i++)); do python3 produce_ranger_dtl_input.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.nhx simulation_output/simulated_gene_trees/simulated_tree${NLEAVES}leaves_${i}.json; done

