# Stake Engine Upload Files - Sweet Bonanza Clone

This directory contains all the files needed to upload the Sweet Bonanza Clone game to Stake Engine.

## Files to Upload (All 9 files)

Upload the following files to Stake Engine under the **math files** section:

### 1. Index File (Required)
- **`index.json`** - Main configuration that references all bet modes and their files

### 2. Lookup Tables (4 files - Required)
- **`lookUpTable_base_0.csv`** - Symbol distribution weights for base mode (1x bet)
- **`lookUpTable_ante_0.csv`** - Symbol distribution weights for ante mode (1.25x bet)
- **`lookUpTable_bonus_buy_0.csv`** - Symbol distribution weights for bonus buy mode (100x bet)
- **`lookUpTable_super_bonus_0.csv`** - Symbol distribution weights for super bonus mode (500x bet)

### 3. Game Logic Files (4 files - Required)
- **`books_base.jsonl.zst`** - Compressed game events for base mode
- **`books_ante.jsonl.zst`** - Compressed game events for ante mode
- **`books_bonus_buy.jsonl.zst`** - Compressed game events for bonus buy mode
- **`books_super_bonus.jsonl.zst`** - Compressed game events for super bonus mode

## File Details

| File | Size | Description |
|------|------|-------------|
| `index.json` | 736 B | Bet mode configuration |
| `lookUpTable_base_0.csv` | 7.8 KB | Base mode weights |
| `lookUpTable_ante_0.csv` | 7.8 KB | Ante mode weights |
| `lookUpTable_bonus_buy_0.csv` | 8.1 KB | Bonus buy weights |
| `lookUpTable_super_bonus_0.csv` | 8.2 KB | Super bonus weights |
| `books_base.jsonl.zst` | 58 KB | Base mode events (1000 rounds) |
| `books_ante.jsonl.zst` | 61 KB | Ante mode events (1000 rounds) |
| `books_bonus_buy.jsonl.zst` | 654 KB | Bonus buy events (1000 rounds) |
| `books_super_bonus.jsonl.zst` | 658 KB | Super bonus events (1000 rounds) |

**Total Size:** ~1.5 MB

## Upload Instructions

1. Navigate to Stake Engine's game management interface
2. Select "Upload Math Files" or equivalent section
3. Select the directory containing these files OR upload all 9 files individually
4. Ensure all files are uploaded together in the same upload session
5. Stake Engine will validate the files and show a summary of:
   - Game modes detected
   - RTP calculations
   - Symbol distributions
   - Payout analysis

## Bet Mode Configuration

The game includes 4 bet modes as defined in `index.json`:

| Mode | Cost | Type | Description |
|------|------|------|-------------|
| `base` | 1.0x | Natural play | Standard gameplay with natural bonus triggers |
| `ante` | 1.25x | Natural play | Enhanced scatter frequency (2x bonus chance) |
| `bonus_buy` | 100x | Feature buy | Direct entry to 10 free spins |
| `super_bonus` | 500x | Feature buy | Direct entry to 10 free spins with high multipliers |

## Game Specifications

- **Game Type:** 6x5 scatter-pay slot with tumbling mechanics
- **Symbols:** 10 total (H1-H4, L1-L4, S scatter, W wild, M multiplier bomb)
- **Win Evaluation:** Scatter pays (8+ matching symbols anywhere)
- **Special Features:**
  - Tumbling/cascading wins
  - Multiplier bombs (bonus only) that ADD together
  - Free spin bonus with retriggering (3+ scatters = +5 spins)
  - Win cap at 5000x
- **Target RTP:** 96% (all modes)

## Verification

After upload, verify that Stake Engine shows:
- 4 bet modes correctly configured
- All lookup tables and event files linked properly
- RTP calculations for each mode
- No validation errors

## Support Files

The following files are in this directory but **NOT required** for upload:
- `README_UPLOAD.md` - This file (instructions only)
- `convert_and_compress.py` - Script used to generate the compressed files (in parent directory)

## Regenerating Files

If you need to regenerate the compressed book files:

```bash
cd /path/to/sweet_bonanza_clone
python3 convert_and_compress.py
```

This will re-compress the JSON books from `library/books/` directory.

---

**Ready to Upload!** All files in this directory are properly formatted and compressed for Stake Engine deployment.
