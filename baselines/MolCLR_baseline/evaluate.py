import os
import sys
import yaml
import json
import datetime
import warnings
import numpy as np
import pandas as pd
from pathlib import Path

import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import Dataset
from torch.utils.data.sampler import SubsetRandomSampler
from torch.optim.lr_scheduler import CosineAnnealingLR
from sklearn.metrics import mean_squared_error, mean_absolute_error

from torch_geometric.data import Data, DataLoader

# MolCLR imports
sys.path.append('/home/akshatz/MolCLR')
from models.gcn_finetune import GCN
from dataset.dataset_test import ATOM_LIST, CHIRALITY_LIST, BOND_LIST, BONDDIR_LIST

import rdkit
from rdkit import Chem
from rdkit.Chem.rdchem import HybridizationType
from rdkit.Chem.rdchem import BondType as BT
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Constants for MolCLR
ATOM_LIST = list(range(1, 119))
CHIRALITY_LIST = [
    Chem.rdchem.ChiralType.CHI_UNSPECIFIED,
    Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW,
    Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW,
    Chem.rdchem.ChiralType.CHI_OTHER
]
BOND_LIST = [BT.SINGLE, BT.DOUBLE, BT.TRIPLE, BT.AROMATIC]
BONDDIR_LIST = [
    Chem.rdchem.BondDir.NONE,
    Chem.rdchem.BondDir.ENDUPRIGHT,
    Chem.rdchem.BondDir.ENDDOWNRIGHT
]


class Normalizer(object):
    """Normalize a Tensor and restore it later."""

    def __init__(self, tensor):
        self.mean = torch.mean(tensor)
        self.std = torch.std(tensor)

    def norm(self, tensor):
        return (tensor - self.mean) / self.std

    def denorm(self, normed_tensor):
        return normed_tensor * self.std + self.mean

    def state_dict(self):
        return {'mean': self.mean, 'std': self.std}

    def load_state_dict(self, state_dict):
        self.mean = state_dict['mean']
        self.std = state_dict['std']


class MolDataset(Dataset):
    def __init__(self, df, smiles_column="resonance_smis", target_column="H298_kcal"):
        self.df = df
        self.smiles_column = smiles_column
        self.target_column = target_column
        
        self.smiles_data = df[smiles_column].values
        self.labels = df[target_column].values

    def __getitem__(self, index):
        mol = Chem.MolFromSmiles(self.smiles_data[index])
        mol = Chem.AddHs(mol)

        # Prepare node features
        type_idx = []
        chirality_idx = []
        for atom in mol.GetAtoms():
            type_idx.append(ATOM_LIST.index(atom.GetAtomicNum()))
            chirality_idx.append(CHIRALITY_LIST.index(atom.GetChiralTag()))

        x1 = torch.tensor(type_idx, dtype=torch.long).view(-1, 1)
        x2 = torch.tensor(chirality_idx, dtype=torch.long).view(-1, 1)
        x = torch.cat([x1, x2], dim=-1)

        # Prepare edge features
        row, col, edge_feat = [], [], []
        for bond in mol.GetBonds():
            start, end = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
            row += [start, end]
            col += [end, start]
            edge_feat.append([
                BOND_LIST.index(bond.GetBondType()),
                BONDDIR_LIST.index(bond.GetBondDir())
            ])
            edge_feat.append([
                BOND_LIST.index(bond.GetBondType()),
                BONDDIR_LIST.index(bond.GetBondDir())
            ])

        edge_index = torch.tensor([row, col], dtype=torch.long)
        edge_attr = torch.tensor(np.array(edge_feat), dtype=torch.long)
        
        # Target value
        y = torch.tensor(self.labels[index], dtype=torch.float).view(1, -1)
        
        data = Data(x=x, y=y, edge_index=edge_index, edge_attr=edge_attr)
        return data

    def __len__(self):
        return len(self.smiles_data)


def calculate_rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

