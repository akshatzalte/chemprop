#!/bin/bash -l
echo 'date: ' $(date)
conda activate chemprop

export RAY_TEMP_DIR=/home/akshatz/bond_order_free/tmp_dir_2
mkdir -p $RAY_TEMP_DIR

results_dir="."
data_path="../dataset/final_aug_data_set.csv"
split_path="../dataset/aug_splits.json"

chemprop hpopt \
-t regression \
--data-path $data_path \
--splits-file $split_path \
--weight-column weights \
--hyperopt-n-initial-points 80 \
--raytune-num-samples 160 \
--epochs 100 \
--raytune-grace-period 100 \
--hyperopt-random-state-seed 21 \
--aggregation sum \
--no-batch-norm \
--raytune-temp-dir $RAY_TEMP_DIR \
--raytune-num-cpus 40 \
--raytune-num-gpus 2 \
--raytune-max-concurrent-trials 2 \
--search-parameter-keywords ffn_num_layers ffn_hidden_dim depth message_hidden_dim dropout \
--num-workers 20 \
--hpopt-save-dir $results_dir \
--smiles-columns resonance_smis \
--target-columns H298_kcal \
--add-h \
--keep-h \
--raytune-use-gpu \
-vvv

echo 'date: ' $(date)

chemprop train \
-t regression \
--data-path $data_path \
--splits-file $split_path \
--target-columns H298_kcal \
--weight-column weights \
--epochs 100 \
--aggregation sum \
--no-batch-norm \
--num-workers 20 \
--accelerator gpu \
--devices "1," \
--ensemble-size 5 \
--num-folds 5 \
--pytorch-seed 21 \
--add-h \
--keep-h \
--config-path $results_dir/best_config.toml \
-vvv

echo 'date: ' $(date)