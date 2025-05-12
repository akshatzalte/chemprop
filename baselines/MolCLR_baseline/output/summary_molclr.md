# Split 1 of 5
# Predicting the mean baseline
    timestamp: 2025-05-09 18:08:07.388695
    ## Mean Predictions
    Mean Training Target: 7.8399 kcal/mol
    Mean Test Target: -6.4638 kcal/mol
    Mean Augmented Test Target: -8.0790 kcal/mol

    ## RMSE for Mean Predictions:
    ### final_test.csv
    RMSE: 63.7638 kcal/mol

    ### final_aug_test.csv
    RMSE: 63.5695 kcal/mol

    # MolCLR Finetuning Results
    timestamp: 2025-05-09 18:08:07.388715

    ## Random Seed 42

    ### final_test.csv
    RMSE: 13.8633 kcal/mol
    MAE: 10.2663 kcal/mol

    ### final_aug_test.csv
    RMSE: 13.9409 kcal/mol
    MAE: 10.3485 kcal/mol

    ## Random Seed 117

    ### final_test.csv
    RMSE: 13.7692 kcal/mol
    MAE: 10.1509 kcal/mol

    ### final_aug_test.csv
    RMSE: 13.8539 kcal/mol
    MAE: 10.2274 kcal/mol

    ## Random Seed 709

    ### final_test.csv
    RMSE: 13.1455 kcal/mol
    MAE: 9.7465 kcal/mol

    ### final_aug_test.csv
    RMSE: 13.3280 kcal/mol
    MAE: 9.9252 kcal/mol

    ## Random Seed 1701

    ### final_test.csv
    RMSE: 13.6293 kcal/mol
    MAE: 10.1825 kcal/mol

    ### final_aug_test.csv
    RMSE: 13.9076 kcal/mol
    MAE: 10.4671 kcal/mol

    ## Random Seed 9001

    ### final_test.csv
    RMSE: 13.6260 kcal/mol
    MAE: 10.2351 kcal/mol

    ### final_aug_test.csv
    RMSE: 13.7823 kcal/mol
    MAE: 10.3961 kcal/mol

    
    ## Summary for Split 1

    ### Averaged Predictions RMSE
    - final_test.csv: 13.0999 kcal/mol (MAE: 9.7022 kcal/mol)
    - final_aug_test.csv: 13.2704 kcal/mol (MAE: 9.8700 kcal/mol)

    ### Performance Dictionary
    ```
    results_dict = {
    "final_test": {
        "seed_42": 13.86327838897705,
        "seed_117": 13.769208908081055,
        "seed_709": 13.14547061920166,
        "seed_1701": 13.62929916381836,
        "seed_9001": 13.626045227050781,
        "average": 13.099882531572572
    },
    "final_aug_test": {
        "seed_42": 13.94091796875,
        "seed_117": 13.853887557983398,
        "seed_709": 13.328001976013184,
        "seed_1701": 13.907649040222168,
        "seed_9001": 13.782328605651855,
        "average": 13.270351188688055
    }
}
    ```

    
    Output files with predictions for split 0 have been saved to:
    - output/final_test_with_molclr_preds_0.csv
    - output/final_aug_test_with_molclr_preds_0.csv
    # Split 2 of 5
# Predicting the mean baseline
    timestamp: 2025-05-09 19:09:30.945140
    ## Mean Predictions
    Mean Training Target: 4.5080 kcal/mol
    Mean Test Target: -6.4638 kcal/mol
    Mean Augmented Test Target: -8.0790 kcal/mol

    ## RMSE for Mean Predictions:
    ### final_test.csv
    RMSE: 63.0999 kcal/mol

    ### final_aug_test.csv
    RMSE: 62.8181 kcal/mol

    # MolCLR Finetuning Results
    timestamp: 2025-05-09 19:09:30.945154

    ## Random Seed 42

    ### final_test.csv
    RMSE: 14.6407 kcal/mol
    MAE: 11.0114 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.6814 kcal/mol
    MAE: 11.0573 kcal/mol

    ## Random Seed 117

    ### final_test.csv
    RMSE: 15.2373 kcal/mol
    MAE: 11.4060 kcal/mol

    ### final_aug_test.csv
    RMSE: 15.3280 kcal/mol
    MAE: 11.4495 kcal/mol

    ## Random Seed 709

    ### final_test.csv
    RMSE: 13.9648 kcal/mol
    MAE: 10.4204 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.2781 kcal/mol
    MAE: 10.7181 kcal/mol

    ## Random Seed 1701

    ### final_test.csv
    RMSE: 14.2006 kcal/mol
    MAE: 10.5312 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.2116 kcal/mol
    MAE: 10.5482 kcal/mol

    ## Random Seed 9001

    ### final_test.csv
    RMSE: 13.8714 kcal/mol
    MAE: 10.3500 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.0695 kcal/mol
    MAE: 10.4860 kcal/mol

    
    ## Summary for Split 2

    ### Averaged Predictions RMSE
    - final_test.csv: 13.8140 kcal/mol (MAE: 10.2584 kcal/mol)
    - final_aug_test.csv: 13.9463 kcal/mol (MAE: 10.3487 kcal/mol)

    ### Performance Dictionary
    ```
    results_dict = {
    "final_test": {
        "seed_42": 14.640670776367188,
        "seed_117": 15.23729419708252,
        "seed_709": 13.964797973632812,
        "seed_1701": 14.20063591003418,
        "seed_9001": 13.871437072753906,
        "average": 13.813998845556233
    },
    "final_aug_test": {
        "seed_42": 14.68144416809082,
        "seed_117": 15.32799243927002,
        "seed_709": 14.278094291687012,
        "seed_1701": 14.21163558959961,
        "seed_9001": 14.069497108459473,
        "average": 13.946276693149114
    }
}
    ```

    
    Output files with predictions for split 1 have been saved to:
    - output/final_test_with_molclr_preds_1.csv
    - output/final_aug_test_with_molclr_preds_1.csv
    # Split 3 of 5
