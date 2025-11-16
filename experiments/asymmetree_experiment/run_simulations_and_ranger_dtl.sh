#!/bin/bash
NLEAVES=$1
NRUNS=$2
NRECONCRUNS=$3
echo "simulation"
python3 asymmetree_simulation.py $NRUNS $NLEAVES
echo "json to gr (species trees)"
for ((i=0; i<NRUNS;i++)); do python3 asymmetree_json_to_gr.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.json > simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr; done
echo "getting true networks"
#for ((i=0; i<NRUNS;i++)); do python3 combining_species_gene_trees_into_network.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr simulation_output/simulated_gene_trees/simulated_tree${NLEAVES}leaves_${i}.json > networks/network_${NLEAVES}leaves_${i}.gr; done
for ((i=0; i<NRUNS;i++)); do python3 combining_species_gene_trees_into_unordered_network.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr simulation_output/simulated_gene_trees/simulated_tree${NLEAVES}leaves_${i}.json > networks/network_${NLEAVES}leaves_${i}_unordered.gr; done
echo "producing ranger dtl input"
for ((i=0; i<NRUNS;i++)); do python3 produce_ranger_dtl_input.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.nhx simulation_output/simulated_gene_trees/simulated_tree${NLEAVES}leaves_${i}.json > ranger_dtl_input/ranger_dtl_input_${NLEAVES}leaves_${i}.newick; done
echo "running rangerDTL"
for T in {10,20,30,40,50,60,70,80,90}; do 
    for ((i=0; i<NRUNS;i++)); do 
        for ((j=0; j<NRECONCRUNS; j++)); do 
            ./Ranger-DTL.linux -D 10 -T ${T} -L 10 -i ranger_dtl_input/ranger_dtl_input_${NLEAVES}leaves_${i}.newick -o ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}_${T}.out${j}; done; done; done
echo "reconstruct network predicted by rangerDTL"
for T in {10,20,30,40,50,60,70,80,90}; do 
    for ((i=0; i<NRUNS;i++)); do 
        for ((j=0; j<NRECONCRUNS; j++)); do 
            python3 ranger_dtl_reconstruct_network.py simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}_${T}.out${j} > ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}_${j}_T${T}.gr; done; done; done
#echo "reconstruct weighted network predicted by rangerDTL"
#for ((i=0; i<NRUNS;i++)); do python3 ranger_dtl_reconstruct_aggregated_network.py ${NRECONCRUNS} simulation_output/simulated_species_trees/species_tree${NLEAVES}leaves_${i}.gr ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}.out > weighted_reconstructions/weighted_network${NLEAVES}leaves_${i}.wgr; done 




#echo "running AggregateRanger"
#for ((i=0; i<NRUNS;i++)); do ./AggregateRanger.linux ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}.out; done
