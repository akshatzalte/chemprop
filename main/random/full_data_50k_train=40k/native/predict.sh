#!/bin/bash -l

mkdir results_base
mkdir results_rnd
mkdir results_aug

# Identify the latest directory within chemprop_training
data_run_dir=$(ls -t chemprop_training | head -1)
latest_dir=$(ls -t chemprop_training/$data_run_dir | head -1)
echo "Latest directory: $latest_dir"

# Loop over each fold
for i in {0..4}; do
    # Create directory for the current fold
    all_model_dir="models_fold_$i"
    mkdir -p $all_model_dir
    
    # Copy model files for each fold
    for j in {0..4}; do
        cp chemprop_training/$data_run_dir/$latest_dir/fold_$i/model_$j/best.pt $all_model_dir/best$j.pt
    done

    # Run Chemprop predictions on base test set
    chemprop predict \
        -i ../dataset/final_test.csv \
        -o results_base/test_preds_$i.csv \
        --model-path $all_model_dir \
        --add-h \
        --keep-h \
        --devices 1

    # Run Chemprop predictions on rnd test set
    chemprop predict \
        -i ../dataset/final_rnd_test.csv \
        -o results_rnd/test_preds_$i.csv \
        --model-path $all_model_dir \
        --add-h \
        --keep-h \
        --devices 1
    
    # Run Chemprop predictions on aug test set
    chemprop predict \
        -i ../dataset/final_aug_test.csv \
        -o results_aug/test_preds_$i.csv \
        --model-path $all_model_dir \
        --add-h \
        --keep-h \
        --devices 1

done