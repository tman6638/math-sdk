#!/usr/bin/env python3
"""Convert JSON books to JSONL.zst format for Stake Engine upload"""

import json
import zstandard as zstd
import os
from pathlib import Path

# Paths
books_dir = Path("/home/runner/work/math-sdk/math-sdk/games/sweet_bonanza_clone/library/books")
publish_dir = Path("/home/runner/work/math-sdk/math-sdk/games/sweet_bonanza_clone/library/publish_files")

# Bet modes to process
bet_modes = ["base", "ante", "bonus_buy", "super_bonus"]

print("Converting and compressing book files...\n")

for mode in bet_modes:
    input_file = books_dir / f"books_{mode}.json"
    output_file = publish_dir / f"books_{mode}.jsonl.zst"
    
    if not input_file.exists():
        print(f"⚠️  Warning: {input_file} not found, skipping...")
        continue
    
    print(f"Processing {mode}...")
    
    # Read JSON array
    with open(input_file, 'r') as f:
        books = json.load(f)
    
    print(f"  - Loaded {len(books)} book entries")
    
    # Convert to JSONL (one JSON object per line)
    jsonl_data = '\n'.join(json.dumps(book, separators=(',', ':')) for book in books)
    
    # Compress with zstandard
    cctx = zstd.ZstdCompressor(level=3)  # Level 3 for good compression/speed balance
    compressed_data = cctx.compress(jsonl_data.encode('utf-8'))
    
    # Write compressed file
    with open(output_file, 'wb') as f:
        f.write(compressed_data)
    
    original_size = len(jsonl_data.encode('utf-8'))
    compressed_size = len(compressed_data)
    ratio = (1 - compressed_size / original_size) * 100
    
    print(f"  - Original size: {original_size / 1024 / 1024:.2f} MB")
    print(f"  - Compressed size: {compressed_size / 1024:.2f} KB")
    print(f"  - Compression ratio: {ratio:.1f}%")
    print(f"  ✅ Created {output_file.name}\n")

print("="*60)
print("Conversion complete!")
print(f"\nFiles ready for upload in: {publish_dir}")
print("\nFiles to upload to Stake Engine:")
print("  1. index.json")
print("  2. lookUpTable_base_0.csv")
print("  3. lookUpTable_ante_0.csv")
print("  4. lookUpTable_bonus_buy_0.csv")
print("  5. lookUpTable_super_bonus_0.csv")
print("  6. books_base.jsonl.zst")
print("  7. books_ante.jsonl.zst")
print("  8. books_bonus_buy.jsonl.zst")
print("  9. books_super_bonus.jsonl.zst")
print("="*60)