class MolCLRFineTuner:
    def __init__(self, config, train_loader, val_loader, test_loader):
        self.config = config
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.device = self._get_device()
        self.criterion = nn.MSELoss()
        
        # Create model
        self.model = self._create_model()
        
        # Prepare training directories
        current_time = datetime.datetime.now().strftime('%b%d_%H-%M-%S')
        dir_name = current_time + '_' + config['task_name'] + '_H298_kcal'
        log_dir = os.path.join('finetune_outputs', dir_name)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_dir = log_dir
        self.writer = SummaryWriter(log_dir=log_dir)
        
        # Create normalizer for regression targets - collect all training targets first
        all_targets = []
        for data in train_loader:
            all_targets.extend(data.y.view(-1).tolist())
        targets_tensor = torch.tensor(all_targets, dtype=torch.float)
        self.normalizer = Normalizer(targets_tensor)

    def _get_device(self):
        if torch.cuda.is_available() and self.config.get('gpu', 'cpu') != 'cpu':
            device = self.config['gpu']
            torch.cuda.set_device(device)
        else:
            device = 'cpu'
        print(f"Running on: {device}")
        return device

    def _create_model(self):
        from models.gcn_finetune import GCN
        model = GCN('regression', **self.config["model"]).to(self.device)
        model = self._load_pre_trained_weights(model)
        return model

    def _load_pre_trained_weights(self, model):
        try:
            checkpoints_folder = os.path.join('/home/akshatz/MolCLR/ckpt', self.config['fine_tune_from'], 'checkpoints')
            state_dict = torch.load(os.path.join(checkpoints_folder, 'model.pth'), map_location=self.device)
            model.load_my_state_dict(state_dict)
            print("Loaded pre-trained model with success.")
        except FileNotFoundError:
            print("Pre-trained weights not found. Training from scratch.")
        return model

    def _step(self, model, data):
        data = data.to(self.device)
        _, pred = model(data)
        
        # In PyTorch Geometric, data.y is now a tensor on the device
        target = self.normalizer.norm(data.y)
        loss = self.criterion(pred, target)
        
        return loss, pred

    def train(self, random_seed):
        print(f"Training model with random seed {random_seed}")
        
        # Set seed for reproducibility
        torch.manual_seed(random_seed)
        np.random.seed(random_seed)
        
        # Create new model instance for this seed
        model = self._create_model()
        
        # Setup optimizer with separate learning rates for the backbone and prediction head
        layer_list = []
        for name, param in model.named_parameters():
            if 'pred_head' in name:
                print(name, param.requires_grad)
                layer_list.append(name)

        params = list(map(lambda x: x[1], list(filter(lambda kv: kv[0] in layer_list, model.named_parameters()))))
        base_params = list(map(lambda x: x[1], list(filter(lambda kv: kv[0] not in layer_list, model.named_parameters()))))

        optimizer = torch.optim.Adam(
            [{'params': base_params, 'lr': self.config['init_base_lr']}, 
             {'params': params, 'lr': self.config['init_lr']}],
            weight_decay=float(self.config['weight_decay'])
        )
        
        # Training loop
        n_iter = 0
        valid_n_iter = 0
        best_valid_loss = float('inf')
        best_valid_rmse = float('inf')
        
        for epoch in range(self.config['epochs']):
            model.train()
            
            train_loss = 0
            for bn, data in enumerate(self.train_loader):
                optimizer.zero_grad()
                
                loss, _ = self._step(model, data)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                
                if n_iter % self.config['log_every_n_steps'] == 0:
                    self.writer.add_scalar(f'train_loss_{random_seed}', loss.item(), global_step=n_iter)
                
                n_iter += 1
            
            # Validate model
            if epoch % self.config['eval_every_n_epochs'] == 0:
                valid_loss, valid_rmse = self._validate(model, self.val_loader)
                self.writer.add_scalar(f'valid_loss_{random_seed}', valid_loss, global_step=valid_n_iter)
                self.writer.add_scalar(f'valid_rmse_{random_seed}', valid_rmse, global_step=valid_n_iter)
                
                if valid_rmse < best_valid_rmse:
                    best_valid_rmse = valid_rmse
                    model_path = os.path.join(self.log_dir, f'model_{random_seed}.pth')
                    torch.save(model.state_dict(), model_path)
                    print(f"Epoch {epoch}: New best validation RMSE: {valid_rmse:.4f}")
                
                valid_n_iter += 1
        
        # Load best model for this seed
        best_model_path = os.path.join(self.log_dir, f'model_{random_seed}.pth')
        model.load_state_dict(torch.load(best_model_path))
        
        return model

    def _validate(self, model, loader):
        model.eval()
        predictions = []
        labels = []
        
        valid_loss = 0.0
        num_data = 0
        
        with torch.no_grad():
            for data in loader:
                data = data.to(self.device)
                loss, pred = self._step(model, data)
                
                valid_loss += loss.item() * data.y.size(0)
                num_data += data.y.size(0)
                
                # Denormalize predictions
                pred = self.normalizer.denorm(pred)
                
                # Extract predictions and labels properly from batched data
                if self.device == 'cpu':
                    predictions.extend(pred.detach().numpy().reshape(-1))
                    labels.extend(data.y.detach().numpy().reshape(-1))
                else:
                    predictions.extend(pred.cpu().detach().numpy().reshape(-1))
                    labels.extend(data.y.cpu().detach().numpy().reshape(-1))
        
        valid_loss /= num_data
        
        # Calculate RMSE
        predictions = np.array(predictions)
        labels = np.array(labels)
        rmse = calculate_rmse(labels, predictions)
        
        model.train()
        return valid_loss, rmse

    def evaluate(self, model, loader):
        model.eval()
        predictions = []
        labels = []
        
        with torch.no_grad():
            for data in loader:
                data = data.to(self.device)
                _, pred = self._step(model, data)
                
                # Denormalize predictions
                pred = self.normalizer.denorm(pred)
                
                # Extract predictions and labels properly from batched data
                if self.device == 'cpu':
                    predictions.extend(pred.detach().numpy().reshape(-1))
                    labels.extend(data.y.detach().numpy().reshape(-1))
                else:
                    predictions.extend(pred.cpu().detach().numpy().reshape(-1))
                    labels.extend(data.y.cpu().detach().numpy().reshape(-1))
        
        # Calculate metrics
        predictions = np.array(predictions)
        labels = np.array(labels)
        rmse = calculate_rmse(labels, predictions)
        mae = mean_absolute_error(labels, predictions)
        
        return predictions, labels, rmse, mae


