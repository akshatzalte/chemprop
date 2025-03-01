# %% [markdown]
# # Just setting up

# %% [markdown]
# ### Customize Chemprop featurizers for SHAP analysis

# %%
# Import dependencies and classes
import sys
sys.path.insert(0, '/home/akshatz/bond_order_free/chemprop') # change to your chemprop path if not developmentally installed

from copy import deepcopy
from lightning import pytorch as pl
from pathlib import Path

import pandas as pd
import numpy as np
import torch

from dataclasses import InitVar, dataclass
from typing import List, Sequence, Tuple, Union, Optional
from rdkit import Chem
from rdkit.Chem import Mol, Draw
from rdkit.Chem.rdchem import Atom, Bond, BondType

from chemprop.featurizers.atom import MultiHotAtomFeaturizer ; # semicolon to suppress output
from chemprop.featurizers.bond import MultiHotBondFeaturizer ;
from chemprop.featurizers.molgraph.molecule import SimpleMoleculeMolGraphFeaturizer ;

from chemprop.data.molgraph import MolGraph ;
from chemprop.featurizers.base import GraphFeaturizer ;
from chemprop.featurizers.molgraph.mixins import _MolGraphFeaturizerMixin ;
from chemprop.utils.utils import make_mol ;

from chemprop import data, featurizers, models ;

import shap # do "pip install shap" if you don't have it installed

import logging

# Set logging level to WARNING to suppress INFO logs
logging.getLogger("lightning.pytorch.utilities.rank_zero").setLevel(logging.WARNING)

# %% [markdown]
# #### CustomMultiHotAtomFeaturizer

# %%
class CustomMultiHotAtomFeaturizer(MultiHotAtomFeaturizer):
    """A custom MultiHotAtomFeaturizer that allows for selective feature ablation.
        
    Parameters
    ----------
    keep_features : List[bool], optional
    a list of booleans to indicate which atom features to keep. If None, all features are kept. If False, corresponding feature is set to zeros. Useful for ablation and SHAP analysis.
    """
    
    def __init__(self,
                 atomic_nums: Sequence[int],
                 degrees: Sequence[int],
                 formal_charges: Sequence[int],
                 chiral_tags: Sequence[int],
                 num_Hs: Sequence[int],
                 hybridizations: Sequence[int],
                 keep_features: List[bool] = None):
        super().__init__(atomic_nums, degrees, formal_charges, chiral_tags, num_Hs, hybridizations)
        
        if keep_features is None:
            keep_features = [True] * (len(self._subfeats) + 2)
        self.keep_features = keep_features

    def __call__(self, a: Atom | None) -> np.ndarray:
        x = np.zeros(self._MultiHotAtomFeaturizer__size)
        if a is None:
            return x
        
        feats = [
            a.GetAtomicNum(),
            a.GetTotalDegree(),
            a.GetFormalCharge(),
            int(a.GetChiralTag()),
            int(a.GetTotalNumHs()),
            a.GetHybridization(),
        ]
        
        i = 0
        for feat, choices, keep in zip(feats, self._subfeats, self.keep_features[:len(feats)]):
            j = choices.get(feat, len(choices))
            if keep:
                x[i + j] = 1
            i += len(choices) + 1
        
        if self.keep_features[len(feats)]:
            x[i] = int(a.GetIsAromatic())
        if self.keep_features[len(feats) + 1]:
            x[i + 1] = 0.01 * a.GetMass()

        return x

    def zero_mask(self) -> np.ndarray:
        """Featurize the atom by setting all bits to zero."""
        return np.zeros(len(self))

# %%
# Example usage
atomic_nums = [6, 7, 8]
degrees = [1, 2, 3]
formal_charges = [-1, 0, 1]
chiral_tags = [0, 1, 2]
num_Hs = [0, 1, 2]
hybridizations = [1, 2, 3]

keep_features_all = [True] * 8
keep_features_some = [True, True, False, True, False, True, True, False]
keep_features_none = [False] * 8

