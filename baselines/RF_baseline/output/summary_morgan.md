# Predicing the mean baseline
timestamp: 2025-05-09 22:57:42.136823
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
timestamp: 2025-05-09 22:57:42.136839

## Random Seed 42

### final_test.csv
RMSE: 29.1489 kcal/mol

### final_aug_test.csv
RMSE: 29.4641 kcal/mol

## Random Seed 117

### final_test.csv
RMSE: 29.0616 kcal/mol

### final_aug_test.csv
RMSE: 29.3520 kcal/mol

## Random Seed 709

### final_test.csv
RMSE: 29.0050 kcal/mol

### final_aug_test.csv
RMSE: 29.3029 kcal/mol

## Random Seed 1701

### final_test.csv
RMSE: 29.0784 kcal/mol

### final_aug_test.csv
RMSE: 29.3269 kcal/mol

## Random Seed 9001

### final_test.csv
RMSE: 28.9971 kcal/mol

### final_aug_test.csv
RMSE: 29.3414 kcal/mol


## Summary

### Averaged Predictions RMSE
- final_test.csv: 28.9402 kcal/mol
- final_aug_test.csv: 29.2361 kcal/mol

### Performance Dictionary
```
results_dict = {
    "final_test": {
        "seed_42": 29.148942380742714,
        "seed_117": 29.061595157721126,
        "seed_709": 29.005012844131198,
        "seed_1701": 29.07839789404969,
        "seed_9001": 28.997055192544757,
        "average": 28.9401570110979
    },
    "final_aug_test": {
        "seed_42": 29.464116045789865,
        "seed_117": 29.351959808371706,
        "seed_709": 29.302911896565835,
        "seed_1701": 29.326919294543035,
        "seed_9001": 29.34142000634253,
        "average": 29.236144831497395
    }
}
```


Output files with predictions have been saved to:
- output/final_test_with_preds.csv
- output/final_aug_test_with_preds.csv
