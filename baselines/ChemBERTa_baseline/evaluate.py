from pathlib import Path
import sys
import datetime
import json
import warnings
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
import torch
from chemberta_model import ChemBERTaModel

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


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

    # Load data
    dataset_df = pd.read_csv(dataset_path)
    test_df = pd.read_csv(test_path)
    aug_test_df = pd.read_csv(aug_test_path)

    with open(splits_path, "r") as f:
        splits = json.load(f)

    # Prepare output file
    output_file = open(output_dir / "summary_chemberta.md", "w")
    
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

        # Extract train/val/test indices from the current split
        test_indices = split["test"]
        train_indices = split["train"]
        val_indices = split["val"]

        # Extract train data
        train_df = dataset_df.iloc[train_indices].copy()
        train_smiles = train_df["resonance_smis"].values
        train_targets = train_df["H298_kcal"].values

        # Extract validation data
        val_df = dataset_df.iloc[val_indices].copy()
        val_smiles = val_df["resonance_smis"].values
        val_targets = val_df["H298_kcal"].values

        # Extract test data
        test_smiles = test_df["resonance_smis"].values
        test_targets = test_df["H298_kcal"].values
        aug_test_smiles = aug_test_df["resonance_smis"].values
        aug_test_targets = aug_test_df["H298_kcal"].values

        # Calculate mean values for baseline
        mean_train_target = np.mean(train_targets)
        mean_test_target = np.mean(test_targets)
        mean_aug_test_target = np.mean(aug_test_targets)

        # Predict the mean target for the test set (baseline)
        test_mean_all_preds = np.ones(len(test_df)) * mean_train_target
        aug_test_mean_all_preds = np.ones(len(aug_test_df)) * mean_train_target

        # Calculate RMSE for mean predictions (baseline)
        test_rmse = calculate_rmse(test_targets, test_mean_all_preds)
        aug_test_rmse = calculate_rmse(aug_test_targets, aug_test_mean_all_preds)

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
            f"""# ChemBERTa Baseline Results
timestamp: {datetime.datetime.now()}

"""
        )
        
        # Random seeds for initializations
        random_seeds = [42, 117, 709, 1701, 9001]
        # For quick testing, uncomment the following line
        # random_seeds = [42]

        # Store predictions for each initialization
        test_all_preds = np.zeros((len(test_df), len(random_seeds)))
        aug_test_all_preds = np.zeros((len(aug_test_df), len(random_seeds)))

        # Dictionary to store model performance for this split
        performance_dict = {"final_test": {}, "final_aug_test": {}}

        # ChemBERTa model parameters (matching the original paper)
        model_params = {
            "task_type": "regression",
            "model_name": "DeepChem/ChemBERTa-77M-MTR",
            "max_length": 512,         # Use full max length
            "batch_size": 32,
            "num_epochs": 10,          # Original paper used 10 epochs
            "learning_rate": 1e-4      # Higher LR used for fine-tuning from scratch
        }
        
        # Train models with different initializations
        for seed_idx, random_seed in enumerate(random_seeds):
            output_file.write(f"## Random Seed {random_seed}\n")

            print(
                f"Training model with random seed {random_seed} ({seed_idx+1}/{len(random_seeds)})"
            )

            # Create and train the model with this seed
            model = ChemBERTaModel(random_seed=random_seed, **model_params)
            model.fit(train_smiles, train_targets)

            # Predict on test sets
            test_preds_current = model.predict(test_smiles)
            aug_test_preds_current = model.predict(aug_test_smiles)

            # Store predictions for this initialization
            test_all_preds[:, seed_idx] = test_preds_current
            aug_test_all_preds[:, seed_idx] = aug_test_preds_current

            # Calculate metrics
            test_rmse = calculate_rmse(test_targets, test_preds_current)
            test_mae = mean_absolute_error(test_targets, test_preds_current)
            aug_test_rmse = calculate_rmse(aug_test_targets, aug_test_preds_current)
            aug_test_mae = mean_absolute_error(aug_test_targets, aug_test_preds_current)

            performance_dict["final_test"][f"seed_{random_seed}"] = float(test_rmse)
            performance_dict["final_aug_test"][f"seed_{random_seed}"] = float(aug_test_rmse)

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

            # Free up GPU memory after each model
            torch.cuda.empty_cache() if torch.cuda.is_available() else None

        # Average predictions across initializations
        test_avg_preds = np.mean(test_all_preds, axis=1)
        aug_test_avg_preds = np.mean(aug_test_all_preds, axis=1)

        # Calculate RMSE for averaged predictions
        test_avg_rmse = calculate_rmse(test_targets, test_avg_preds)
        test_avg_mae = mean_absolute_error(test_targets, test_avg_preds)
        aug_test_avg_rmse = calculate_rmse(aug_test_targets, aug_test_avg_preds)
        aug_test_avg_mae = mean_absolute_error(aug_test_targets, aug_test_avg_preds)
        
        # Add metrics to all_splits_performance
        all_splits_performance["test_rmse"].append(test_avg_rmse)
        all_splits_performance["test_mae"].append(test_avg_mae)
        all_splits_performance["aug_test_rmse"].append(aug_test_avg_rmse)
        all_splits_performance["aug_test_mae"].append(aug_test_avg_mae)

        performance_dict["final_test"]["average"] = float(test_avg_rmse)
        performance_dict["final_aug_test"]["average"] = float(aug_test_avg_rmse)

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

        # Add the predictions to the test CSVs for this specific split
        test_df_with_preds = test_df.copy()
        aug_test_df_with_preds = aug_test_df.copy()

        test_df_with_preds["ChemBERTa_preds"] = test_avg_preds
        aug_test_df_with_preds["ChemBERTa_preds"] = aug_test_avg_preds

        # Save the CSVs with predictions for this specific split
        test_df_with_preds.to_csv(output_dir / f"final_test_with_chemberta_preds_{split_idx}.csv", index=False)
        aug_test_df_with_preds.to_csv(output_dir / f"final_aug_test_with_chemberta_preds_{split_idx}.csv", index=False)

        output_file.write(
            f"""
Output files with predictions for split {split_idx} have been saved to:
- {output_dir / f"final_test_with_chemberta_preds_{split_idx}.csv"}
- {output_dir / f"final_aug_test_with_chemberta_preds_{split_idx}.csv"}
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
    print(f"Evaluation completed. Results saved to {output_dir / 'summary_chemberta.md'}")