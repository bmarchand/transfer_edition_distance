## Source code for the experiments of "On the Comparison of LGT networks and Tree-based Networks"


| experiment   | description                                             |                  folder |
|--------------|---------------------------------------------------------|-------------------------|
| experiment 1 | benchmark on random LGT networks                        |      random_LGT_networks|
| experiment 2 | comparison of networks built by character-based methods | character_based_methods |
| experiment 3 | calibration of transfer costs with simulated gene trees | asymmetree_experiment   |

### network visualizer
This short script is to be used as follows:
```
python3 network_visualizer.py path/to/network.gr
```

where ``network.gr`` is essentially a list of edges of a network. An example is given in this folder ``network_example.gr``.
