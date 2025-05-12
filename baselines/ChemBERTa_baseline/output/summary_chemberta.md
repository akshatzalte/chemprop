# Split 1 of 5
# Predicting the mean baseline
timestamp: 2025-05-09 19:36:52.242738
## Mean Predictions
Mean Training Target: 7.8399 kcal/mol
Mean Test Target: -6.4638 kcal/mol
Mean Augmented Test Target: -8.0790 kcal/mol

## RMSE for Mean Predictions:
### final_test.csv
RMSE: 63.7638 kcal/mol

### final_aug_test.csv
RMSE: 63.5695 kcal/mol

# ChemBERTa Baseline Results
timestamp: 2025-05-09 19:36:52.242764

## Random Seed 42

### final_test.csv
RMSE: 17.6401 kcal/mol
MAE: 12.7160 kcal/mol

### final_aug_test.csv
RMSE: 19.3745 kcal/mol
MAE: 14.2121 kcal/mol

## Random Seed 117

### final_test.csv
RMSE: 18.7513 kcal/mol
MAE: 13.2125 kcal/mol

### final_aug_test.csv
RMSE: 20.9446 kcal/mol
MAE: 15.0735 kcal/mol

## Random Seed 709

### final_test.csv
RMSE: 17.8456 kcal/mol
MAE: 13.3230 kcal/mol

### final_aug_test.csv
RMSE: 19.3206 kcal/mol
MAE: 14.5996 kcal/mol

## Random Seed 1701

### final_test.csv
RMSE: 19.6825 kcal/mol
MAE: 14.0423 kcal/mol

### final_aug_test.csv
RMSE: 21.7462 kcal/mol
MAE: 15.8133 kcal/mol

## Random Seed 9001

### final_test.csv
RMSE: 17.9549 kcal/mol
MAE: 13.4714 kcal/mol

### final_aug_test.csv
RMSE: 19.6513 kcal/mol
MAE: 14.8053 kcal/mol


## Summary for Split 1

### Averaged Predictions RMSE
- final_test.csv: 17.6746 kcal/mol (MAE: 12.5533 kcal/mol)
- final_aug_test.csv: 19.5627 kcal/mol (MAE: 14.1658 kcal/mol)

### Performance Dictionary
```
results_dict = {
    "final_test": {
        "seed_42": 17.640111326725552,
        "seed_117": 18.751334063693303,
        "seed_709": 17.845550863596465,
        "seed_1701": 19.682459563159863,
        "seed_9001": 17.95486400959912,
        "average": 17.67455432660401
    },
    "final_aug_test": {
        "seed_42": 19.374485920297992,
        "seed_117": 20.944603389632757,
        "seed_709": 19.32063856899542,
        "seed_1701": 21.746155617117473,
        "seed_9001": 19.65128454175859,
        "average": 19.562722058227255
    }
}
```


Output files with predictions for split 0 have been saved to:
- output/final_test_with_chemberta_preds_0.csv
- output/final_aug_test_with_chemberta_preds_0.csv
# Split 2 of 5
# Predicting the mean baseline
timestamp: 2025-05-09 19:44:26.961069
## Mean Predictions
Mean Training Target: 4.5080 kcal/mol
Mean Test Target: -6.4638 kcal/mol
Mean Augmented Test Target: -8.0790 kcal/mol

## RMSE for Mean Predictions:
### final_test.csv
RMSE: 63.0999 kcal/mol

### final_aug_test.csv
RMSE: 62.8181 kcal/mol

# ChemBERTa Baseline Results
timestamp: 2025-05-09 19:44:26.961082

## Random Seed 42

### final_test.csv
RMSE: 17.9457 kcal/mol
MAE: 12.8929 kcal/mol

### final_aug_test.csv
RMSE: 19.7299 kcal/mol
MAE: 14.4548 kcal/mol

## Random Seed 117

### final_test.csv
RMSE: 18.6475 kcal/mol
MAE: 13.1356 kcal/mol

### final_aug_test.csv
RMSE: 20.9340 kcal/mol
MAE: 15.0507 kcal/mol

## Random Seed 709

### final_test.csv
RMSE: 18.6642 kcal/mol
MAE: 13.2652 kcal/mol

### final_aug_test.csv
RMSE: 20.7747 kcal/mol
MAE: 15.0992 kcal/mol

## Random Seed 1701

### final_test.csv
RMSE: 18.2108 kcal/mol
MAE: 13.3898 kcal/mol

### final_aug_test.csv
RMSE: 19.8596 kcal/mol
MAE: 14.8452 kcal/mol

## Random Seed 9001

### final_test.csv
RMSE: 18.3578 kcal/mol
MAE: 13.0444 kcal/mol

### final_aug_test.csv
RMSE: 20.4459 kcal/mol
MAE: 14.8500 kcal/mol


## Summary for Split 2

### Averaged Predictions RMSE
- final_test.csv: 17.8143 kcal/mol (MAE: 12.5119 kcal/mol)
- final_aug_test.csv: 19.8214 kcal/mol (MAE: 14.2572 kcal/mol)

