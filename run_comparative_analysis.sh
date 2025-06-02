#!/bin/bash
#SBATCH --job-name=m6a_compare
#SBATCH --output=m6a_compare_%j.log
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --partition=dept_cpu

eval "$(conda shell.bash hook)"
conda activate m6a_analysis
cd ~/projects/cross-cancer-m6a-analysis

echo "Starting comparative m6A analysis at $(date)"
python comparative_m6a_analysis.py
echo "Finished at $(date)"
