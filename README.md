![ChemProp Logo](images/rigr_logo.svg)
# RIGR

Welcome to the home branch for RIGR!

Resonance Invariant Graph Representation (RIGR) is a featurizer implemented as a part of Chemprop v2 to impose resonance invariance for molecular property prediction tasks. If using command line interface (CLI), simply add `--rigr` flag to your Chemprop script to train (or infer) your models using this featurizer. For using RIGR in a Jupyter notebook refer to our example notebook [here](https://github.com/akshatzalte/chemprop/blob/rigr_flag/notebooks/rigr_flag_notebook.ipynb). 

RIGR is introduced and discussed in our work, which can be found [here](). If RIGR is helpful for your research, please cite our paper.

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


Documentation can be found [here](https://chemprop.readthedocs.io/en/main/).

There are tutorial notebooks in the [`examples/`](https://github.com/chemprop/chemprop/tree/main/examples) directory.

Chemprop recently underwent a ground-up rewrite and new major release (v2.0.0). A helpful transition guide from Chemprop v1 to v2 can be found [here](https://docs.google.com/spreadsheets/u/3/d/e/2PACX-1vRshySIknVBBsTs5P18jL4WeqisxDAnDE5VRnzxqYEhYrMe4GLS17w5KeKPw9sged6TmmPZ4eEZSTIy/pubhtml). This includes a side-by-side comparison of CLI argument options, a list of which arguments will be implemented in later versions of v2, and a list of changes to default hyperparameters.

**License:** Chemprop is free to use under the [MIT License](LICENSE.txt). The Chemprop logo is free to use under [CC0 1.0](docs/source/_static/images/logo/LICENSE.txt).

**References**: Please cite the appropriate papers if Chemprop is helpful to your research.

- Chemprop was initially described in the papers [Analyzing Learned Molecular Representations for Property Prediction](https://pubs.acs.org/doi/abs/10.1021/acs.jcim.9b00237) for molecules and [Machine Learning of Reaction Properties via Learned Representations of the Condensed Graph of Reaction](https://doi.org/10.1021/acs.jcim.1c00975) for reactions.
- The interpretation functionality (available in v1, but not yet implemented in v2) is based on the paper [Multi-Objective Molecule Generation using Interpretable Substructures](https://arxiv.org/abs/2002.03244).
- Chemprop now has its own dedicated manuscript that describes and benchmarks it in more detail: [Chemprop: A Machine Learning Package for Chemical Property Prediction](https://doi.org/10.1021/acs.jcim.3c01250).
- A paper describing and benchmarking the changes in v2.0.0 is forthcoming.

**Selected Applications**: Chemprop has been successfully used in the following works.

- [A Deep Learning Approach to Antibiotic Discovery](https://www.cell.com/cell/fulltext/S0092-8674(20)30102-1) - _Cell_ (2020): Chemprop was used to predict antibiotic activity against _E. coli_, leading to the discovery of [Halicin](https://en.wikipedia.org/wiki/Halicin), a novel antibiotic candidate. Model checkpoints are availabile on [Zenodo](https://doi.org/10.5281/zenodo.6527882).
- [Discovery of a structural class of antibiotics with explainable deep learning](https://www.nature.com/articles/s41586-023-06887-8) - _Nature_ (2023): Identified a structural class of antibiotics selective against methicillin-resistant _S. aureus_ (MRSA) and vancomycin-resistant enterococci using ensembles of Chemprop models, and explained results using Chemprop's interpret method.
- [ADMET-AI: A machine learning ADMET platform for evaluation of large-scale chemical libraries](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btae416/7698030?utm_source=authortollfreelink&utm_campaign=bioinformatics&utm_medium=email&guestAccessKey=f4fca1d2-49ec-4b10-b476-5aea3bf37045): Chemprop was trained on 41 absorption, distribution, metabolism, excretion, and toxicity (ADMET) datasets from the [Therapeutics Data Commons](https://tdcommons.ai). The Chemprop models in ADMET-AI are available both as a web server at [admet.ai.greenstonebio.com](https://admet.ai.greenstonebio.com) and as a Python package at [github.com/swansonk14/admet_ai](https://github.com/swansonk14/admet_ai).
- A more extensive list of successful Chemprop applications is given in our [2023 paper](https://doi.org/10.1021/acs.jcim.3c01250)

## Version 1.x

For users who have not yet made the switch to Chemprop v2.0, please reference the following resources.

### v1 Documentation

- Documentation of Chemprop v1 is available [here](https://chemprop.readthedocs.io/en/v1.7.1/). Note that the content of this site is several versions behind the final v1 release (v1.7.1) and does not cover the full scope of features available in chemprop v1.
- The v1 [README](https://github.com/chemprop/chemprop/blob/v1.7.1/README.md) is the best source for documentation on more recently-added features.
- Please also see descriptions of all the possible command line arguments in the v1 [`args.py`](https://github.com/chemprop/chemprop/blob/v1.7.1/chemprop/args.py) file.

### v1 Tutorials and Examples

- [Benchmark scripts](https://github.com/chemprop/chemprop_benchmark) - scripts from our 2023 paper, providing examples of many features using Chemprop v1.6.1
- [ACS Fall 2023 Workshop](https://github.com/chemprop/chemprop-workshop-acs-fall2023) - presentation, interactive demo, exercises on Google Colab with solution key
- [Google Colab notebook](https://colab.research.google.com/github/chemprop/chemprop/blob/v1.7.1/colab_demo.ipynb) - several examples, intended to be run in Google Colab rather than as a Jupyter notebook on your local machine
- [nanoHUB tool](https://nanohub.org/resources/chempropdemo/) - a notebook of examples similar to the Colab notebook above, doesn't require any installation
  - [YouTube video](https://www.youtube.com/watch?v=TeOl5E8Wo2M) - lecture accompanying nanoHUB tool
- These [slides](https://docs.google.com/presentation/d/14pbd9LTXzfPSJHyXYkfLxnK8Q80LhVnjImg8a3WqCRM/edit?usp=sharing) provide a Chemprop tutorial and highlight additions as of April 28th, 2020

### v1 Known Issues

We have discontinued support for v1 since v2 has been released, but we still appreciate v1 bug reports and will tag them as [`v1-wontfix`](https://github.com/chemprop/chemprop/issues?q=label%3Av1-wontfix+) so the community can find them easily.