featurizer_all = CustomMultiHotAtomFeaturizer(
    atomic_nums=atomic_nums,
    degrees=degrees,
    formal_charges=formal_charges,
    chiral_tags=chiral_tags,
    num_Hs=num_Hs,
    hybridizations=hybridizations,
    keep_features=keep_features_all
)

featurizer_some = CustomMultiHotAtomFeaturizer(
    atomic_nums=atomic_nums,
    degrees=degrees,
    formal_charges=formal_charges,
    chiral_tags=chiral_tags,
    num_Hs=num_Hs,
    hybridizations=hybridizations,
    keep_features=keep_features_some
)

featurizer_none = CustomMultiHotAtomFeaturizer(
    atomic_nums=atomic_nums,
    degrees=degrees,
    formal_charges=formal_charges,
    chiral_tags=chiral_tags,
    num_Hs=num_Hs,
    hybridizations=hybridizations,
    keep_features=keep_features_none
)

mol = Chem.MolFromSmiles('CCO')
atom = mol.GetAtomWithIdx(0)  # Get the first atom

features = featurizer_all(atom)
print("Atom features all:", features)

features = featurizer_some(atom)
print("Atom features some:", features)

features = featurizer_none(atom)
print("Atom features none:", features)

# %% [markdown]
# #### CustomMultiHotBondFeaturizer

# %%
class CustomMultiHotBondFeaturizer(MultiHotBondFeaturizer):
    """A custom MultiHotBondFeaturizer that allows for selective feature ablation.
    
    Parameters
    ----------
    keep_features : List[bool], optional
    a list of booleans to indicate which bond features to keep except for nullity. If None, all features are kept. If False, corresponding feature is set to zeros. Useful for ablation and SHAP analysis.
    """
    
    def __init__(self,
                 bond_types: Sequence[BondType] | None = None,
                 stereos: Sequence[int] | None = None,
                 keep_features: List[bool] = None):
        super().__init__(bond_types, stereos)
        
        self._MultiHotBondFeaturizer__size = 1 + len(self.bond_types) + 2 + (len(self.stereo) + 1)

        if keep_features is None:
            keep_features = [True] * 4 
        self.keep_features = keep_features        

    def __len__(self) -> int:
        return self._MultiHotBondFeaturizer__size

    def __call__(self, b: Bond) -> np.ndarray:
        x = np.zeros(len(self), int)

        if b is None:
            x[0] = 1
            return x
        i = 1
        bond_type = b.GetBondType()
        bt_bit, size = self.one_hot_index(bond_type, self.bond_types)
        if self.keep_features[0] and bt_bit != size:
            x[i + bt_bit] = 1
        i += size - 1

        if self.keep_features[1]:
            x[i] = int(b.GetIsConjugated())
        if self.keep_features[2]:
            x[i + 1] = int(b.IsInRing())
        i += 2

        if self.keep_features[3]:
            stereo_bit, _ = self.one_hot_index(int(b.GetStereo()), self.stereo)
            x[i + stereo_bit] = 1

        return x

    def zero_mask(self) -> np.ndarray:
        """Featurize the bond by setting all bits to zero."""
        return np.zeros(len(self), int)

    @classmethod
    def one_hot_index(cls, x, xs: Sequence) -> tuple[int, int]:
        """Returns a tuple of the index of ``x`` in ``xs`` and ``len(xs) + 1`` if ``x`` is in ``xs``.
        Otherwise, returns a tuple with ``len(xs)`` and ``len(xs) + 1``."""
        n = len(xs)
        return xs.index(x) if x in xs else n, n + 1

# %%
# Example usage
bond_types = [BondType.SINGLE, BondType.DOUBLE, BondType.TRIPLE, BondType.AROMATIC]
stereos = [0, 1, 2, 3, 4, 5]
keep_features_all = [True] * 4
keep_features_some = [True, False, True, False]
keep_features_none = [False] * 4