### Performance Dictionary
```
results_dict = {
    "final_test": {
        "seed_42": 17.94565639875672,
        "seed_117": 18.64754674166005,
        "seed_709": 18.664168181799806,
        "seed_1701": 18.210817892171008,
        "seed_9001": 18.357841548458516,
        "average": 17.814290713141304
    },
    "final_aug_test": {
        "seed_42": 19.7298840986039,
        "seed_117": 20.93401184398008,
        "seed_709": 20.774749335590407,
        "seed_1701": 19.85957824501732,
        "seed_9001": 20.44585128628548,
        "average": 19.821440958089664
    }
}
```


Output files with predictions for split 1 have been saved to:
- output/final_test_with_chemberta_preds_1.csv
- output/final_aug_test_with_chemberta_preds_1.csv
# Split 3 of 5
# Predicting the mean baseline
timestamp: 2025-05-09 19:55:15.591412
## Mean Predictions
Mean Training Target: 10.0060 kcal/mol
Mean Test Target: -6.4638 kcal/mol
Mean Augmented Test Target: -8.0790 kcal/mol

## RMSE for Mean Predictions:
### final_test.csv
RMSE: 64.2843 kcal/mol

### final_aug_test.csv
RMSE: 64.1463 kcal/mol

# ChemBERTa Baseline Results
timestamp: 2025-05-09 19:55:15.591428

## Random Seed 42

### final_test.csv
RMSE: 18.9287 kcal/mol
MAE: 13.5027 kcal/mol

### final_aug_test.csv
RMSE: 20.9731 kcal/mol
MAE: 15.2897 kcal/mol

## Random Seed 117

### final_test.csv
RMSE: 18.9421 kcal/mol
MAE: 13.3760 kcal/mol

### final_aug_test.csv
RMSE: 21.4012 kcal/mol
MAE: 15.4420 kcal/mol

## Random Seed 709

### final_test.csv
RMSE: 18.4744 kcal/mol
MAE: 13.2035 kcal/mol

### final_aug_test.csv
RMSE: 20.5639 kcal/mol
MAE: 14.9715 kcal/mol

## Random Seed 1701

### final_test.csv
RMSE: 20.6551 kcal/mol
MAE: 14.6124 kcal/mol

### final_aug_test.csv
RMSE: 22.8817 kcal/mol
MAE: 16.6131 kcal/mol

## Random Seed 9001

### final_test.csv
RMSE: 19.5560 kcal/mol
MAE: 14.0807 kcal/mol

### final_aug_test.csv
RMSE: 21.8241 kcal/mol
MAE: 16.0473 kcal/mol


## Summary for Split 3

### Averaged Predictions RMSE
- final_test.csv: 18.7884 kcal/mol (MAE: 13.1609 kcal/mol)
- final_aug_test.csv: 21.0199 kcal/mol (MAE: 15.1019 kcal/mol)

### Performance Dictionary
```
results_dict = {
    "final_test": {
        "seed_42": 18.928727759680267,
        "seed_117": 18.942134245581773,
        "seed_709": 18.47441784943269,
        "seed_1701": 20.65512950901687,
        "seed_9001": 19.55604480301609,
        "average": 18.788378281183668
    },
    "final_aug_test": {
        "seed_42": 20.973073036355334,
        "seed_117": 21.40123198322726,
        "seed_709": 20.5639320757015,
        "seed_1701": 22.881725131015504,
        "seed_9001": 21.824108156189432,
        "average": 21.019861274455597
    }
}
```


Output files with predictions for split 2 have been saved to:
- output/final_test_with_chemberta_preds_2.csv
- output/final_aug_test_with_chemberta_preds_2.csv
# Split 4 of 5
# Predicting the mean baseline
timestamp: 2025-05-09 20:02:46.747315
## Mean Predictions
Mean Training Target: 6.2134 kcal/mol
Mean Test Target: -6.4638 kcal/mol
Mean Augmented Test Target: -8.0790 kcal/mol

## RMSE for Mean Predictions:
### final_test.csv
RMSE: 63.4187 kcal/mol

### final_aug_test.csv
RMSE: 63.1819 kcal/mol

# ChemBERTa Baseline Results
timestamp: 2025-05-09 20:02:46.747331

## Random Seed 42

### final_test.csv
RMSE: 18.5353 kcal/mol
MAE: 13.5162 kcal/mol

### final_aug_test.csv
RMSE: 20.3613 kcal/mol
MAE: 15.1336 kcal/mol

## Random Seed 117

### final_test.csv
RMSE: 17.8021 kcal/mol
MAE: 12.5497 kcal/mol

### final_aug_test.csv
RMSE: 19.6813 kcal/mol
MAE: 14.2567 kcal/mol

## Random Seed 709

### final_test.csv
RMSE: 17.6576 kcal/mol
MAE: 12.8019 kcal/mol

### final_aug_test.csv
RMSE: 19.4402 kcal/mol
MAE: 14.3489 kcal/mol

## Random Seed 1701

### final_test.csv
RMSE: 17.5599 kcal/mol
MAE: 12.8400 kcal/mol

### final_aug_test.csv
RMSE: 19.3979 kcal/mol
MAE: 14.3522 kcal/mol

