#!/bin/bash -l
echo 'date: ' $(date)
conda activate chemprop

export RAY_TEMP_DIR=/home/akshatz/bond_order_free/tmp_dir_1
mkdir -p $RAY_TEMP_DIR

results_dir="."
data_path="/home/akshatz/bond_order_free/barriers_sn2/dataset/sn2_data.csv"
splits_path="/home/akshatz/bond_order_free/barriers_sn2/dataset/splits.json"

#Hyperparameter optimization
chemprop hpopt \
-t regression \
--data-path $data_path \
--splits-file $splits_path \
--num-workers 20 \
--raytune-num-samples 100 \
--molecule-featurizers charge \
--epochs 200 \
--aggregation norm \
--no-batch-norm \
--raytune-temp-dir $RAY_TEMP_DIR \
--raytune-num-cpus 40 \
--raytune-num-gpus 2 \
--raytune-max-concurrent-trials 2 \
--search-parameter-keywords depth ffn_num_layers message_hidden_dim ffn_hidden_dim dropout max_lr final_lr init_lr batch_size warmup_epochs \
--hyperopt-random-state-seed 42 \
--hpopt-save-dir $results_dir \
--reaction-columns AAM \
--add-h \
--keep-h 

#Training with optimized hyperparameters
chemprop train \
-t regression \
--data-path $data_path \
--splits-file $splits_path \
--molecule-featurizers charge \
--num-workers 20 \
--epochs 200 \
--pytorch-seed 42 \
--aggregation norm \
--no-batch-norm \
--accelerator gpu \
--devices 1 \
--reaction-columns AAM \
--add-h \
--keep-h \
--save-dir $results_dir \
--ensemble-size 5 \
--metrics mae rmse \
--config-path $results_dir/best_config.toml

echo 'date: ' $(date)