featurizer_all = CustomMultiHotBondFeaturizer(
    bond_types=bond_types,
    stereos=stereos,
    keep_features=keep_features_all
)

featurizer_some = CustomMultiHotBondFeaturizer(
    bond_types=bond_types,
    stereos=stereos,
    keep_features=keep_features_some
)

featurizer_none = CustomMultiHotBondFeaturizer(
    bond_types=bond_types,
    stereos=stereos,
    keep_features=keep_features_none
)

mol = Chem.MolFromSmiles('CCO')
bond = mol.GetBondWithIdx(0)  # Get the first bond

features = featurizer_all(bond)
print("Bond features all:", features)

features = featurizer_some(bond)
print("Bond features some:", features)

features = featurizer_none(bond)
print("Bond features none:", features)

# %% [markdown]
# #### CustomSimpleMoleculeMolGraphFeaturizer

# %%
@dataclass
class CustomSimpleMoleculeMolGraphFeaturizer(SimpleMoleculeMolGraphFeaturizer):
    """A custom SimpleMoleculeMolGraphFeaturizer with additional feature control."""
    
    keep_atom_features: Optional[List[bool]] = None
    keep_bond_features: Optional[List[bool]] = None
    keep_atoms: Optional[List[bool]] = None
    keep_bonds: Optional[List[bool]] = None

    def __post_init__(self, extra_atom_fdim: int = 0, extra_bond_fdim: int = 0):
        super().__post_init__(extra_atom_fdim, extra_bond_fdim)

        if isinstance(self.atom_featurizer, CustomMultiHotAtomFeaturizer) and self.keep_atom_features is not None:
            self.atom_featurizer.keep_features = self.keep_atom_features
        if isinstance(self.bond_featurizer, CustomMultiHotBondFeaturizer) and self.keep_bond_features is not None:
            self.bond_featurizer.keep_features = self.keep_bond_features

    def __call__(
        self,
        mol: Chem.Mol,
        atom_features_extra: np.ndarray | None = None,
        bond_features_extra: np.ndarray | None = None,
    ) -> MolGraph:
        n_atoms = mol.GetNumAtoms()
        n_bonds = mol.GetNumBonds()

        if self.keep_atoms is None:
            self.keep_atoms = [True] * n_atoms
        if self.keep_bonds is None:
            self.keep_bonds = [True] * n_bonds

        if atom_features_extra is not None and len(atom_features_extra) != n_atoms:
            raise ValueError(
                "Input molecule must have same number of atoms as `len(atom_features_extra)`!"
                f"got: {n_atoms} and {len(atom_features_extra)}, respectively"
            )
        if bond_features_extra is not None and len(bond_features_extra) != n_bonds:
            raise ValueError(
                "Input molecule must have same number of bonds as `len(bond_features_extra)`!"
                f"got: {n_bonds} and {len(bond_features_extra)}, respectively"
            )
        if n_atoms == 0:
            V = np.zeros((1, self.atom_fdim), dtype=np.single)
        else:
            V = np.array([self.atom_featurizer(a) if self.keep_atoms[a.GetIdx()] else self.atom_featurizer.zero_mask()
                          for a in mol.GetAtoms()], dtype=np.single)

        if atom_features_extra is not None:
            V = np.hstack((V, atom_features_extra))

        E = np.empty((2 * n_bonds, self.bond_fdim))
        edge_index = [[], []]

        i = 0
        for u in range(n_atoms):
            for v in range(u + 1, n_atoms):
                bond = mol.GetBondBetweenAtoms(u, v)
                if bond is None:
                    continue

                x_e = self.bond_featurizer(bond) if self.keep_bonds[bond.GetIdx()] else self.bond_featurizer.zero_mask()

                if bond_features_extra is not None:
                    x_e = np.concatenate((x_e, bond_features_extra[bond.GetIdx()]), dtype=np.single)

                E[i: i + 2] = x_e
                edge_index[0].extend([u, v])
                edge_index[1].extend([v, u])
                i += 2

        rev_edge_index = np.arange(len(E)).reshape(-1, 2)[:, ::-1].ravel()
        edge_index = np.array(edge_index, int)
        return MolGraph(V, E, edge_index, rev_edge_index)

