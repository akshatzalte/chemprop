from pathlib import Path
import sys
import datetime
import json
import warnings
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import TransformedTargetRegressor
from sklearn.metrics import mean_squared_error
from scikit_mol.conversions import SmilesToMolTransformer
from scikit_mol.fingerprints import MorganFingerprintTransformer

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


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
    output_file = open(output_dir / "summary_morgan.md", "w")

    # Extract test indices from the splits
    split = splits[0]
    test_indices = split["test"]
    train_indices = [i for i in range(50000) if i not in test_indices]
    train_indices = [i for i in train_indices]

    # Extract train data
    train_df = dataset_df.iloc[train_indices].copy()
    train_smiles = train_df["resonance_smis"]
    train_targets = train_df["H298_kcal"].values

    mean_train_target = np.mean(train_targets)
    mean_test_target = np.mean(test_df["H298_kcal"])
    mean_aug_test_target = np.mean(aug_test_df["H298_kcal"])

    # Predict the mean target for the test set
    test_mean_all_preds = np.ones(len(test_df)) * mean_train_target
    aug_test_mean_all_preds = np.ones(len(aug_test_df)) * mean_train_target

    # Calculate RMSE for mean predictions
    test_rmse = calculate_rmse(test_df["H298_kcal"], test_mean_all_preds)
    aug_test_rmse = calculate_rmse(aug_test_df["H298_kcal"], aug_test_mean_all_preds)

    output_file.write(
        f"""# Predicing the mean baseline
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
        f"""# Random Forest Baseline Results
timestamp: {datetime.datetime.now()}

"""
    )
    # Random seeds for initializations
    random_seeds = [42, 117, 709, 1701, 9001]
    # random_seeds = [42]

    # Store predictions for each initialization
    test_all_preds = np.zeros((len(test_df), len(random_seeds)))
    aug_test_all_preds = np.zeros((len(aug_test_df), len(random_seeds)))

    # Dictionary to store model performance
    performance_dict = {"final_test": {}, "final_aug_test": {}}

    # Train models with different initializations
    for seed_idx, random_seed in enumerate(random_seeds):
        output_file.write(f"## Random Seed {random_seed}\n")

        print(
            f"Training model with random seed {random_seed} ({seed_idx+1}/{len(random_seeds)})"
        )

        # Create and train the model
        model = TransformedTargetRegressor(
            regressor=RandomForestRegressor(
                random_state=random_seed, n_estimators=100, n_jobs=-1
            ),
            transformer=StandardScaler(),
        )

        pipe = Pipeline(
            [
                ("smiles2mol", SmilesToMolTransformer()),
                ("mol2fp", MorganFingerprintTransformer(radius=4)),
                ("model", model),
            ]
        )

        pipe.fit(train_smiles, train_targets)

        # Predict on test sets
        test_smiles = test_df["resonance_smis"]
        aug_test_smiles = aug_test_df["resonance_smis"]

        test_preds_current = pipe.predict(test_smiles).flatten()
        aug_test_preds_current = pipe.predict(aug_test_smiles).flatten()

        # Store predictions for this initialization
        test_all_preds[:, seed_idx] = test_preds_current
        aug_test_all_preds[:, seed_idx] = aug_test_preds_current

        # Calculate RMSE for individual seed
        test_rmse = calculate_rmse(test_df["H298_kcal"], test_preds_current)
        aug_test_rmse = calculate_rmse(aug_test_df["H298_kcal"], aug_test_preds_current)

        performance_dict["final_test"][f"seed_{random_seed}"] = test_rmse
        performance_dict["final_aug_test"][f"seed_{random_seed}"] = aug_test_rmse

        output_file.write(
            f"""
### final_test.csv
RMSE: {test_rmse:.4f} kcal/mol

### final_aug_test.csv
RMSE: {aug_test_rmse:.4f} kcal/mol

"""
        )

    # Average predictions across initializations
    test_avg_preds = np.mean(test_all_preds, axis=1)
    aug_test_avg_preds = np.mean(aug_test_all_preds, axis=1)

    # Calculate RMSE for averaged predictions
    test_avg_rmse = calculate_rmse(test_df["H298_kcal"], test_avg_preds)
    aug_test_avg_rmse = calculate_rmse(aug_test_df["H298_kcal"], aug_test_avg_preds)

    performance_dict["final_test"]["average"] = test_avg_rmse
    performance_dict["final_aug_test"]["average"] = aug_test_avg_rmse

    # Write summary results
    output_file.write(
        f"""
## Summary

### Averaged Predictions RMSE
- final_test.csv: {test_avg_rmse:.4f} kcal/mol
- final_aug_test.csv: {aug_test_avg_rmse:.4f} kcal/mol

### Performance Dictionary
```
results_dict = {json.dumps(performance_dict, indent=4)}
```

"""
    )

    # Add the predictions to the test CSVs
    test_df["RF_preds"] = test_avg_preds
    aug_test_df["RF_preds"] = aug_test_avg_preds

    # Save the CSVs with predictions
    test_df.to_csv(output_dir / "final_test_with_morgan_preds.csv", index=False)
    aug_test_df.to_csv(output_dir / "final_aug_test_with_morgan_preds.csv", index=False)

    output_file.write(
        f"""
Output files with predictions have been saved to:
- {output_dir / "final_test_with_preds.csv"}
- {output_dir / "final_aug_test_with_preds.csv"}
"""
    )

    output_file.close()
    print(f"Evaluation completed. Results saved to {output_dir / 'summary_morgan.md'}")
