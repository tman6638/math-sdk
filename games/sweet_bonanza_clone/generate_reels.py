#!/usr/bin/env python3
"""Generate balanced reel strips for Sweet Bonanza Clone to achieve ~96% RTP"""

import random
import csv
from pathlib import Path

# Configuration
REEL_LENGTH = 250  # Standard length for scatter-pay games
NUM_REELS = 6

# Symbol pools with frequencies (higher weight = more common)
# For a 6x5 tumbling game targeting 96% RTP, we need good hit rates

# Base game symbols - VERY HIGH frequency for 8+ scatter-pay matches
# With 30 positions and 8-symbol minimum, need ~27% frequency minimum
# Using only 4 symbols (2 high, 2 low) plus specials for better clustering
BASE_SYMBOLS = {
    # Only use 4 paying symbols for better concentration
    # High pays
    'H3': 70,   # ~23% - will cluster to 8+ sometimes
    'H4': 75,   # ~25% - will cluster to 8+ sometimes
    # Low pays - highest frequency
    'L3': 85,   # ~28% - best chance for 8+
    'L4': 90,   # ~30% - best chance for 8+
    # Special symbols
    'S': 30,    # ~10% scatter for bonus trigger (3 scatters avg per spin)
    'W': 25,    # ~8% wild helps create wins
}
# Note: H1, H2, L1, L2 will NOT appear in base game to concentrate wins

# Ante game symbols - increased scatter frequency
# Same 4 paying symbols but more scatters
ANTE_SYMBOLS = {
    'H3': 65,
    'H4': 70,
    'L3': 80,
    'L4': 85,
    'S': 50,  # Much higher scatter frequency (5 scatters avg per spin for bonus)
    'W': 25,
}

# Free spin symbols - ALL symbols active with high multipliers
# Free spins need BIG wins to justify the buy-in cost
FREE_SYMBOLS = {
    # All 8 paying symbols active in free spins for variety
    'H1': 45,
    'H2': 50,
    'H3': 55,
    'H4': 60,
    'L1': 50,
    'L2': 55,
    'L3': 60,
    'L4': 65,
    # Specials
    'S': 25,   # Scatters for retrigger
    'W': 30,   # More wilds in free spins
    'M': 40,   # Lots of multiplier bombs for big wins
}

# Win cap symbols - very high frequency for forced wins
WCAP_SYMBOLS = {
    'H1': 50,  # All high frequency to ensure big wins
    'H2': 50,
    'H3': 50,
    'H4': 50,
    'L1': 10,
    'L2': 10,
    'L3': 10,
    'L4': 10,
    'S': 5,
    'W': 5,
}


def generate_reel_strip(symbols_config, num_reels, reel_length, seed=None):
    """Generate a balanced reel strip"""
    if seed:
        random.seed(seed)
    
    # Create weighted symbol pool
    symbol_pool = []
    for symbol, weight in symbols_config.items():
        symbol_pool.extend([symbol] * weight)
    
    # Generate reels
    reels = []
    for reel_idx in range(num_reels):
        reel = []
        for row_idx in range(reel_length):
            # Add some position-based variation for better distribution
            # Ensure scatters are well distributed
            if symbols_config.get('S', 0) > 0:
                # Place scatters strategically every ~25-35 rows
                if row_idx % 30 == 15 and random.random() < 0.7:
                    reel.append('S')
                    continue
            
            # Otherwise pick from pool
            reel.append(random.choice(symbol_pool))
        
        reels.append(reel)
    
    return reels


def write_reel_csv(reels, filename):
    """Write reel data to CSV file"""
    output_path = Path(__file__).parent / "reels" / filename
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        # Transpose - each row becomes one line with symbols for all reels
        for row_idx in range(len(reels[0])):
            row_data = [reels[reel_idx][row_idx] for reel_idx in range(len(reels))]
            writer.writerow(row_data)
    
    print(f"✅ Generated {filename} ({len(reels[0])} rows x {len(reels)} reels)")
    
    # Print symbol distribution stats
    symbol_counts = {}
    for reel in reels:
        for symbol in reel:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
    
    print(f"   Symbol distribution:")
    for symbol in sorted(symbol_counts.keys()):
        count = symbol_counts[symbol]
        percentage = (count / (len(reels[0]) * len(reels))) * 100
        print(f"   - {symbol}: {count} ({percentage:.1f}%)")


def main():
    """Generate all reel strips"""
    print("Generating reel strips for Sweet Bonanza Clone...\n")
    
    # Base game reels
    print("1. Base Game Reels (BR0)")
    base_reels = generate_reel_strip(BASE_SYMBOLS, NUM_REELS, REEL_LENGTH, seed=12345)
    write_reel_csv(base_reels, "BR0.csv")
    print()
    
    # Ante game reels
    print("2. Ante Game Reels (AR0)")
    ante_reels = generate_reel_strip(ANTE_SYMBOLS, NUM_REELS, REEL_LENGTH, seed=23456)
    write_reel_csv(ante_reels, "AR0.csv")
    print()
    
    # Free spin reels
    print("3. Free Spin Reels (FR0)")
    free_reels = generate_reel_strip(FREE_SYMBOLS, NUM_REELS, REEL_LENGTH, seed=34567)
    write_reel_csv(free_reels, "FR0.csv")
    print()
    
    # Win cap reels
    print("4. Win Cap Reels (WCAP)")
    wcap_reels = generate_reel_strip(WCAP_SYMBOLS, NUM_REELS, REEL_LENGTH, seed=45678)
    write_reel_csv(wcap_reels, "WCAP.csv")
    print()
    
    print("="*60)
    print("Reel generation complete!")
    print("These reels are designed to achieve ~96% RTP with:")
    print("- Better symbol distribution")
    print("- Increased scatter frequency")
    print("- Multiplier bombs in free spins")
    print("- 250 rows per reel (vs previous 50)")
    print("="*60)


if __name__ == "__main__":
    main()
