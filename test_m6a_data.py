import json
import pandas as pd

print("Testing m6A data loading...")

# Load the m6A predictions
with open('data/raw/A549_test/data.json', 'r') as f:
    m6a_data = json.load(f)

print(f"Number of m6A sites detected: {len(m6a_data)}")
print(f"First few genes with m6A sites: {list(m6a_data.keys())[:5]}")

# Look at one example
first_gene = list(m6a_data.keys())[0]
first_sites = m6a_data[first_gene]
print(f"\nExample gene '{first_gene}' has {len(first_sites)} m6A sites")
print(f"First site details: {first_sites[0]}")

print("\nData loading test successful!")