# Predicting the mean baseline
    timestamp: 2025-05-09 20:27:00.037879
    ## Mean Predictions
    Mean Training Target: 10.0060 kcal/mol
    Mean Test Target: -6.4638 kcal/mol
    Mean Augmented Test Target: -8.0790 kcal/mol

    ## RMSE for Mean Predictions:
    ### final_test.csv
    RMSE: 64.2843 kcal/mol

    ### final_aug_test.csv
    RMSE: 64.1463 kcal/mol

    # MolCLR Finetuning Results
    timestamp: 2025-05-09 20:27:00.037899

    ## Random Seed 42

    ### final_test.csv
    RMSE: 13.9935 kcal/mol
    MAE: 10.3280 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.1054 kcal/mol
    MAE: 10.4849 kcal/mol

    ## Random Seed 117

    ### final_test.csv
    RMSE: 14.4667 kcal/mol
    MAE: 10.5608 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.4942 kcal/mol
    MAE: 10.6436 kcal/mol

    ## Random Seed 709

    ### final_test.csv
    RMSE: 14.1784 kcal/mol
    MAE: 10.4248 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.4596 kcal/mol
    MAE: 10.7391 kcal/mol

    ## Random Seed 1701

    ### final_test.csv
    RMSE: 14.0699 kcal/mol
    MAE: 10.1774 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.1467 kcal/mol
    MAE: 10.3906 kcal/mol

    ## Random Seed 9001

    ### final_test.csv
    RMSE: 14.4442 kcal/mol
    MAE: 10.5428 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.4708 kcal/mol
    MAE: 10.6874 kcal/mol

    
    ## Summary for Split 3

    ### Averaged Predictions RMSE
    - final_test.csv: 13.6642 kcal/mol (MAE: 9.9155 kcal/mol)
    - final_aug_test.csv: 13.7791 kcal/mol (MAE: 10.1192 kcal/mol)

    ### Performance Dictionary
    ```
    results_dict = {
    "final_test": {
        "seed_42": 13.993525505065918,
        "seed_117": 14.466702461242676,
        "seed_709": 14.17839241027832,
        "seed_1701": 14.069903373718262,
        "seed_9001": 14.44423770904541,
        "average": 13.664238429196866
    },
    "final_aug_test": {
        "seed_42": 14.10541820526123,
        "seed_117": 14.49418830871582,
        "seed_709": 14.459610939025879,
        "seed_1701": 14.146651268005371,
        "seed_9001": 14.470752716064453,
        "average": 13.77912279274577
    }
}
    ```

    
    Output files with predictions for split 2 have been saved to:
    - output/final_test_with_molclr_preds_2.csv
    - output/final_aug_test_with_molclr_preds_2.csv
    # Split 4 of 5
# Predicting the mean baseline
    timestamp: 2025-05-09 21:29:55.265124
    ## Mean Predictions
    Mean Training Target: 6.2134 kcal/mol
    Mean Test Target: -6.4638 kcal/mol
    Mean Augmented Test Target: -8.0790 kcal/mol

    ## RMSE for Mean Predictions:
    ### final_test.csv
    RMSE: 63.4187 kcal/mol

    ### final_aug_test.csv
    RMSE: 63.1819 kcal/mol

    # MolCLR Finetuning Results
    timestamp: 2025-05-09 21:29:55.265138

    ## Random Seed 42

    ### final_test.csv
    RMSE: 14.0591 kcal/mol
    MAE: 10.4349 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.2279 kcal/mol
    MAE: 10.6479 kcal/mol

    ## Random Seed 117

    ### final_test.csv
    RMSE: 13.8293 kcal/mol
    MAE: 10.3320 kcal/mol

    ### final_aug_test.csv
    RMSE: 13.9087 kcal/mol
    MAE: 10.4589 kcal/mol

    ## Random Seed 709

    ### final_test.csv
    RMSE: 14.2070 kcal/mol
    MAE: 10.4203 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.3942 kcal/mol
    MAE: 10.6289 kcal/mol

    ## Random Seed 1701

    ### final_test.csv
    RMSE: 14.1824 kcal/mol
    MAE: 10.3462 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.3195 kcal/mol
    MAE: 10.4856 kcal/mol

    ## Random Seed 9001

    ### final_test.csv
    RMSE: 14.0733 kcal/mol
    MAE: 10.4211 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.1962 kcal/mol
    MAE: 10.5385 kcal/mol

    
    ## Summary for Split 4

    ### Averaged Predictions RMSE
    - final_test.csv: 13.3403 kcal/mol (MAE: 9.7870 kcal/mol)
    - final_aug_test.csv: 13.5000 kcal/mol (MAE: 9.9650 kcal/mol)

    ### Performance Dictionary
    ```
    results_dict = {
    "final_test": {
        "seed_42": 14.059096336364746,
        "seed_117": 13.829264640808105,
        "seed_709": 14.207006454467773,
        "seed_1701": 14.18241024017334,
        "seed_9001": 14.07331657409668,
        "average": 13.340310027778479
    },
    "final_aug_test": {
        "seed_42": 14.227860450744629,
        "seed_117": 13.908744812011719,
        "seed_709": 14.394196510314941,
        "seed_1701": 14.319533348083496,
        "seed_9001": 14.196155548095703,
        "average": 13.499978782266082
    }
}
    ```

    
    Output files with predictions for split 3 have been saved to:
    - output/final_test_with_molclr_preds_3.csv
    - output/final_aug_test_with_molclr_preds_3.csv
    # Split 5 of 5
