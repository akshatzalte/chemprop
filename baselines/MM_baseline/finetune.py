import sys
import os

# Add MM-DTI to Python path and change working directory
sys.path.append('/home/akshatz/MM-DTI')
os.chdir('/home/akshatz/MM-DTI')

from train import MolTrain
from predict import MolPredict
from tasks import random_scaffold_split, random_split
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, roc_auc_score, precision_recall_curve
import csv
import json

def main():
    # Configuration
    data_path = '/home/akshatz/bond_order_free/k_means/rigr_h298_50k/dataset/final_data_set.csv'
    splits_path = '/home/akshatz/bond_order_free/k_means/rigr_h298_50k/dataset/splits.json'
    
    # Test sets for inference
    test_sets = {
        'final_test': '/home/akshatz/bond_order_free/k_means/rigr_h298_50k/dataset/final_test.csv',
        'final_aug_test': '/home/akshatz/bond_order_free/k_means/rigr_h298_50k/dataset/final_aug_test.csv'
    }
    
    output_dir = '/home/akshatz/bond_order_free/k_means/rigr_h298_50k/MM_baseline/output'
    
    # Model parameters
    col_name = ['H298_kcal']
    seed = 42
    batch_size = 16
    epoch = 50
    learning_rate = 1e-4
    using_scaler = True
    fds_num = 30
    use_weight = True
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load custom splits
    print(f"Loading splits from: {splits_path}")
    with open(splits_path, 'r') as f:
        splits_data = json.load(f)
    
    # Load the full dataset
    print(f"Loading dataset from: {data_path}")
    full_dataset = pd.read_csv(data_path)
    
    test_rmse = []
    test_mae = []
    test_predictions_per_fold = {test_name: [] for test_name in test_sets.keys()}
    
    print(f"Starting training with {len(splits_data)} folds...")
    
    for idx, split in enumerate(splits_data):
        print(f"\n=== Split {idx + 1}/{len(splits_data)} ===")
        
        # Extract indices for this fold
        train_indices = split['train']
        val_indices = split['val']
        test_indices = split['test']
        
        # Create datasets using your indices
        train_dataset = full_dataset.iloc[train_indices]
        valid_dataset = full_dataset.iloc[val_indices]
        test_dataset = full_dataset.iloc[test_indices]
        
        print(f"Train: {len(train_dataset)}, Val: {len(valid_dataset)}, Test: {len(test_dataset)}")
        
        # Save split data (temporary files for training)
        train_file = f'train_fold_{idx}.csv'
        val_file = f'val_fold_{idx}.csv' 
        test_file = f'test_fold_{idx}.csv'
        
        train_dataset.to_csv(train_file, index=False)
        valid_dataset.to_csv(val_file, index=False)
        test_dataset.to_csv(test_file, index=False)

        # Initialize and train model
        clf = MolTrain(
            task='regression',
            data_type='molecule',
            epochs=epoch,
            learning_rate=learning_rate,
            batch_size=batch_size,
            early_stopping=10,
            metrics='mse',
            smiles_col='resonance_smis',
            save_path=f'./exp_seed_{idx}',
            target_cols=col_name,
            use_cuda=True,
            model_name='mm_model',
            using_infonce=True,
            using_ct=True,
            raw_data=train_file,
            use_weight=use_weight,
            all_weight=False,
            fds=True,
            seed=seed,
            cache_dir_train=None,
            cache_dir_test=None,
            target_anomaly_check='filter',
            using_scaler=using_scaler,
            fds_num=fds_num,
            fds_raw_path=train_file,
            fds_col_data=col_name[0],
            chemberta_dir='weights/ChemBERTa',
            unimol_dir='weights/Uni-Mol/mol_pre_all_h_220816.pt',
        )

        print("Training...")
        clf.fit(train_file, val_file)
        
        print("Predicting on test set...")
        predictor = MolPredict(load_model=f'./exp_seed_{idx}', cache_dir=None)
        
        # Make predictions on the fold's test set
        test_pred = predictor.predict(test_file)
        
        # Calculate metrics
        true_values = test_dataset[col_name[0]].values
        rmse = np.sqrt(mean_squared_error(true_values, test_pred))
        mae = mean_absolute_error(true_values, test_pred)
        
        test_rmse.append(rmse)
        test_mae.append(mae)
        
        print(f"Fold {idx + 1} - RMSE: {rmse:.4f}, MAE: {mae:.4f}")
        
        # Save predictions for this fold
        fold_predictions = pd.DataFrame({
            'true_values': true_values,
            'predictions': test_pred.flatten(),
            'fold': idx + 1
        })
        fold_predictions.to_csv(os.path.join(output_dir, f'mmdti_fold_{idx+1}_predictions.csv'), index=False)
        
        # Predict on external test sets
        for test_name, test_path in test_sets.items():
            if os.path.exists(test_path):
                print(f"Predicting on {test_name}: {test_path}")
                test_file_pred = predictor.predict(test_path)
                
                # Load the original test file and add predictions column
                test_df = pd.read_csv(test_path)
                test_df_with_preds = test_df.copy()
                test_df_with_preds['MM_preds'] = test_file_pred.flatten()
                
                # Save with the specified naming convention
                output_filename = f'{test_name}_with_mm_preds_{idx}.csv'
                test_df_with_preds.to_csv(
                    os.path.join(output_dir, output_filename), 
                    index=False
                )
                
                # Store predictions for ensemble calculation
                test_file_predictions = pd.DataFrame({
                    'smiles': test_df['smiles'] if 'smiles' in test_df.columns else range(len(test_file_pred)),
                    'predictions': test_file_pred.flatten(),
                    'fold': idx + 1
                })
                test_predictions_per_fold[test_name].append(test_file_predictions)
            else:
                print(f"Warning: Test file not found at {test_path}")
        
        # Clean up temporary files
        for temp_file in [train_file, val_file, test_file]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    # Save cross-validation results
    results_df = pd.DataFrame({
        'fold': list(range(1, len(splits_data) + 1)),
        'rmse': test_rmse,
        'mae': test_mae
    })

    # Calculate summary statistics
    avg_rmse = np.mean(test_rmse)
    std_rmse = np.std(test_rmse)
    avg_mae = np.mean(test_mae)
    std_mae = np.std(test_mae)

    print(f"\n=== Cross-Validation Results ===")
    print(f"Average RMSE: {avg_rmse:.4f} ± {std_rmse:.4f}")
    print(f"Average MAE: {avg_mae:.4f} ± {std_mae:.4f}")

    # Add summary row
    summary_row = pd.DataFrame({
        'fold': ['average'],
        'rmse': [f"{avg_rmse:.4f} ± {std_rmse:.4f}"],
        'mae': [f"{avg_mae:.4f} ± {std_mae:.4f}"]
    })

    final_results = pd.concat([results_df, summary_row], ignore_index=True)
    final_results.to_csv(os.path.join(output_dir, 'mmdti_cv_results.csv'), index=False)

    print(f"Results saved to: {os.path.join(output_dir, 'mmdti_cv_results.csv')}")

    # Create ensemble predictions for each external test set
    for test_name, predictions_list in test_predictions_per_fold.items():
        if predictions_list and len(predictions_list) > 0:
            print(f"\n=== Creating Ensemble Predictions for {test_name} ===")
            
            # Combine all fold predictions
            ensemble_df = pd.concat(predictions_list, ignore_index=True)
            
            # Calculate ensemble (average) predictions
            ensemble_summary = ensemble_df.groupby(ensemble_df.index // len(splits_data)).agg({
                'smiles': 'first',
                'predictions': ['mean', 'std'],
                'fold': 'count'
            }).round(4)
            
            # Flatten column names
            ensemble_summary.columns = ['smiles', 'ensemble_prediction', 'prediction_std', 'n_models']
            
            # Save ensemble predictions
            ensemble_file = os.path.join(output_dir, f'mmdti_{test_name}_ensemble_predictions.csv')
            ensemble_summary.to_csv(ensemble_file, index=False)
            
            print(f"Ensemble predictions for {test_name} saved to: {ensemble_file}")
            print(f"Ensemble uses {len(splits_data)} models")

    print(f"\nTraining and prediction completed!")
    print(f"All outputs saved to: {output_dir}")

if __name__ == "__main__":
    main()
