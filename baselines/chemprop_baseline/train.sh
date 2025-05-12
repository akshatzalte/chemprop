#!/bin/bash -l
echo 'date: ' $(date)
conda activate chemprop

results_dir="."
data_path="../dataset/final_data_set.csv"
split_path="../dataset/splits.json"

chemprop train \
-t regression \
--data-path $data_path \
--splits-file $split_path \
--epochs 100 \
--aggregation sum \
--no-batch-norm \
--num-workers 20 \
--accelerator gpu \
--devices 1 \
--ensemble-size 1 \
--num-folds 5 \
--pytorch-seed 21 \
--add-h \
--keep-h \
-vvv

echo 'date: ' $(date)