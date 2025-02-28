# Notebooks

This section contains a collection of notebooks essential to our work on developing and evaluating RIGR. Most of these notebooks require a local copy of the primary dataset, which can be accessed [here](https://zenodo.org/records/14942335).

## Resonance SMILES Generation and Data Augmentation

We provide a notebook (`resonance_generation_and_augmentation.ipynb`) for generating a representative set of resonance structures and their corresponding SMILES strings for radicals or closed-shell species. This includes an example of data augmentation for resonance, which can be integrated into your workflow when working with resonance-active chemical species.

## Training with RIGR

An example Jupyter notebook demonstrating how to train and infer models using the RIGR featurizer is available [here](https://github.com/chemprop/chemprop/blob/main/examples/rigr_featurizer.ipynb). RIGR eliminates the need for tedious data augmentation and also reduces training costs.
