"""
fit a descriptor-based MLP (fastprop) to H298 dataset
"""
from pathlib import Path
import sys
import datetime
import warnings
import json
import numpy as np
import pandas as pd
import torch
from mordred import Calculator, descriptors
from rdkit.Chem import MolFromSmiles
from lightning import Trainer, LightningModule, seed_everything
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping
from lightning.pytorch.loggers import TensorBoardLogger
from fastprop.data import standard_scale, inverse_standard_scale
from torch import distributed
from sklearn.metrics import mean_squared_error, mean_absolute_error


warnings.filterwarnings("ignore", category=FutureWarning)


class FeatureNormalizer(torch.nn.Module):
    """Module that normalizes input features using precomputed statistics."""
    def __init__(self, feature_means, feature_vars):
        super().__init__()
        self.register_buffer("feature_means", feature_means)
        self.register_buffer("feature_vars", feature_vars)

    def normalize(self, x):
        return standard_scale(x, self.feature_means, self.feature_vars).clamp(min=-6, max=6)


class FastPropModel(LightningModule):
    """FastProp model implementation for regression tasks."""
    def __init__(
        self,
        normalizer: torch.nn.Module,
        input_dim: int,
        hidden_sizes=(1024,),
        learning_rate=0.001,  # Changed to default FastProp learning rate
    ):
        super().__init__()
        self.normalizer = normalizer
        self.learning_rate = learning_rate
        
        # Build network layers
        modules = []
        for i in range(len(hidden_sizes)):
            modules.append(
                torch.nn.Linear(
                    input_dim if i == 0 else hidden_sizes[i-1], hidden_sizes[i]
                )
            )
            modules.append(torch.nn.ReLU())
        modules.append(torch.nn.Linear(hidden_sizes[-1], 1))
        self.network = torch.nn.Sequential(*modules)
        self.save_hyperparameters()

    def configure_optimizers(self):
        return {"optimizer": torch.optim.Adam(self.parameters(), lr=self.learning_rate)}

    def log(self, name, value, **kwargs):
        """Wrap the parent PyTorch Lightning log function to automatically detect DDP."""
        return super().log(
            name, value, sync_dist=distributed.is_initialized(), **kwargs
        )

    def forward(self, descriptors):
        return self.network(self.normalizer.normalize(descriptors))

    def _step(self, batch, name):
        descriptors, y = batch
        y_hat = self(descriptors)
        loss = torch.nn.functional.mse_loss(y_hat, y, reduction="mean")
        self.log(f"{name}/loss", loss)
        return loss

    def training_step(self, batch, batch_idx):
        return self._step(batch, "train")

    def validation_step(self, batch, batch_idx):
        return self._step(batch, "validation")

    def test_step(self, batch, batch_idx):
        return self._step(batch, "test")

    def predict_step(self, batch, batch_idx):
        return self(batch[0])