# %%
# Example usage
atom_featurizer = CustomMultiHotAtomFeaturizer(
    atomic_nums=[6, 7, 8],
    degrees=[1, 2, 3],
    formal_charges=[-1, 0, 1],
    chiral_tags=[0, 1, 2],
    num_Hs=[0, 1, 2],
    hybridizations=[1, 2, 3],
    keep_features=[True, True, False, True, False, True, True, False]
)

bond_featurizer = CustomMultiHotBondFeaturizer(
    bond_types=[BondType.SINGLE, BondType.DOUBLE, BondType.TRIPLE, BondType.AROMATIC],
    stereos=[0, 1, 2, 3, 4, 5],
    keep_features=[True, False, True, False]
)

featurizer = CustomSimpleMoleculeMolGraphFeaturizer(
    atom_featurizer=atom_featurizer,
    bond_featurizer=bond_featurizer,
    keep_atom_features=[True, True, False, True, False, True, True, False],
    keep_bond_features=[True, False, True, False],
)

# Example molecule (RDKit Mol object required)
from rdkit import Chem
mol = Chem.MolFromSmiles('CCO')

mol_graph = featurizer(mol)
print("Molecule graph:", mol_graph)

# %% [markdown]
# # SHAP analysis

# %% [markdown]
# ## saving the values for 1 split and all weight initializations

# %%
from tqdm import tqdm
from pathlib import Path
chemprop_dir = Path.cwd().parent

# %%
# A helper function to get predictions from a molecule with ability to keep or remove specific atom and bond features
def get_predictions(keep_atom_features: Optional[List[bool]], keep_bond_features: Optional[List[bool]], mol: str, trainer) -> float:
    featurizer = CustomSimpleMoleculeMolGraphFeaturizer(
        atom_featurizer=atom_featurizer,
        bond_featurizer=bond_featurizer,
        keep_atom_features=keep_atom_features,
        keep_bond_features=keep_bond_features
    )
    test_data = [data.MoleculeDatapoint(make_mol(mol, True, True))]
    test_dset = data.MoleculeDataset(test_data, featurizer=featurizer)
    test_loader = data.build_dataloader(test_dset, shuffle=False)

    with torch.inference_mode():
        
        test_preds = trainer.predict(mpnn, test_loader)
    return test_preds[0][0]


# An example wrapper class for use as the model input in SHAP explainer
# The wrapper needs to be initialized first with the molecule to be explained, and then can be called with a boolean list representing the features to keep
# The wrapper is needed because SHAP explainer requires a callable model with a single input argument, adapt X as needed
class MoleculeModelWrapper:
    def __init__(self, mols: str, trainer):
        self.mol = mols
        self.trainer = trainer
    
    def __call__(self, X):
        preds = []
        for keep_features in X:
            try:
                # unpacking X, indices corresponds to feature orders from default chemprop featurizer, adapt as needed
                keep_atom_features = keep_features[:8] # 8 atom features
                keep_bond_features = keep_features[8:] # 4 bond features
            except:
                print(f"Invalid input: {keep_features}")
                raise
            pred = get_predictions(keep_atom_features, keep_bond_features, self.mol, self.trainer)
            preds.append([pred.item()])
        return np.array(preds)

# An example masker function for use with SHAP explainer
# The masker function takes in a binary mask and the input data X, and returns the masked input data. This simulates the effect of masking out certain features.
def binary_masker(binary_mask, x):
    masked_x = deepcopy(x)
    masked_x[binary_mask == 0] = 0
    return np.array([masked_x])

def get_values(test_mol, trainer):
    model_wrapper = MoleculeModelWrapper(test_mol, trainer=trainer)
    explainer = shap.PermutationExplainer(model_wrapper, masker=binary_masker)
    explanation = explainer(feature_choice, max_evals=1000)
    return explanation.base_values, explanation.values

