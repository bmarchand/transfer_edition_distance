# The arguments are, in order: the number of
# leaves, the number of simulated pairs of
# species tree and gene tree, and the number
# of runs of RangerDTL for each of these pairs
# and each cost value for transfers in the 
# reconciliation.

NLEAVES_SHORT = 10
NSIMULRUNS_SHORT = 5
NRECONC_SHORT = 5

NLEAVES_LONG = 50
NSIMULRUNS_LONG = 20
NRECONC_LONG = 50

all: clean
	./run_simulations_and_ranger_dtl.sh $(NLEAVES_SHORT) $(NSIMULRUNS_SHORT) $(NRECONC_SHORT)
	./compute_distances.sh $(NLEAVES_SHORT) $(NSIMULRUNS_SHORT) $(NRECONC_SHORT)
	python3 transfer_cost_calibration_figure.py $(NLEAVES_SHORT) $(NSIMULRUNS_SHORT) $(NRECONC_SHORT)

complete: clean
	./run_simulations_and_ranger_dtl.sh $(NLEAVES_LONG) $(NSIMULRUNS_LONG) $(NRECONC_LONG)
	./compute_distances.sh $(NLEAVES_LONG) $(NSIMULRUNS_LONG) $(NRECONC_LONG)
	python3 transfer_cost_calibration_figure.py $(NLEAVES_LONG) $(NSIMULRUNS_LONG) $(NRECONC_LONG)

clean:
	rm -f ranger_dtl_output/*.gr
	rm -f ranger_dtl_output/*out*
	rm -f results_nleaves*_nruns*_nreconcruns*_T*
	rm -f networks/*.gr
