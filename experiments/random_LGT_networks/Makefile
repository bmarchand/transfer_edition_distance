all : small_experiment

small_experiment : clean run_small_experiment
complete : clean run_complete_experiment

run_small_experiment: figures_small

figures_small: benchmark_small.csv
	python3 rtime_against_ntaxa.py small
	python3 fixed_n_alpha_beta.py small

benchmark_small.csv:
	python3 level_k_lgt_generator.py small
	python3 run_distance_computations.py small

run_complete_experiment: figures_complete

figures_complete: benchmark_complete.csv
	python3 rtime_against_ntaxa.py complete
	python3 fixed_n_alpha_beta.py complete

benchmark_complete.csv:
	python3 level_k_lgt_generator.py complete
	python3 run_distance_computations.py complete

clean:
	rm -f generated_networks/*.gr
