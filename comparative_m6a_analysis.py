#!/usr/bin/env python3

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import os

def load_m6a_data(cell_line):
    """Load m6A data for a specific cell line"""
    print(f"Loading {cell_line} data...")
    
    cell_data = defaultdict(dict)
    data_dir = f"data/raw/{cell_line}"
    
    # Find all JSON files for this cell line
    json_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file == "data.json":
                json_files.append(os.path.join(root, file))
    
    print(f"Found {len(json_files)} replicates for {cell_line}")
    
    # Load each replicate
    for json_file in json_files:
        replicate = os.path.basename(os.path.dirname(json_file))
        print(f"  Loading {replicate}...")
        
        with open(json_file, 'r') as f:
            for line_num, line in enumerate(f):
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        for transcript_id, positions in data.items():
                            if transcript_id not in cell_data:
                                cell_data[transcript_id] = {}
                            
                            for position, motif_data in positions.items():
                                pos_key = f"{position}"
                                if pos_key not in cell_data[transcript_id]:
                                    cell_data[transcript_id][pos_key] = []
                                
                                # Store motif and probability info
                                for motif, prob_data in motif_data.items():
                                    cell_data[transcript_id][pos_key].append({
                                        'motif': motif,
                                        'probability': prob_data[0][0] if prob_data else 0,
                                        'replicate': replicate
                                    })
                                    
                    except json.JSONDecodeError:
                        continue
                        
                # Progress indicator
                if line_num % 100000 == 0 and line_num > 0:
                    print(f"    Processed {line_num} lines...")
    
    return dict(cell_data)

def summarize_cell_line(cell_data, cell_line):
    """Summarize m6A data for one cell line"""
    total_transcripts = len(cell_data)
    total_sites = sum(len(positions) for positions in cell_data.values())
    
    # Get motif distribution
    motifs = []
    probabilities = []
    for transcript, positions in cell_data.items():
        for position, site_data in positions.items():
            for site in site_data:
                motifs.append(site['motif'])
                probabilities.append(site['probability'])
    
    motif_counts = pd.Series(motifs).value_counts()
    avg_probability = np.mean(probabilities)
    
    return {
        'cell_line': cell_line,
        'transcripts': total_transcripts,
        'sites': total_sites,
        'avg_probability': avg_probability,
        'top_motifs': motif_counts.head().to_dict(),
        'all_probabilities': probabilities
    }

def main():
    print("=== Cross-Cancer m6A Analysis ===")
    
    # Cell lines to analyze
    cell_lines = ['A549', 'HepG2', 'MCF7', 'K562']
    
    # Load data for each cell line
    all_data = {}
    summaries = []
    
    for cell_line in cell_lines:
        cell_data = load_m6a_data(cell_line)
        all_data[cell_line] = cell_data
        
        summary = summarize_cell_line(cell_data, cell_line)
        summaries.append(summary)
        
        print(f"\n{cell_line} Summary:")
        print(f"  Transcripts with m6A: {summary['transcripts']:,}")
        print(f"  Total m6A sites: {summary['sites']:,}")
        print(f"  Average probability: {summary['avg_probability']:.4f}")
        print(f"  Top motifs: {list(summary['top_motifs'].keys())[:3]}")
    
    # Create comparison table
    comparison_df = pd.DataFrame(summaries)
    print(f"\n=== Cross-Cancer Comparison ===")
    print(comparison_df[['cell_line', 'transcripts', 'sites', 'avg_probability']])
    
    # Save results
    os.makedirs('results', exist_ok=True)
    comparison_df.to_csv('results/m6a_comparison.csv', index=False)
    
    print(f"\n✅ Analysis complete! Results saved to results/m6a_comparison.csv")

if __name__ == "__main__":
    main()
