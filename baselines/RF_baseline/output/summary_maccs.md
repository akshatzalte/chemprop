# Predicing the mean baseline
timestamp: 2025-05-09 23:00:54.592088
## Mean Predictions
Mean Training Target: 8.0887 kcal/mol
Mean Test Target: -6.4638 kcal/mol
Mean Augmented Test Target: -8.0790 kcal/mol

## RMSE for Mean Predictions:
### final_test.csv

RMSE: 63.8200 kcal/mol

### final_aug_test.csv
RMSE: 63.6323 kcal/mol

# Random Forest Baseline Results
timestamp: 2025-05-09 23:00:54.592103

## Random Seed 42

### final_test.csv
RMSE: 23.2443 kcal/mol

### final_aug_test.csv
RMSE: 24.3969 kcal/mol

## Random Seed 117

### final_test.csv
RMSE: 22.9395 kcal/mol

### final_aug_test.csv
RMSE: 24.1013 kcal/mol

## Random Seed 709

### final_test.csv
RMSE: 23.2206 kcal/mol

### final_aug_test.csv
RMSE: 24.3593 kcal/mol

## Random Seed 1701

### final_test.csv
RMSE: 23.2277 kcal/mol

### final_aug_test.csv
RMSE: 24.4484 kcal/mol

## Random Seed 9001

### final_test.csv
RMSE: 23.2427 kcal/mol

### final_aug_test.csv
RMSE: 24.4027 kcal/mol


## Summary

### Averaged Predictions RMSE
- final_test.csv: 23.0745 kcal/mol
- final_aug_test.csv: 24.2401 kcal/mol

### Performance Dictionary
```
results_dict = {
    "final_test": {
        "seed_42": 23.244312515038065,
        "seed_117": 22.93949946960335,
        "seed_709": 23.22060930356481,
        "seed_1701": 23.227690381445615,
        "seed_9001": 23.2427348515657,
        "average": 23.07447482030121
    },
    "final_aug_test": {
        "seed_42": 24.39693035036447,
        "seed_117": 24.10133067467906,
        "seed_709": 24.35932349593367,
        "seed_1701": 24.44839097486207,
        "seed_9001": 24.40269365560303,
        "average": 24.240123257209465
    }
}
```


Output files with predictions have been saved to:
- output/final_test_with_preds.csv
- output/final_aug_test_with_preds.csv
