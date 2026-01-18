# Sweet Bonanza Clone - Installation & Usage Guide

## Requirements

This game requires Python 3.8+ and the following dependencies:

```bash
pip install numpy xlsxwriter zstandard toml matplotlib
```

Or install all requirements from the repository root:

```bash
cd /path/to/math-sdk
pip install -r requirements.txt
```

## Running the Game

### Option 1: Run from Game Directory (Recommended)

The game now includes automatic path setup, so you can run it from the game directory:

```bash
cd games/sweet_bonanza_clone
python run.py
```

### Option 2: Run from Repository Root

Alternatively, you can run from the repository root:

```bash
cd /path/to/math-sdk
python -m games.sweet_bonanza_clone.run
```

## Configuration

Edit `run.py` to configure simulations:

```python
# Number of simulations per bet mode
num_sim_args = {
    "base": 100000,        # Base game simulations
    "ante": 100000,        # Ante bet simulations
    "bonus_buy": 100000,   # Bonus buy simulations
    "super_bonus": 100000, # Super bonus simulations
}

# Execution parameters
num_threads = 10          # Number of parallel threads
batch_size = 10000        # Simulations per batch
```

## Expected Runtime

- **100 simulations per mode**: ~10 seconds (quick test)
- **1,000 simulations per mode**: ~1 minute
- **10,000 simulations per mode**: ~10 minutes
- **100,000 simulations per mode**: ~30-60 minutes

Total of 400,000 simulations (100K per mode) takes approximately 30-60 minutes depending on CPU.

## Output Files

After running simulations, output files will be generated in:

```
games/sweet_bonanza_clone/library/
├── books/               # Simulation data (JSON)
├── configs/             # Event configurations
├── forces/              # Force file configurations
├── lookup_tables/       # Symbol distribution weights
└── publish_files/       # Files ready for Stake Engine upload
```

## Generating Stake Engine Upload Files

After simulations complete, compress the results:

```bash
python convert_and_compress.py
```

This creates 9 files in `library/publish_files/` ready for upload to Stake Engine:
1. `index.json` - Bet mode configuration
2-5. `lookUpTable_*.csv` - Distribution weights (4 files)
6-9. `books_*.jsonl.zst` - Compressed event files (4 files)

## Game Configuration

- **RTP Target**: 96.4%
- **Max Win**: 10,000x
- **Grid Size**: 6 reels × 5 rows (30 positions)
- **Paytable**: 8-symbol minimum for wins
- **Tumbling**: Max 50 cascades per spin

## Troubleshooting

### Import Error: No module named 'src'

The game requires the repository root to be in Python's path. The updated `run.py` handles this automatically. If you still see this error:

1. Ensure you're running from the game directory
2. Check that the repository structure is intact
3. Verify `sys.path` includes the repository root

### Import Error: No module named 'numpy'

Install the required dependencies:

```bash
pip install numpy xlsxwriter zstandard toml matplotlib
```

### Low RTP in Test Runs

Small sample sizes (< 1,000 simulations) will show high variance. Run at least 10,000 simulations per mode for reliable RTP estimates. The target 96.4% RTP requires 100,000+ simulations to converge.

### Memory Issues

If running out of memory with 100K simulations:
1. Reduce `num_threads` to 4 or 2
2. Reduce `batch_size` to 5,000
3. Run modes separately by commenting out modes in `num_sim_args`

## Testing Before Full Run

To test that everything works before running the full 400K simulations:

Edit `run.py` and temporarily change:

```python
num_sim_args = {
    "base": 100,
    "ante": 100,
    "bonus_buy": 100,
    "super_bonus": 100,
}
```

Run the test (takes ~10 seconds), then increase back to 100,000 for production runs.

## Validation

After running simulations, check the RTP values in the output:

```
Thread X finished with Y.ZZ RTP. [baseGame: A.AA, freeGame: B.BB]
```

Expected ranges for 100K simulations:
- **Base game**: 94-98% RTP
- **Ante game**: 94-98% RTP  
- **Bonus buy**: 94-98% RTP
- **Super bonus**: 94-98% RTP

The average should converge to approximately 96.4% ± 2%.

## Support

For issues specific to the Sweet Bonanza Clone implementation, check:
- `readme.txt` - Game rules and mechanics
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- Repository issues: https://github.com/tman6638/math-sdk/issues
