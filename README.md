# Transfer edition distance for LGT networks

This is the companion repository of INSERTPREPRINTLINK.
It contains the rust implementation of the **transfer edition distance
for LGT networks** that the article presents.

## Dependencies

We suggest creating a python virtual environment using:
```
python3 -m venv lgt_env
source lgt_env/bin/activate
```

The python dependencies (for running the experiments and installing the rust
code as a python module) may be installed with:
```
pip install -r requirements.txt
```

The algorithms for computing the distance itself have been implemented in Rust.
To be able to compile and use it, you need to [install
rust](https://rust-lang.org/tools/install/).

## Building and running distance computations

The rust library can be compiled with
```
cargo build --release
```
and installed as a python module called ``ted_module`` using:
```
maturin develop --release
```

### small example test
For the **ordered** version of the distance
```
./target/release/ted_module tests/small_network1.gr tests/small_network2.gr
```
For the **unordered** version:
```
./target/release/ted_module --unordered /small_network1.gr tests/small_network2.gr
```

Examples of how to call the method from python can be found in this [test file](tests/test_distance_computation.py).

## Experiments

Steps to reproduce the experiments of the paper can be found in the following respective folders:
- **Scalability analysis on random LGT networks**: [experiments/random_LGT_networks/](experiments/random_LGT_networks)
- **Pairwise comparison of several character-based methods**: [experiments/character_based_methods/](experiments/character_based_methods)
- **Example of a calibration of the cost of transfers for reconciliation**: [experiments/asymmetree_experiment/](experiments/asymmetree_experiment)


### network visualizer
This short script is to be used as follows:
```
python3 network_visualizer.py path/to/network.gr
```

where ``network.gr`` is essentially a list of edges of a network. An example is given here [experiments/network_example.gr](experiments/network_example.gr).
