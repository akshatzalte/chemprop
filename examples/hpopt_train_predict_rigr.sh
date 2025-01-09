#!/bin/bash -l
conda activate chemprop

# Example script for using RIGR as a flag (`--rigr`)

export RAY_TEMP_DIR=/home/akshatz/bond_order_free/tmp_dir_80
mkdir -p $RAY_TEMP_DIR

results_dir="."
data_path="../dataset/run1/data_run_1.csv"
split_path="../dataset/run1/splits.json"

# Be consistent while using `--rigr` for each chemprop task (hpopt, train, predict)

# Hyperparameter optimization 
# Using RIGR along with additional molecular features
chemprop hpopt \
-t regression \
--data-path $data_path \
--splits-file $splits_path \
--rigr \
--molecule-featurizer charge multiplicity \
--add-h \
--keep-h \
--epochs 10 \
--aggregation sum \
--no-batch-norm \
--raytune-temp-dir $RAY_TEMP_DIR \
--raytune-num-cpus 40 \
--raytune-num-gpus 2 \
--raytune-max-concurrent-trials 2 \
--search-parameter-keywords depth ffn_num_layers message_hidden_dim ffn_hidden_dim dropout \
--hyperopt-random-state-seed 42 \
--hpopt-save-dir $results_dir \

# Training
# Using RIGR along with additional molecular features
chemprop train \
-t regression \
--data-path $data_path \
--splits-file $split_path \
--rigr \
--molecule-featurizer charge multiplicity \
--add-h \
--keep-h \
--epochs 10 \
--aggregation sum \
--no-batch-norm \
--num-workers 20 \
--accelerator gpu \
--devices 1 \
--ensemble-size 1 \
--num-folds 1 \
--pytorch-seed 21 \
--config-path $results_dir/best_config.toml \
-vvv

# Inference
# Using RIGR along with additional molecular features
chemprop predict \
-i ../../rigr_h298_50k/dataset/final_aug_test.csv \
-o results_aug/test_preds.csv \
--model-path $all_model_dir \
--rigr \
--molecule-featurizer charge multiplicity \
--add-h \
--keep-h \
--devices 1