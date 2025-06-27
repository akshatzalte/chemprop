#!/bin/bash -l

results_dir="."
data_path="../../dataset/final_data_set.csv"
split_path="../../dataset/splits_timing.json"

chemprop -h # Load and cache all the python packages for correct timing of the actual chemprop train call

nvidia-smi \
--query-gpu=index,timestamp,name,pstate,memory.used,utilization.gpu,utilization.memory,power.draw,temperature.gpu \
--format=csv -l 10 > $results_dir/gpu_stats_train.csv &
nvidia-smi --query-compute-apps=timestamp,pid,process_name,used_memory \
--format=csv -l 10 > $results_dir/process_stats_train.csv &

/usr/bin/time -v chemprop train \
-t regression \
--data-path $data_path \
--splits-file $split_path \
--epochs 100 \
--aggregation sum \
--no-batch-norm \
--num-workers 20 \
--accelerator gpu \
--devices "1," \
--ensemble-size 1 \
--num-folds 1 \
--pytorch-seed 21 \
--add-h \
--keep-h \