if __name__ == "__main__":
    try:
        output_dir = Path(sys.argv[1])
    except:
        print("usage: python evaluate.py OUTPUT_DIR")
        exit(1)

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Define dataset paths
    dataset_path = Path(
        "/home/akshatz/bond_order_free/k_means/rigr_h298_50k/dataset/final_data_set.csv"
    )
    test_path = Path(
        "/home/akshatz/bond_order_free/k_means/rigr_h298_50k/dataset/final_test.csv"
    )
    aug_test_path = Path(
        "/home/akshatz/bond_order_free/k_means/rigr_h298_50k/dataset/final_aug_test.csv"
    )
    splits_path = Path(
        "/home/akshatz/bond_order_free/k_means/rigr_h298_50k/dataset/splits.json"
    )

    # Load data
    dataset_df = pd.read_csv(dataset_path)
    test_df = pd.read_csv(test_path)
    aug_test_df = pd.read_csv(aug_test_path)

    # Load splits
    with open(splits_path, "r") as f:
        splits = json.load(f)

    # Prepare output file
    output_file = open(output_dir / "summary_molclr.md", "w")
    
    # Dictionary to store all performance metrics across splits
    all_splits_performance = {
        "test_rmse": [],
        "test_mae": [],
        "aug_test_rmse": [],
        "aug_test_mae": []
    }

    for split_idx in range(len(splits)):
        output_file.write(
            f"# Split {split_idx + 1} of {len(splits)}\n"
        )
        print(f"Processing split {split_idx + 1} of {len(splits)}")
        
        # Extract data from the splits
        split = splits[split_idx]
        test_indices = split["test"]
        train_indices = split["train"]
        val_indices = split["val"]

        # Create train, val, test datasets
        full_dataset = MolDataset(dataset_df)
        
        # Create data samplers
        train_sampler = SubsetRandomSampler(train_indices)
        val_sampler = SubsetRandomSampler(val_indices)
        
        # Create data loaders using PyTorch Geometric's DataLoader
        train_loader = DataLoader(
            full_dataset, batch_size=32, sampler=train_sampler,
            num_workers=4, drop_last=False
        )
        val_loader = DataLoader(
            full_dataset, batch_size=32, sampler=val_sampler,
            num_workers=4, drop_last=False
        )
        
        # Create test datasets
        test_dataset = MolDataset(test_df)
        aug_test_dataset = MolDataset(aug_test_df)
        
        # Create test loaders
        test_loader = DataLoader(
            test_dataset, batch_size=32, shuffle=False,
            num_workers=4, drop_last=False
        )
        aug_test_loader = DataLoader(
            aug_test_dataset, batch_size=32, shuffle=False,
            num_workers=4, drop_last=False
        )

        # Mean baseline calculations
        mean_train_target = np.mean(dataset_df.iloc[train_indices]["H298_kcal"].values)
        mean_test_target = np.mean(test_df["H298_kcal"])
        mean_aug_test_target = np.mean(aug_test_df["H298_kcal"])

        # Predict the mean target for the test set
        test_mean_all_preds = np.ones(len(test_df)) * mean_train_target
        aug_test_mean_all_preds = np.ones(len(aug_test_df)) * mean_train_target

        # Calculate RMSE for mean predictions
        test_rmse = calculate_rmse(test_df["H298_kcal"], test_mean_all_preds)
        aug_test_rmse = calculate_rmse(aug_test_df["H298_kcal"], aug_test_mean_all_preds)

        output_file.write(
            f"""# Predicting the mean baseline
    timestamp: {datetime.datetime.now()}
    ## Mean Predictions
    Mean Training Target: {mean_train_target:.4f} kcal/mol
    Mean Test Target: {mean_test_target:.4f} kcal/mol
    Mean Augmented Test Target: {mean_aug_test_target:.4f} kcal/mol

    ## RMSE for Mean Predictions:
    ### final_test.csv
    RMSE: {test_rmse:.4f} kcal/mol

    ### final_aug_test.csv
    RMSE: {aug_test_rmse:.4f} kcal/mol

    """
        )

        output_file.write(
            f"""# MolCLR Finetuning Results
    timestamp: {datetime.datetime.now()}

    """
        )

        # Configure MolCLR model
        config = {
            'batch_size': 32,
            'epochs': 50,
            'eval_every_n_epochs': 1,
            'fine_tune_from': 'pretrained_gcn',
            'log_every_n_steps': 50,
            'init_lr': 0.0005,
            'init_base_lr': 0.0001,
            'weight_decay': '1e-6',
            'gpu': 'cuda:1' if torch.cuda.is_available() else 'cpu',
            'task_name': 'H298_prediction',
            'model_type': 'gcn',
            'model': {
                'num_layer': 5,
                'emb_dim': 300,
                'feat_dim': 512,
                'drop_ratio': 0.3,
                'pool': 'mean'
            },
            'dataset': {
                'task': 'regression',
                'target': 'H298_kcal'
            }
        }

        # Initialize MolCLR finetuner
        finetuner = MolCLRFineTuner(config, train_loader, val_loader, test_loader)
        
        # Random seeds for initializations
        random_seeds = [42, 117, 709, 1701, 9001]
        # random_seeds = [42]
        
        # Dictionary to store model performance
        performance_dict = {"final_test": {}, "final_aug_test": {}}
        
        # Store predictions for each initialization
        test_all_preds = np.zeros((len(test_df), len(random_seeds)))
        aug_test_all_preds = np.zeros((len(aug_test_df), len(random_seeds)))
        
        # Train models with different initializations
        for seed_idx, random_seed in enumerate(random_seeds):
            output_file.write(f"## Random Seed {random_seed}\n")
            print(f"Training model with random seed {random_seed} ({seed_idx+1}/{len(random_seeds)})")
            
            # Train model with current random seed
            model = finetuner.train(random_seed)
            
            # Evaluate on test sets
            test_preds, test_labels, test_rmse, test_mae = finetuner.evaluate(model, test_loader)
            aug_test_preds, aug_test_labels, aug_test_rmse, aug_test_mae = finetuner.evaluate(model, aug_test_loader)
            
            # Store predictions
            test_all_preds[:, seed_idx] = test_preds
            aug_test_all_preds[:, seed_idx] = aug_test_preds
            
            # Store performance metrics
            performance_dict["final_test"][f"seed_{random_seed}"] = float(test_rmse)
            performance_dict["final_aug_test"][f"seed_{random_seed}"] = float(aug_test_rmse)
            
            # Write results to output file
            output_file.write(
                f"""
    ### final_test.csv
    RMSE: {test_rmse:.4f} kcal/mol
    MAE: {test_mae:.4f} kcal/mol

    ### final_aug_test.csv
    RMSE: {aug_test_rmse:.4f} kcal/mol
    MAE: {aug_test_mae:.4f} kcal/mol

    """
            )
        
        # Average predictions across initializations
        test_avg_preds = np.mean(test_all_preds, axis=1)
        aug_test_avg_preds = np.mean(aug_test_all_preds, axis=1)
        
        # Calculate RMSE for averaged predictions
        test_avg_rmse = calculate_rmse(test_df["H298_kcal"], test_avg_preds)
        aug_test_avg_rmse = calculate_rmse(aug_test_df["H298_kcal"], aug_test_avg_preds)
        
        # Calculate MAE for averaged predictions
        test_avg_mae = mean_absolute_error(test_df["H298_kcal"], test_avg_preds)
        aug_test_avg_mae = mean_absolute_error(aug_test_df["H298_kcal"], aug_test_avg_preds)
        
        # Add metrics to all_splits_performance
        all_splits_performance["test_rmse"].append(test_avg_rmse)
        all_splits_performance["test_mae"].append(test_avg_mae)
        all_splits_performance["aug_test_rmse"].append(aug_test_avg_rmse)
        all_splits_performance["aug_test_mae"].append(aug_test_avg_mae)
        
        performance_dict["final_test"]["average"] = test_avg_rmse
        performance_dict["final_aug_test"]["average"] = aug_test_avg_rmse
        
        # Write summary results
        output_file.write(
            f"""
    ## Summary for Split {split_idx + 1}

    ### Averaged Predictions RMSE
    - final_test.csv: {test_avg_rmse:.4f} kcal/mol (MAE: {test_avg_mae:.4f} kcal/mol)
    - final_aug_test.csv: {aug_test_avg_rmse:.4f} kcal/mol (MAE: {aug_test_avg_mae:.4f} kcal/mol)

    ### Performance Dictionary
    ```
    results_dict = {json.dumps(performance_dict, indent=4)}
    ```

    """
        )
        
        # Add the predictions to the test CSVs
        test_df_with_preds = test_df.copy()
        aug_test_df_with_preds = aug_test_df.copy()
        
        test_df_with_preds["MolCLR_preds"] = test_avg_preds
        aug_test_df_with_preds["MolCLR_preds"] = aug_test_avg_preds
        
        # Save the CSVs with predictions for this specific split
        test_df_with_preds.to_csv(output_dir / f"final_test_with_molclr_preds_{split_idx}.csv", index=False)
        aug_test_df_with_preds.to_csv(output_dir / f"final_aug_test_with_molclr_preds_{split_idx}.csv", index=False)
        
        output_file.write(
            f"""
    Output files with predictions for split {split_idx} have been saved to:
    - {output_dir / f"final_test_with_molclr_preds_{split_idx}.csv"}
    - {output_dir / f"final_aug_test_with_molclr_preds_{split_idx}.csv"}
    """
        )
    
    # Calculate mean and standard deviation of RMSE across all splits
    mean_test_rmse = np.mean(all_splits_performance["test_rmse"])
    std_test_rmse = np.std(all_splits_performance["test_rmse"])
    mean_test_mae = np.mean(all_splits_performance["test_mae"])
    std_test_mae = np.std(all_splits_performance["test_mae"])
    
    mean_aug_test_rmse = np.mean(all_splits_performance["aug_test_rmse"])
    std_aug_test_rmse = np.std(all_splits_performance["aug_test_rmse"])
    mean_aug_test_mae = np.mean(all_splits_performance["aug_test_mae"])
    std_aug_test_mae = np.std(all_splits_performance["aug_test_mae"])
    
    # Write final summary section with statistics across all splits
    output_file.write(
        f"""
# Overall Summary Across All Splits

## Final Test Set Performance
- RMSE: {mean_test_rmse:.4f} ± {std_test_rmse:.4f} kcal/mol
- MAE: {mean_test_mae:.4f} ± {std_test_mae:.4f} kcal/mol

## Augmented Test Set Performance
- RMSE: {mean_aug_test_rmse:.4f} ± {std_aug_test_rmse:.4f} kcal/mol
- MAE: {mean_aug_test_mae:.4f} ± {std_aug_test_mae:.4f} kcal/mol

## Performance Details By Split
"""
    )
    
    # Add a table with per-split performance
    output_file.write(
        f"""
| Split | Test RMSE | Test MAE | Aug Test RMSE | Aug Test MAE |
|-------|-----------|----------|--------------|-------------|
"""
    )
    for i in range(len(splits)):
        output_file.write(
            f"| {i+1} | {all_splits_performance['test_rmse'][i]:.4f} | {all_splits_performance['test_mae'][i]:.4f} | {all_splits_performance['aug_test_rmse'][i]:.4f} | {all_splits_performance['aug_test_mae'][i]:.4f} |\n"
        )
    
    output_file.close()
    print(f"Evaluation completed. Results saved to {output_dir / 'summary_molclr.md'}")