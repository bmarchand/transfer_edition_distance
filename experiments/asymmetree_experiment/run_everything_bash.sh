#!/bin/bash
./run_simulations_and_ranger_dtl.sh 50 20 50
./compute_distances.sh 50 20 50
python3 transfer_cost_calibration_figure.py