## Random Seed 9001

### final_test.csv
RMSE: 18.2572 kcal/mol
MAE: 12.9730 kcal/mol

### final_aug_test.csv
RMSE: 20.4186 kcal/mol
MAE: 14.7837 kcal/mol


## Summary for Split 4

### Averaged Predictions RMSE
- final_test.csv: 17.5047 kcal/mol (MAE: 12.4533 kcal/mol)
- final_aug_test.csv: 19.4110 kcal/mol (MAE: 14.0833 kcal/mol)

### Performance Dictionary
```
results_dict = {
    "final_test": {
        "seed_42": 18.535340471466384,
        "seed_117": 17.802139337203375,
        "seed_709": 17.65761383714901,
        "seed_1701": 17.55994203243767,
        "seed_9001": 18.257196536986843,
        "average": 17.504682750234583
    },
    "final_aug_test": {
        "seed_42": 20.36132966088015,
        "seed_117": 19.681349813332034,
        "seed_709": 19.440236799300727,
        "seed_1701": 19.39791741288228,
        "seed_9001": 20.41858403623483,
        "average": 19.410973650982275
    }
}
```


Output files with predictions for split 3 have been saved to:
- output/final_test_with_chemberta_preds_3.csv
- output/final_aug_test_with_chemberta_preds_3.csv
# Split 5 of 5
# Predicting the mean baseline
timestamp: 2025-05-09 20:10:27.641816
## Mean Predictions
Mean Training Target: 11.3337 kcal/mol
Mean Test Target: -6.4638 kcal/mol
Mean Augmented Test Target: -8.0790 kcal/mol

## RMSE for Mean Predictions:
### final_test.csv
RMSE: 64.6372 kcal/mol

### final_aug_test.csv
RMSE: 64.5332 kcal/mol

# ChemBERTa Baseline Results
timestamp: 2025-05-09 20:10:27.641834

## Random Seed 42

### final_test.csv
RMSE: 17.8853 kcal/mol
MAE: 12.8445 kcal/mol

### final_aug_test.csv
RMSE: 19.7785 kcal/mol
MAE: 14.4589 kcal/mol

## Random Seed 117

### final_test.csv
RMSE: 18.9168 kcal/mol
MAE: 14.1148 kcal/mol

### final_aug_test.csv
RMSE: 20.4603 kcal/mol
MAE: 15.4058 kcal/mol

## Random Seed 709

### final_test.csv
RMSE: 19.4761 kcal/mol
MAE: 13.6723 kcal/mol

### final_aug_test.csv
RMSE: 21.6392 kcal/mol
MAE: 15.5620 kcal/mol

## Random Seed 1701

### final_test.csv
RMSE: 17.5922 kcal/mol
MAE: 12.7939 kcal/mol

### final_aug_test.csv
RMSE: 19.4317 kcal/mol
MAE: 14.2726 kcal/mol

## Random Seed 9001

### final_test.csv
RMSE: 19.1154 kcal/mol
MAE: 13.6558 kcal/mol

### final_aug_test.csv
RMSE: 21.2250 kcal/mol
MAE: 15.4812 kcal/mol


## Summary for Split 5

### Averaged Predictions RMSE
- final_test.csv: 18.0085 kcal/mol (MAE: 12.7805 kcal/mol)
- final_aug_test.csv: 19.9464 kcal/mol (MAE: 14.4093 kcal/mol)

### Performance Dictionary
```
results_dict = {
    "final_test": {
        "seed_42": 17.885335389864675,
        "seed_117": 18.916782793715097,
        "seed_709": 19.47613211683619,
        "seed_1701": 17.592150442635166,
        "seed_9001": 19.115352248280413,
        "average": 18.00845394857201
    },
    "final_aug_test": {
        "seed_42": 19.77848433776845,
        "seed_117": 20.460298087228505,
        "seed_709": 21.63917682474416,
        "seed_1701": 19.431668518121196,
        "seed_9001": 21.225027314953127,
        "average": 19.946406847361047
    }
}
```


Output files with predictions for split 4 have been saved to:
- output/final_test_with_chemberta_preds_4.csv
- output/final_aug_test_with_chemberta_preds_4.csv

# Overall Summary Across All Splits

## Final Test Set Performance
- RMSE: 17.9581 ± 0.4469 kcal/mol
- MAE: 12.6920 ± 0.2594 kcal/mol

## Augmented Test Set Performance
- RMSE: 19.9523 ± 0.5660 kcal/mol
- MAE: 14.4035 ± 0.3656 kcal/mol

## Performance Details By Split

| Split | Test RMSE | Test MAE | Aug Test RMSE | Aug Test MAE |
|-------|-----------|----------|--------------|-------------|
| 1 | 17.6746 | 12.5533 | 19.5627 | 14.1658 |
| 2 | 17.8143 | 12.5119 | 19.8214 | 14.2572 |
| 3 | 18.7884 | 13.1609 | 21.0199 | 15.1019 |
| 4 | 17.5047 | 12.4533 | 19.4110 | 14.0833 |
| 5 | 18.0085 | 12.7805 | 19.9464 | 14.4093 |
