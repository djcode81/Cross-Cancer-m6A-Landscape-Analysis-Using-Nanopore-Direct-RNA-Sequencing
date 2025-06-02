#!/bin/bash
#SBATCH --job-name=download_data
#SBATCH --output=download_%j.log
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --partition=dept_cpu

eval "$(conda shell.bash hook)"
conda activate m6a_analysis
cd ~/projects/cross-cancer-m6a-analysis

echo "Starting download at $(date)"

# Download each cell line
for cell_line in A549 HepG2 MCF7 K562; do
    echo "Downloading $cell_line..."
    aws s3 sync --no-sign-request \
        s3://sg-nex-data/data/processed_data/m6Anet/ \
        data/raw/$cell_line/ \
        --exclude "*" \
        --include "*${cell_line}_directRNA*"
done

echo "Download complete at $(date)"
du -sh data/raw/*
