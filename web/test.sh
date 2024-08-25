#!/bin/bash

# Activate conda environment
# conda init
conda activate dl

echo "Starting object detection..."

# Run a Python script
python run_object_detect.py

echo "Done object detection!"

python test.py --dataroot test_cycle_gan --name latest_net_G  --model test --no_dropout

echo "Done cycleGAN!"

python run_verify.py

echo "Finished!"

conda deactivate
