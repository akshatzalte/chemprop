![ChemProp Logo](images/rigr_logo.svg)
# RIGR

Welcome to the user information page for RIGR.  
**60% fewer features, resonance-invariant, and delivering the same high performance!**

Resonance Invariant Graph Representation (RIGR) is a featurizer implemented as part of [**Chemprop v2**](https://github.com/chemprop/chemprop) (available in versions 2.1.2 and above), designed to impose resonance invariance for molecular property prediction tasks.

- **For CLI users**: RIGR is available as a choice for the multi-hot atom featurization scheme. To use RIGR, add the following argument to your training or inference script.
   ```bash
   --multi-hot-atom-featurizer-mode RIGR
   ```
   This sets the atom and bond feature set to be resonance invariant and applies to both non-reaction and reaction featurization. See an example bash script [here](https://github.com/akshatzalte/chemprop/blob/rigr_home/examples/hpopt_train_predict_rigr.sh). If required, the overall molecular charge descriptor can be added to the learned embedding by using `--molecule-featurizer charge`.

    **NOTE**: Ensure consistent featurization scheme for train, predict, and hpopt.

- **For Jupyter Notebook users**: Refer to our [example notebook](https://github.com/chemprop/chemprop/blob/main/examples/rigr_featurizer.ipynb) to use RIGR in a notebook environment.

RIGR is introduced and discussed in our work: [**RIGR: Resonance Invariant Graph Representation for Molecular Property Prediction**](https://chemrxiv.org/engage/chemrxiv/article-details/67c36c29fa469535b9803722). It ensures a unified graph representation of different resonance structures of the same molecule, including non-equivalent resonance forms. By using RIGR, users can avoid manually selecting a specific resonance form for molecules or radicals exhibiting resonance. If you find RIGR helpful in your research, please consider citing our [paper](https://chemrxiv.org/engage/chemrxiv/article-details/67c36c29fa469535b9803722).

RIGR uses only the subset of atom and bond features from Chemprop that remain invariant across different resonance forms. The tables below indicate which atom and bond features are present and absent in RIGR.

### Atom Features

| **Feature**            | **Description**                                                                 | **Present in RIGR?** |
|------------------------|---------------------------------------------------------------------------------|:--------------------:|
| Atomic&nbsp;number     | The choice for atom type denoted by atomic number                                | ☑️                   |
| Degree                 | Number of direct neighbors of the atom                                           | ☑️                    |
| Formal&nbsp;charge     | Integer charge assigned to the atom                                              | ☐                   |
| Chiral&nbsp;tag        | The choices for an atom's chiral tag (See `rdkit.Chem.rdchem.ChiralType`)        | ☐                   |
| Number&nbsp;of&nbsp;H  | Number of bonded hydrogen atoms                                                  | ☑️                   |
| Hybridization          | Atom's hybridization type (See `rdkit.Chem.rdchem.HybridizationType`)            | ☐                   |
| Aromaticity            | Indicates whether the atom is aromatic or not                                    | ☐                   |
| Atomic&nbsp;mass       | The atomic mass of the atom                                                      | ☑️                   |


### Bond Features

| **Feature**           | **Description**                                                                                      | **Present in RIGR?** |
|-----------------------|------------------------------------------------------------------------------------------------------|:--------------------:|
| Bond&nbsp;type        | The known bond types: single, double, or triple bond                                                 | ☐                   |
| Conjugation           | Indicates whether the bond is conjugated or not                                                     | ☐                   |
| Ring                  | Indicates whether the bond is a part of a ring                                                      | ☑️                    |
| Stereochemistry       | Stores the known bond stereochemistries (See [BondStereo](https://www.rdkit.org/docs/source/rdkit.Chem.rdchem.html#rdkit.Chem.rdchem.BondStereo.values)) | ☐                    |

## Branch Guide

The table below provides details on which branch corresponds to specific analyses in our paper:

| Branch Name     | Purpose                                                   |
|------------------|-----------------------------------------------------------|
| [`rigr_home`](https://github.com/akshatzalte/chemprop/tree/rigr_home)     | Home branch with all necessary information to learn about RIGR |
| [`rigr`](https://github.com/akshatzalte/chemprop/tree/rigr) | The branch used for training all the `rigr` models in the [paper](https://github.com/chemprop/chemprop) |
| [`native`](https://github.com/akshatzalte/chemprop/tree/native) | The branch used for training all the `native` and `native+aug` models in the [paper](https://github.com/chemprop/chemprop) |
| [`rigr_charge`](https://github.com/akshatzalte/chemprop/tree/rigr_charge)  | Same as `rigr` but with additional molecule level charge featurizer — used for most of the [property prediction benchmarks](./benchmarks) |
| [`rigr_charge_stereo_chiral`](https://github.com/akshatzalte/chemprop/tree/rigr_charge_stereo_chiral)  | Same as `rigr_charge` but with bond stereochemistry and atom chirality features — used for [RGD1 benchmark](./benchmarks/barrier_rgd1_cnho) |
---