def calculate_rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))


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

    output_file = open(output_dir / "fastprop_results.md", "w")
    output_file.write(
        f"""# FastProp Results for H298 Dataset
timestamp: {datetime.datetime.now()}
"""
    )
    
    # Load data
    dataset_df = pd.read_csv(dataset_path)
    test_df = pd.read_csv(test_path)
    aug_test_df = pd.read_csv(aug_test_path)

    # Load splits from JSON file
    with open(splits_path, "r") as f:
        splits = json.load(f)
    
    # Dictionary to store all performance metrics across splits
    all_splits_performance = {
        "test_rmse": [],
        "test_mae": [],
        "aug_test_rmse": [],
        "aug_test_mae": []
    }
    
    # Process each split
    for split_idx, split in enumerate(splits):
        output_file.write(
            f"# Split {split_idx + 1} of {len(splits)}\n"
        )
        print(f"Processing split {split_idx + 1} of {len(splits)}")
        
        # Initialize performance dictionary for this split
        performance_dict = {"final_test": {}, "final_aug_test": {}}
        
        test_indices = split["test"]
        val_indices = split["val"]
        train_indices = split["train"]
        
        print(f"Dataset split: {len(train_indices)} train, {len(val_indices)} validation, {len(test_indices)} test samples")
        
        # Extract data based on splits
        train_df = dataset_df.iloc[train_indices].copy()
        val_df = dataset_df.iloc[val_indices].copy()
        
        print("Preparing molecular descriptors...")
        
        # Calculate molecular descriptors
        calc = Calculator(descriptors, ignore_3D=True)
        calc.config(timeout=1)
        
        # Calculate descriptors for training data
        train_smiles = train_df["resonance_smis"]
        train_targets = train_df["H298_kcal"].values
        train_targets = torch.tensor(train_targets, dtype=torch.float32).reshape(-1, 1)
        
        print("Calculating training set descriptors...")
        train_mols = list(map(MolFromSmiles, train_smiles))
        for mol in train_mols:
            if mol is not None:
                mol.SetProp("_Name", "")
        train_desc = calc.pandas(train_mols).fill_missing().to_numpy(dtype=np.float32)
        train_desc = torch.tensor(train_desc, dtype=torch.float32)
        
        # Calculate descriptors for validation data
        print("Calculating validation set descriptors...")
        val_smiles = val_df["resonance_smis"]
        val_targets = val_df["H298_kcal"].values
        val_targets = torch.tensor(val_targets, dtype=torch.float32).reshape(-1, 1)
        
        val_mols = list(map(MolFromSmiles, val_smiles))
        for mol in val_mols:
            if mol is not None:
                mol.SetProp("_Name", "")
        val_desc = calc.pandas(val_mols).fill_missing().to_numpy(dtype=np.float32)
        val_desc = torch.tensor(val_desc, dtype=torch.float32)
        
        # Calculate descriptors for test sets
        print("Calculating test set descriptors...")
        test_smiles = test_df["resonance_smis"]
        test_mols = list(map(MolFromSmiles, test_smiles))
        for mol in test_mols:
            if mol is not None:
                mol.SetProp("_Name", "")
        test_desc = calc.pandas(test_mols).fill_missing().to_numpy(dtype=np.float32)
        test_desc = torch.tensor(test_desc, dtype=torch.float32)
        
        # Calculate aug_test descriptors
        print("Calculating augmented test set descriptors...")
        aug_test_smiles = aug_test_df["resonance_smis"]
        aug_test_mols = list(map(MolFromSmiles, aug_test_smiles))
        for mol in aug_test_mols:
            if mol is not None:
                mol.SetProp("_Name", "")
        aug_test_desc = calc.pandas(aug_test_mols).fill_missing().to_numpy(dtype=np.float32)
        aug_test_desc = torch.tensor(aug_test_desc, dtype=torch.float32)
        
        # Normalize features and targets (only using training data for normalization statistics)
        print("Computing normalization statistics from training data...")
        _, feature_means, feature_vars = standard_scale(train_desc)
        
        # Scale all datasets using the same statistics
        train_desc_scaled = standard_scale(train_desc, feature_means, feature_vars)
        val_desc_scaled = standard_scale(val_desc, feature_means, feature_vars)
        test_desc_scaled = standard_scale(test_desc, feature_means, feature_vars)
        aug_test_desc_scaled = standard_scale(aug_test_desc, feature_means, feature_vars)
        
        # Normalize targets
        _, target_means, target_vars = standard_scale(train_targets)
        train_targets_scaled = standard_scale(train_targets, target_means, target_vars)
        val_targets_scaled = standard_scale(val_targets, target_means, target_vars)
        
        # Create datasets
        train_dataset = torch.utils.data.TensorDataset(train_desc_scaled, train_targets_scaled)
        validation_dataset = torch.utils.data.TensorDataset(val_desc_scaled, val_targets_scaled)
        test_dataset = torch.utils.data.TensorDataset(test_desc_scaled)
        aug_test_dataset = torch.utils.data.TensorDataset(aug_test_desc_scaled)
        
        # Create dataloaders (these remain constant across all random seeds)
        print("Creating data loaders...")
        train_dataloader = torch.utils.data.DataLoader(
            train_dataset,
            num_workers=1,
            persistent_workers=True,
            batch_size=64,
            shuffle=True,
        )
        val_dataloader = torch.utils.data.DataLoader(
            validation_dataset,
            num_workers=1,
            batch_size=64,
            persistent_workers=True,
        )
        test_dataloader = torch.utils.data.DataLoader(
            test_dataset, 
            num_workers=1, 
            batch_size=64, 
            persistent_workers=True
        )
        aug_test_dataloader = torch.utils.data.DataLoader(
            aug_test_dataset, 
            num_workers=1, 
            batch_size=64, 
            persistent_workers=True
        )
        
        # Set up for multiple random initializations
        random_seeds = [42, 117, 709, 1701, 9001]
        print(f"Training with {len(random_seeds)} different random initializations...")
        
        # Store predictions for each initialization
        test_all_preds = np.zeros((len(test_df), len(random_seeds)))
        aug_test_all_preds = np.zeros((len(aug_test_df), len(random_seeds)))
        
        # Create the normalizer once (shared architecture)
        normalizer = FeatureNormalizer(feature_means, feature_vars)
        input_size = feature_means.shape[0]
        hidden_size = (1_800, 1_800)  # standard fastprop architecture
        
        for seed_idx, random_seed in enumerate(random_seeds):
            print(f"Training model with random seed {random_seed} for initialization ({seed_idx+1}/{len(random_seeds)})")
            output_file.write(f"## Random Seed {random_seed}\n")
            
            # Set seed for reproducibility of weight initialization
            seed_everything(random_seed)
            
            # Create model with the current random seed
            model = FastPropModel(
                normalizer, input_size, hidden_size, learning_rate=0.001  # Default FastProp learning rate
            )
                
            # Setup training
            _subdir = f"split_{split_idx}_seed_{random_seed}"
            tensorboard_logger = TensorBoardLogger(
                output_dir / _subdir,
                name="tensorboard_logs",
                default_hp_metric=False,
            )
            callbacks = [
                EarlyStopping(
                    monitor="validation/loss",
                    mode="min",
                    verbose=False,
                    patience=20,
                ),
                ModelCheckpoint(
                    monitor="validation/loss",
                    save_top_k=2,
                    mode="min",
                    dirpath=output_dir / _subdir / "checkpoints",
                ),
            ]
                
            # Train model
            print(f"Training model (seed {random_seed})...")
            trainer = Trainer(
                max_epochs=100,
                logger=tensorboard_logger,
                log_every_n_steps=1,
                enable_checkpointing=True,
                check_val_every_n_epoch=1,
                callbacks=callbacks,
            )
            trainer.fit(model, train_dataloader, val_dataloader)
                
            # Load best model for evaluation
            ckpt_path = trainer.checkpoint_callback.best_model_path
            print(f"Reloading best model from checkpoint file: {ckpt_path}")
            model = model.__class__.load_from_checkpoint(ckpt_path, map_location="cpu")
                
            # Generate predictions
            print(f"Generating predictions (seed {random_seed})...")
            trainer = Trainer(logger=tensorboard_logger)
            test_predictions = torch.vstack(trainer.predict(model, test_dataloader))
            aug_test_predictions = torch.vstack(trainer.predict(model, aug_test_dataloader))
                
            # Denormalize predictions
            test_predictions = inverse_standard_scale(test_predictions, target_means, target_vars)
            aug_test_predictions = inverse_standard_scale(aug_test_predictions, target_means, target_vars)
            
            # Convert to numpy arrays for evaluation
            test_preds_current = test_predictions.numpy(force=True).flatten()
            aug_test_preds_current = aug_test_predictions.numpy(force=True).flatten()
            
            # Store predictions for this initialization
            test_all_preds[:, seed_idx] = test_preds_current
            aug_test_all_preds[:, seed_idx] = aug_test_preds_current
            
            # Calculate RMSE
            test_rmse = calculate_rmse(test_df["H298_kcal"], test_preds_current)
            aug_test_rmse = calculate_rmse(aug_test_df["H298_kcal"], aug_test_preds_current)
            
            # Calculate MAE
            test_mae = mean_absolute_error(test_df["H298_kcal"], test_preds_current)
            aug_test_mae = mean_absolute_error(aug_test_df["H298_kcal"], aug_test_preds_current)
            
            performance_dict["final_test"][f"seed_{random_seed}"] = test_rmse
            performance_dict["final_aug_test"][f"seed_{random_seed}"] = aug_test_rmse

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
            
            # Optionally free memory after each seed
            del model
            torch.cuda.empty_cache() if torch.cuda.is_available() else None

        # Average predictions across initializations
        print("Computing ensemble predictions by averaging across all seeds...")
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

        # Write summary results for this split
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

        # Add the predictions to the test CSVs for this split
        test_df_with_preds = test_df.copy()
        aug_test_df_with_preds = aug_test_df.copy()

        test_df_with_preds["FastProp_preds"] = test_avg_preds
        aug_test_df_with_preds["FastProp_preds"] = aug_test_avg_preds

        # Save the CSVs with predictions for this specific split
        test_df_with_preds.to_csv(output_dir / f"final_test_with_fastprop_preds_{split_idx}.csv", index=False)
        aug_test_df_with_preds.to_csv(output_dir / f"final_aug_test_with_fastprop_preds_{split_idx}.csv", index=False)

        output_file.write(
            f"""
Output files with predictions for split {split_idx + 1} have been saved to:
- {output_dir / f"final_test_with_fastprop_preds_{split_idx}.csv"}
- {output_dir / f"final_aug_test_with_fastprop_preds_{split_idx}.csv"}
"""
        )
    
    # Calculate mean and standard deviation of metrics across all splits
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
    print(f"Evaluation completed. Results saved to {output_dir / 'fastprop_results.md'}")
