# Sweet Bonanza Clone - Tumbling Slot Game

## Summary

A 6-reel, 5-row tumbling (cascading) slot game with scatter pays, multiplier bombs, and multiple bonus buy options.

## Game Configuration

* **Grid Size**: 6 reels × 5 rows (30 total positions)
* **Win Type**: Scatter pays (pay anywhere) - symbols pay based on count anywhere on the board
* **Win Cap**: 5000x
* **Symbols**: 10 total
  - High Pays (H1-H4): Premium candy-style symbols
  - Low Pays (L1-L4): Standard fruit symbols
  - Scatter (S): Lollipop - 4+ triggers bonus
  - Wild (W): Substitutes for all paying symbols
  - Multiplier (M): Bonus-only multiplier bomb

## Paytable Structure

Scatter-pay groupings (in bet multipliers):
* **H1**: 8-9=10x, 10-11=25x, 12-14=50x, 15+=500x
* **H2**: 8-9=8x, 10-11=20x, 12-14=40x, 15+=250x
* **H3**: 8-9=5x, 10-11=15x, 12-14=30x, 15+=150x
* **H4**: 8-9=4x, 10-11=10x, 12-14=20x, 15+=100x
* **L1**: 8-9=2.5x, 10-11=5x, 12-14=10x, 15+=50x
* **L2**: 8-9=2x, 10-11=4x, 12-14=8x, 15+=40x
* **L3**: 8-9=1.5x, 10-11=3x, 12-14=6x, 15+=30x
* **L4**: 8-9=1x, 10-11=2x, 12-14=4x, 15+=20x

**Scatter Payouts**:
* 4 scatters: 3x bet + 10 free spins
* 5 scatters: 5x bet + 10 free spins
* 6 scatters: 100x bet + 10 free spins

## Bet Modes

### 1. Base Mode (`base`)
* Standard 1x bet
* 4+ scatters trigger bonus naturally
* No multiplier bombs in base game
* Target RTP: ~96%

### 2. Ante Bet Mode (`ante`)
* Costs 1.25x the base bet
* Increased scatter frequency (roughly 2x higher chance of bonus trigger)
* Same bonus rules as base
* Target RTP: ~96%

### 3. Bonus Buy Mode (`bonus_buy`)
* Costs 100x the base bet
* Immediately enters free spins bonus
* Standard multiplier bomb values: 2x, 3x, 4x, 5x, 6x, 8x, 10x, 12x, 15x, 20x, 25x, 50x, 100x
* 10 free spins awarded
* Target RTP: ~96%

### 4. Super Bonus Buy Mode (`super_bonus`)
* Costs 500x the base bet
* Immediately enters free spins bonus
* High multipliers ONLY: 10x, 12x, 15x, 20x, 25x, 50x, 75x, 100x, 250x, 500x
* 10 free spins awarded
* Higher volatility
* Target RTP: ~96%

## Base Game Mechanics

1. **Initial Spin**: Board is populated with symbols from base game reel strips
2. **Win Evaluation**: Check for scatter pays (8+ matching symbols anywhere)
3. **Tumble/Cascade**: Winning symbols explode and new symbols fall from above
4. **Repeat**: Continue tumbling until no more wins
5. **Bonus Trigger**: 4+ scatter symbols trigger free spins

## Free Spins Bonus Mechanics

1. **Entry**: 
   - 4+ scatters in base/ante mode
   - Via bonus buy (bonus_buy or super_bonus modes)
   
2. **Free Spins**: 
   - 10 spins awarded initially
   - Can retrigger with 3+ scatters for +5 spins each time
   
3. **Multiplier Bombs**: 
   - Random multipliers (M symbols) appear on the board during bonus
   - Multipliers are collected when ANY win occurs on that tumble
   - All collected multipliers ADD together and apply to the tumble win
   - Multiplier bombs do NOT explode - they stay until end of spin
   - Collected multipliers reset at the start of each new free spin
   
4. **Tumbling**: Continues until no more wins on current spin

## Multiplier Distribution

### Standard Bonus (base/ante/bonus_buy):
* 2x: 30%
* 3x: 20%
* 4x: 15%
* 5x: 12%
* 6x: 8%
* 8x: 5%
* 10x: 4%
* 12x: 2.5%
* 15x: 1.5%
* 20x: 1%
* 25x: 0.5%
* 50x: 0.3%
* 100x: 0.2%

### Super Bonus (super_bonus):
* 10x: 35%
* 12x: 20%
* 15x: 15%
* 20x: 10%
* 25x: 8%
* 50x: 6%
* 75x: 3%
* 100x: 2%
* 250x: 0.8%
* 500x: 0.2%

## Key Events

* `reveal` - Board shown to player
* `winInfo` - Win details with symbol positions and payouts
* `tumble` - Symbols removed and new ones fall
* `multiplierCollect` - Multipliers collected this tumble (bonus only)
* `setWin` - Spin total win (after all tumbles complete)
* `setTotalWin` - Round total (cumulative in bonus)
* `fsTrigger` - Bonus triggered
* `fsUpdate` - Free spin counter update
* `bonusComplete` - Bonus round finished

## Notes

* The tumble mechanic allows for multiple wins from a single spin
* Multiplier bombs only appear in free spins bonus
* Multipliers accumulate during tumbles but reset between spins
* Win cap is applied to prevent payouts exceeding 5000x bet
