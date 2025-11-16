#!/bin/bash

for n in {0..49}; do
    sed -i '1s/i//g' "./small_test_10s/alignments/alignment${n}.phylip"
done

for n in {0..49}; do
    sed -i '1s/i//g' "./small_test_5s/alignments/alignment${n}.phylip"
done
