#!/bin/bash
NRUNS=$1
NLEAVES=$2
for ((i=0; i<NRUNS;i++)); do echo "nleaves ${NLEAVES} num ${i}"; ~/Documents/meta_rep/postdoc_projects/transfer_edition_distance/ted_module/target/release/ted_module networks/network_${NLEAVES}leaves_${i}_unordered.gr ranger_dtl_output/ranger_dtl_reconciliation_${NLEAVES}leaves_${i}.gr --unordered; done
