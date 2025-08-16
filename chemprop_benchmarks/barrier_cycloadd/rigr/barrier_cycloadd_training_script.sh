#!/bin/bash -l
echo 'date: ' $(date)
conda activate chemprop

results_dir="."
data_path="/home/akshatz/bond_order_free/barriers_cycloadd/dataset/cycloadd_data.csv"
splits_path="/home/akshatz/bond_order_free/barriers_cycloadd/dataset/multiple_splits.json"

#Training with optimized hyperparameters
chemprop train \
-t regression \
--data-path $data_path \
--splits-file $splits_path \
--num-workers 20 \
--epochs 200 \
--pytorch-seed 42 \
--aggregation norm \
--no-batch-norm \
--save-dir $results_dir \
--ensemble-size 5 \
--num-folds 5 \
--metrics mae \
--reaction-columns rxn_smiles \
--target-columns G_act \
--config-path $results_dir/best_config.toml \
--add-h \
--keep-h \
--accelerator gpu \
--devices "1," \
--molecule-featurizers charge 

echo 'date: ' $(date)