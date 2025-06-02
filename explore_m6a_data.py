import json

print("Exploring m6A data structure...")

# Load first few lines to understand format
m6a_data = {}
with open('data/raw/A549_test/data.json', 'r') as f:
    for i, line in enumerate(f):
        if i >= 5:  # Just look at first 5 lines
            break
        line = line.strip()
        if line:
            data = json.loads(line)
            print(f"Line {i+1} structure: {type(data)}")
            print(f"Line {i+1} keys: {list(data.keys())[:3] if isinstance(data, dict) else 'Not a dict'}")
            print(f"Line {i+1} sample: {data}")
            print("---")

print("\nNow loading some actual data...")

# Load a small sample
sample_data = {}
with open('data/raw/A549_test/data.json', 'r') as f:
    for i, line in enumerate(f):
        if i >= 100:  # Just first 100 lines
            break
        line = line.strip()
        if line:
            data = json.loads(line)
            if isinstance(data, dict):
                sample_data.update(data)

if sample_data:
    first_gene = list(sample_data.keys())[0]
    first_data = sample_data[first_gene]
    print(f"First gene: {first_gene}")
    print(f"Data type: {type(first_data)}")
    print(f"Data structure: {first_data}")

