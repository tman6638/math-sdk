#!/usr/bin/env python3
"""
Generate balanced reel strips for Sweet Bonanza Clone to achieve 96.4% RTP.

Key requirements:
- 8-symbol minimum for wins
- All 8 paying symbols used (not concentrated)
- 10,000x max win
- 96.4% target RTP
"""

import random
import csv
from pathlib import Path

# Configuration
REEL_LENGTH = 250
NUM_REELS = 6

# Base game - ALL 8 symbols active, balanced distribution
# For 8-symbol minimum with 30 positions, need 12-14% per symbol
# This gives expected 3.6-4.2 instances per spin
BASE_SYMBOLS = {
    # High pays (4 symbols)
    'H1': 28,   # 11.2% -> ~3.4 per spin
    'H2': 30,   # 12.0% -> ~3.6 per spin
    'H3': 32,   # 12.8% -> ~3.8 per spin
    'H4': 34,   # 13.6% -> ~4.1 per spin
    # Low pays (4 symbols)
    'L1': 32,   # 12.8% -> ~3.8 per spin
    'L2': 34,   # 13.6% -> ~4.1 per spin
    'L3': 36,   # 14.4% -> ~4.3 per spin
    'L4': 38,   # 15.2% -> ~4.6 per spin (highest - most common low)
    # Specials
    'S': 15,    # 6.0% -> ~1.8 per spin (need 4 for trigger)
    'W': 10,    # 4.0% -> ~1.2 per spin (wild helps)
}

# Ante game - higher scatter frequency only
ANTE_SYMBOLS = {
    'H1': 28,
    'H2': 30,
    'H3': 32,
    'H4': 34,
    'L1': 32,
    'L2': 34,
    'L3': 36,
    'L4': 38,
    'S': 25,    # 10.0% -> ~3.0 per spin (2x scatter chance)
    'W': 10,
}

# Free spins - all symbols plus multiplier bombs
FREE_SYMBOLS = {
    'H1': 32,   # Slightly higher in free spins
    'H2': 34,
    'H3': 36,
    'H4': 38,
    'L1': 36,
    'L2': 38,
    'L3': 40,
    'L4': 42,
    'S': 12,    # Scatters for retrigger
    'W': 15,    # More wilds in free spins
    'M': 30,    # 12% multiplier bombs for big wins
}

# Win cap - high concentration of high-paying symbols
WCAP_SYMBOLS = {
    'H1': 80,   # Force high pays
    'H2': 75,
    'H3': 70,
    'H4': 65,
    'L1': 20,
    'L2': 15,
    'L3': 10,
    'L4': 10,
    'S': 5,
    'W': 5,
}


def generate_reel_strip(symbols_config, num_reels, reel_length, seed=None):
    """Generate a balanced reel strip with good distribution"""
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
        
        # For scatter distribution, place them strategically
        scatter_positions = set()
        if symbols_config.get('S', 0) > 0:
            # Calculate how many scatters per reel based on frequency
            total_weight = sum(symbols_config.values())
            scatter_freq = symbols_config['S'] / total_weight
            num_scatters = int(reel_length * scatter_freq)
            
            # Distribute evenly across reel
            step = reel_length // (num_scatters + 1) if num_scatters > 0 else reel_length
            for i in range(num_scatters):
                pos = (i + 1) * step + random.randint(-3, 3)
                pos = max(0, min(reel_length - 1, pos))
                scatter_positions.add(pos)
        
        for row_idx in range(reel_length):
            # Place scatter at strategic position
            if row_idx in scatter_positions:
                reel.append('S')
            else:
                # Pick random symbol from pool (excluding scatter for this position)
                non_scatter_pool = [s for s in symbol_pool if s != 'S']
                reel.append(random.choice(non_scatter_pool))
        
        reels.append(reel)
    
    return reels


def save_reel_strip(reels, filename):
    """Save reel strip to CSV file"""
    filepath = Path(__file__).parent / 'reels' / filename
    filepath.parent.mkdir(exist_ok=True)
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        for row_idx in range(len(reels[0])):
            row = [reels[reel_idx][row_idx] for reel_idx in range(len(reels))]
            writer.writerow(row)
    
    print(f"Generated {filename} with {len(reels[0])} rows x {len(reels)} reels")


def main():
    """Generate all reel strips"""
    print("Generating balanced reel strips for 96.4% RTP target...")
    print(f"Reel configuration: {REEL_LENGTH} rows x {NUM_REELS} reels\n")
    
    # Generate each reel set with different seeds for variety
    reels_br0 = generate_reel_strip(BASE_SYMBOLS, NUM_REELS, REEL_LENGTH, seed=42)
    save_reel_strip(reels_br0, 'BR0.csv')
    
    reels_ar0 = generate_reel_strip(ANTE_SYMBOLS, NUM_REELS, REEL_LENGTH, seed=43)
    save_reel_strip(reels_ar0, 'AR0.csv')
    
    reels_fr0 = generate_reel_strip(FREE_SYMBOLS, NUM_REELS, REEL_LENGTH, seed=44)
    save_reel_strip(reels_fr0, 'FR0.csv')
    
    reels_wcap = generate_reel_strip(WCAP_SYMBOLS, NUM_REELS, REEL_LENGTH, seed=45)
    save_reel_strip(reels_wcap, 'WCAP.csv')
    
    print("\n✓ All reel strips generated successfully!")
    print("\nSymbol distribution summary:")
    print("  Base game: All 8 symbols (11-15% each), Scatter 6%, Wild 4%")
    print("  Ante game: All 8 symbols, Scatter 10% (increased bonus chance)")
    print("  Free spins: All 8 symbols + 12% Multiplier bombs")
    print("  Expected: ~1.8 scatters/spin base, ~3.0 scatters/spin ante")


if __name__ == "__main__":
    main()
