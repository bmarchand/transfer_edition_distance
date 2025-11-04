#!/bin/bash
NLEAVES=$1
NRUNS=$2
NRECONCRUNS=$3
echo "init file" > "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}";
for ((i=0; i<NRUNS;i++)); do 
    echo "nleaves ${NLEAVES} num ${i}"; 
    echo "nleaves ${NLEAVES} num ${i}" >> "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}"; 
    for ((j=0; j < NRECONCRUNS; j++)); do 
        echo ${j} >> "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}";  
        ~/Documents/meta_rep/postdoc_projects/transfer_edition_distance/ted_module/target/release/ted_module --weighted --unordered networks/network_${NLEAVES}leaves_${i}_unordered.gr ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}_${j}.gr >> "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}"; done; done
for ((i=0; i<NRUNS;i++)); do 
    echo "aggregated network ${NLEAVES} num ${i}" >> "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}"; 
    ~/Documents/meta_rep/postdoc_projects/transfer_edition_distance/ted_module/target/release/ted_module --unordered --weighted networks/network_${NLEAVES}leaves_${i}_unordered.gr weighted_reconstructions/weighted_network${NLEAVES}leaves_${i}.wgr >> "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}"; done