# %% [markdown]
# ## random

# %%
for k in range(5):
    # load chemprop model checkpoint file
    checkpoint_path = f'/home/akshatz/bond_order_free/rigr_h298_50k/run1_baseline/chemprop_training/final_data_set/2024-08-18T03-35-06/fold_0/model_{k}/best.pt'
    mpnn = models.MPNN.load_from_file(checkpoint_path)

    # load data
    test_path = "/home/akshatz/bond_order_free/rigr_h298_50k/dataset/final_test.csv"
    smiles_column = 'resonance_smis'
    df_test = pd.read_csv(test_path)
    smis = df_test[smiles_column]
    test_data = [data.MoleculeDatapoint.from_smi(smi) for smi in smis]
    test_mol = smis.iloc[0]
    # initialize featurizer
    atom_featurizer = CustomMultiHotAtomFeaturizer.v2()
    bond_featurizer = CustomMultiHotBondFeaturizer()
    trainer = pl.Trainer(
        logger=False,
        # checkpoint_callback=False,
        callbacks=False,
        enable_progress_bar=False,
        enable_checkpointing=False,
        accelerator="cpu",
        devices=1
    )

    keep_features = [1] * 12  # 8 atom features + 4 bond features
    feature_choice = np.array([keep_features])

    save_path = Path(f'random/shapley_az_baseline_model_{k}')
    save_path.mkdir(exist_ok=True)
    
    for i, test_mol in tqdm(enumerate(smis)):
        base_value_path = save_path / f"{i}_base_value.npy"
        values_path = save_path / f"{i}_values.npy"
        norm_values_path = save_path / f"{i}_norm_values.npy"
        if base_value_path.exists() and values_path.exists():
            continue
        base_value, values = get_values(test_mol, trainer)
        norm_values = values / base_value
        np.save(norm_values_path, norm_values)
        np.save(base_value_path, base_value)
        np.save(values_path, values)

# %% [markdown]
# ## k-means

# %%
for k in range(5):
    # load chemprop model checkpoint file
    checkpoint_path = f'/home/akshatz/bond_order_free/k_means/rigr_h298_50k/run1_baseline/chemprop_training/final_data_set/2024-08-18T03-38-20/fold_0/model_{k}/best.pt'
    mpnn = models.MPNN.load_from_file(checkpoint_path)

    # load data
    test_path = "/home/akshatz/bond_order_free/k_means/rigr_h298_50k/dataset/final_test.csv"
    smiles_column = 'resonance_smis'
    df_test = pd.read_csv(test_path)
    smis = df_test[smiles_column]
    test_data = [data.MoleculeDatapoint.from_smi(smi) for smi in smis]
    test_mol = smis.iloc[0]
    # initialize featurizer
    atom_featurizer = CustomMultiHotAtomFeaturizer.v2()
    bond_featurizer = CustomMultiHotBondFeaturizer()
    trainer = pl.Trainer(
        logger=False,
        # checkpoint_callback=False,
        callbacks=False,
        enable_progress_bar=False,
        enable_checkpointing=False,
        accelerator="cpu",
        devices=1
    )

    keep_features = [1] * 12  # 8 atom features + 4 bond features
    feature_choice = np.array([keep_features])

    save_path = Path(f'k_means/shapley_az_baseline_model_{k}')
    save_path.mkdir(exist_ok=True)
    
    for i, test_mol in tqdm(enumerate(smis)):
        base_value_path = save_path / f"{i}_base_value.npy"
        values_path = save_path / f"{i}_values.npy"
        norm_values_path = save_path / f"{i}_norm_values.npy"
        if base_value_path.exists() and values_path.exists():
            continue
        base_value, values = get_values(test_mol, trainer)
        norm_values = values / base_value
        np.save(norm_values_path, norm_values)
        np.save(base_value_path, base_value)
        np.save(values_path, values)


