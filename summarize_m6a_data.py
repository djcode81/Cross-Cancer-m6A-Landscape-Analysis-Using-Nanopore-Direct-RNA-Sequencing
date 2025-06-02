import json

print("=== A549 m6A Data Summary ===")

# Parse the data properly
transcripts = {}
total_sites = 0

with open('data/raw/A549_test/data.json', 'r') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if line:
            try:
                data = json.loads(line)
                for transcript_id, positions in data.items():
                    if transcript_id not in transcripts:
                        transcripts[transcript_id] = {}
                    
                    for position, motif_data in positions.items():
                        transcripts[transcript_id][position] = motif_data
                        total_sites += 1
                        
            except json.JSONDecodeError:
                print(f"Error parsing line {line_num}")

print(f"Total transcripts with m6A: {len(transcripts)}")
print(f"Total m6A sites: {total_sites}")

# Sample transcript analysis
sample_transcript = list(transcripts.keys())[0]
sample_data = transcripts[sample_transcript]
sample_position = list(sample_data.keys())[0]
sample_motif = list(sample_data[sample_position].keys())[0]
sample_values = sample_data[sample_position][sample_motif][0]

print(f"\nSample data structure:")
print(f"Transcript: {sample_transcript}")
print(f"Position: {sample_position}")
print(f"Motif: {sample_motif}")
print(f"Values: {sample_values}")
print(f"(Likely: probability scores, signal features, etc.)")

print(f"\nTop 10 transcripts by m6A site count:")
site_counts = {t: len(positions) for t, positions in transcripts.items()}
top_transcripts = sorted(site_counts.items(), key=lambda x: x[1], reverse=True)[:10]
for transcript, count in top_transcripts:
    print(f"{transcript}: {count} sites")

print("\n✅ A549 m6A data successfully parsed!")
