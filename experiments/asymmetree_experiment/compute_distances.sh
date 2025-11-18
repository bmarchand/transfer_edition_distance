#!/bin/bash
NLEAVES=$1
NRUNS=$2
NRECONCRUNS=$3

for T in {10,20,30,40,50,60,70,80,90}; do 
    echo "init file" > "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}_T${T}";
    for ((i=0; i<NRUNS;i++)); do 
        echo "nleaves ${NLEAVES} num ${i}"; 
        echo "nleaves ${NLEAVES} num ${i}" >> "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}_T${T}"; 
        for ((j=0; j < NRECONCRUNS; j++)); do 
            echo ${j} >> "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}_T${T}";  
            echo networks/network_${NLEAVES}leaves_${i}_unordered.gr ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}_${j}_T${T}.gr;
            python3 total_weight.py networks/network_${NLEAVES}leaves_${i}_unordered.gr ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}_${j}_T${T}.gr >> "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}_T${T}";
            ../../target/release/ted_module --unordered networks/network_${NLEAVES}leaves_${i}_unordered.gr ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}_${j}_T${T}.gr >> "results_nleaves${NLEAVES}_nruns${NRUNS}_nreconcruns${NRECONCRUNS}_T${T}"; done; done; done
