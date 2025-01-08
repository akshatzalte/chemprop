![ChemProp Logo](images/rigr_logo.svg)
# RIGR

Welcome to the home branch for RIGR!

Resonance Invariant Graph Representation (RIGR) is a featurizer implemented as a part of Chemprop v2 to impose resonance invariance for molecular property prediction tasks. If using command line interface (CLI), simply add `--rigr` flag to your Chemprop script to train (or infer) your models using this featurizer. For using RIGR in a Jupyter notebook refer to our example notebook [here](https://github.com/akshatzalte/chemprop/blob/rigr_flag/notebooks/rigr_flag_notebook.ipynb). 

RIGR is introduced and discussed in our work: [Resonance Invariant Graph Representation (RIGR) for molecular property prediction](). If RIGR is helpful for your research, please cite our paper.

## Branch Guide

The table below provides details on which branch corresponds to specific analyses in our work:

| Branch Name     | Purpose                                                   |
|------------------|-----------------------------------------------------------|
| [`rigr_home`](https://github.com/akshatzalte/chemprop/tree/rigr_home)     | Home branch with all necessary information to learn about RIGR |
| [`rigr_flag`](https://github.com/akshatzalte/chemprop/tree/rigr_flag) | Implements `rigr` as a flag for easy use in CLI as well as Jupyter notebook |
| [`rigr`](https://github.com/akshatzalte/chemprop/tree/rigr) | The branch used for training all the `rigr` models in the [paper]() |
| [`native`](https://github.com/akshatzalte/chemprop/tree/native) | The branch used for training all the `native` and `native+aug` models in the [paper]() |
| [`rigr_charge`](https://github.com/akshatzalte/chemprop/tree/rigr_charge)  | Same as `rigr` but with additional molecule level charge featurizer -- used for most property prediction benchmarks |
| [`rigr_charge_stereo_chiral`](https://github.com/akshatzalte/chemprop/tree/rigr_charge_stereo_chiral)  | Same as `rigr_charge` but with bond stereochemistry and atom chirality features -- used for [RGD1 benchmark](./benchmarks/barrier_rgd1_cnho) |

---

Chemprop documentation can be found [here](https://chemprop.readthedocs.io/en/main/).
