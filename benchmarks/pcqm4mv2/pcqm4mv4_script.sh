#!/bin/bash -l
echo 'date: ' $(date)
conda activate chemprop

export RAY_TEMP_DIR=/home/akshatz/bond_order_free/tmp_dir_666
mkdir -p $RAY_TEMP_DIR

results_dir="results"
data_path="/home/akshatz/bond_order_free/pcqm4mv2/dataset/pcqm4mv2_data.csv"
splits_path="/home/akshatz/bond_order_free/pcqm4mv2/dataset/splits.json"

#Hyperparameter optimization
chemprop hpopt \
-t regression \
--data-path $data_path \
--splits-file $splits_path \
--num-workers 20 \
--raytune-num-samples 30 \
--epochs 50 \
--aggregation norm \
--no-batch-norm \
--raytune-temp-dir $RAY_TEMP_DIR \
--raytune-num-cpus 40 \
--raytune-num-gpus 2 \
--raytune-max-concurrent-trials 2 \
--search-parameter-keywords depth ffn_num_layers message_hidden_dim ffn_hidden_dim dropout \
--hyperopt-random-state-seed 42 \
--hpopt-save-dir $results_dir \
--molecule-featurizers charge 

echo 'date: ' $(date)

#Training with optimized hyperparameters
chemprop train \
-t regression \
--data-path $data_path \
--splits-file $splits_path \
--num-workers 20 \
--epochs 50 \
--pytorch-seed 42 \
--aggregation norm \
--no-batch-norm \
--save-dir $results_dir \
--ensemble-size 5 \
--metrics mae r2 \
--config-path $results_dir/best_config.toml \
--accelerator gpu \
--devices "1," \
--molecule-featurizers charge 

echo 'date: ' $(date)