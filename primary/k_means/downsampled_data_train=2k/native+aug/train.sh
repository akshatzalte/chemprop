#!/bin/bash -l
echo 'date: ' $(date)
conda activate chemprop

results_dir="."
data_path="../dataset/run4/data_run_4.csv"
split_path="../dataset/run4/splits.json"
best_config="../../rigr_h298_50k/run4_baseline_best/best_config.toml"

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
--devices 1 \
--ensemble-size 5 \
--num-folds 1 \
--pytorch-seed 21 \
--add-h \
--keep-h \
--config-path $best_config \
-vvv

echo 'date: ' $(date)