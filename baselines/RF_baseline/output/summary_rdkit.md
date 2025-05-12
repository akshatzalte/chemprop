# Predicing the mean baseline
timestamp: 2025-05-09 23:02:00.433815
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
timestamp: 2025-05-09 23:02:00.433831

## Random Seed 42

### final_test.csv
RMSE: 27.1372 kcal/mol

### final_aug_test.csv
RMSE: 28.9635 kcal/mol

## Random Seed 117

### final_test.csv
RMSE: 27.0117 kcal/mol

### final_aug_test.csv
RMSE: 28.8311 kcal/mol

## Random Seed 709

### final_test.csv
RMSE: 27.1031 kcal/mol

### final_aug_test.csv
RMSE: 28.9353 kcal/mol

## Random Seed 1701

### final_test.csv
RMSE: 27.0516 kcal/mol

### final_aug_test.csv
RMSE: 28.8979 kcal/mol

## Random Seed 9001

### final_test.csv
RMSE: 26.9636 kcal/mol

### final_aug_test.csv
RMSE: 28.8159 kcal/mol


## Summary

### Averaged Predictions RMSE
- final_test.csv: 26.9079 kcal/mol
- final_aug_test.csv: 28.7385 kcal/mol

### Performance Dictionary
```
results_dict = {
    "final_test": {
        "seed_42": 27.137203627281565,
        "seed_117": 27.01165790502442,
        "seed_709": 27.103073252092965,
        "seed_1701": 27.051648921165846,
        "seed_9001": 26.963632136230597,
        "average": 26.907885680918444
    },
    "final_aug_test": {
        "seed_42": 28.96346190364227,
        "seed_117": 28.831100593337727,
        "seed_709": 28.93530425767987,
        "seed_1701": 28.897878025528463,
        "seed_9001": 28.81589860545364,
        "average": 28.73851585557808
    }
}
```


Output files with predictions have been saved to:
- output/final_test_with_preds.csv
- output/final_aug_test_with_preds.csv