# Predicting the mean baseline
    timestamp: 2025-05-09 22:34:32.052970
    ## Mean Predictions
    Mean Training Target: 11.3337 kcal/mol
    Mean Test Target: -6.4638 kcal/mol
    Mean Augmented Test Target: -8.0790 kcal/mol

    ## RMSE for Mean Predictions:
    ### final_test.csv
    RMSE: 64.6372 kcal/mol

    ### final_aug_test.csv
    RMSE: 64.5332 kcal/mol

    # MolCLR Finetuning Results
    timestamp: 2025-05-09 22:34:32.052984

    ## Random Seed 42

    ### final_test.csv
    RMSE: 13.9366 kcal/mol
    MAE: 10.3590 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.1258 kcal/mol
    MAE: 10.5437 kcal/mol

    ## Random Seed 117

    ### final_test.csv
    RMSE: 13.2779 kcal/mol
    MAE: 9.7815 kcal/mol

    ### final_aug_test.csv
    RMSE: 13.4193 kcal/mol
    MAE: 9.9610 kcal/mol

    ## Random Seed 709

    ### final_test.csv
    RMSE: 13.3550 kcal/mol
    MAE: 9.9631 kcal/mol

    ### final_aug_test.csv
    RMSE: 13.4221 kcal/mol
    MAE: 10.0867 kcal/mol

    ## Random Seed 1701

    ### final_test.csv
    RMSE: 14.1506 kcal/mol
    MAE: 10.5052 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.4471 kcal/mol
    MAE: 10.8196 kcal/mol

    ## Random Seed 9001

    ### final_test.csv
    RMSE: 14.0390 kcal/mol
    MAE: 10.5024 kcal/mol

    ### final_aug_test.csv
    RMSE: 14.1969 kcal/mol
    MAE: 10.6883 kcal/mol

    
    ## Summary for Split 5

    ### Averaged Predictions RMSE
    - final_test.csv: 13.2653 kcal/mol (MAE: 9.8272 kcal/mol)
    - final_aug_test.csv: 13.4358 kcal/mol (MAE: 10.0309 kcal/mol)

    ### Performance Dictionary
    ```
    results_dict = {
    "final_test": {
        "seed_42": 13.9365816116333,
        "seed_117": 13.277921676635742,
        "seed_709": 13.354965209960938,
        "seed_1701": 14.150625228881836,
        "seed_9001": 14.03902530670166,
        "average": 13.265335560053778
    },
    "final_aug_test": {
        "seed_42": 14.125802040100098,
        "seed_117": 13.4193115234375,
        "seed_709": 13.42209529876709,
        "seed_1701": 14.447068214416504,
        "seed_9001": 14.196854591369629,
        "average": 13.4358398712499
    }
}
    ```

    
    Output files with predictions for split 4 have been saved to:
    - output/final_test_with_molclr_preds_4.csv
    - output/final_aug_test_with_molclr_preds_4.csv
    
# Overall Summary Across All Splits

## Final Test Set Performance
- RMSE: 13.4368 ± 0.2631 kcal/mol
- MAE: 9.8981 ± 0.1928 kcal/mol

## Augmented Test Set Performance
- RMSE: 13.5863 ± 0.2436 kcal/mol
- MAE: 10.0668 ± 0.1629 kcal/mol

## Performance Details By Split

| Split | Test RMSE | Test MAE | Aug Test RMSE | Aug Test MAE |
|-------|-----------|----------|--------------|-------------|
| 1 | 13.0999 | 9.7022 | 13.2704 | 9.8700 |
| 2 | 13.8140 | 10.2584 | 13.9463 | 10.3487 |
| 3 | 13.6642 | 9.9155 | 13.7791 | 10.1192 |
| 4 | 13.3403 | 9.7870 | 13.5000 | 9.9650 |
| 5 | 13.2653 | 9.8272 | 13.4358 | 10.0309 |
