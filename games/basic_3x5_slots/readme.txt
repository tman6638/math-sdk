# Basic 3x5 Slots Game

This is a basic 3x5 slot game with 20 paylines and a free spin feature.

## Game Specifications
- **Grid Size**: 3 rows × 5 reels
- **Game ID**: basic_3x5_slots
- **Win Type**: lines (payline-based wins)
- **RTP**: 97%
- **Max Win (Wincap)**: 5000x
- **Paylines**: 20 standard line patterns

## Symbols and Paytable
### High Value Symbols
- H1: 50x (5-of-a-kind), 20x (4-of-a-kind), 10x (3-of-a-kind)
- H2: 15x (5-of-a-kind), 5x (4-of-a-kind), 3x (3-of-a-kind)
- H3: 10x (5-of-a-kind), 3x (4-of-a-kind), 2x (3-of-a-kind)
- H4: 8x (5-of-a-kind), 2x (4-of-a-kind), 1x (3-of-a-kind)

### Low Value Symbols
- L1: 5x (5-of-a-kind), 1x (4-of-a-kind), 0.5x (3-of-a-kind)
- L2: 3x (5-of-a-kind), 0.7x (4-of-a-kind), 0.3x (3-of-a-kind)
- L3: 3x (5-of-a-kind), 0.7x (4-of-a-kind), 0.3x (3-of-a-kind)
- L4: 2x (5-of-a-kind), 0.5x (4-of-a-kind), 0.2x (3-of-a-kind)

### Special Symbols
- **W (Wild)**: Substitutes for all symbols except Scatter, pays same as H1
- **S (Scatter)**: Triggers free spins (3=8FS, 4=12FS, 5=15FS)

## Base Game
Scatter Symbols appear on all reels. A minimum of 3 Scatters are needed to trigger the free game.

## Free Spin Feature
- Triggered by 3+ Scatter symbols
- Base game triggers: 3S=8FS, 4S=12FS, 5S=15FS
- Free game retriggers: 2S=3FS, 3S=5FS, 4S=8FS, 5S=12FS
- Wild multipliers in free spins: 2x, 3x, 4x, 5x, 10x, 20x, 50x
- A separate reel strip is used for the free game
- Wilds have larger multipliers (minimum of 2x) and appear on all reels
- 2 Scatters are needed to trigger extra spins, appearing only on reels 2, 3, 4

## Bet Modes
- **base**: Standard play (cost: 1.0x, feature: true, buybonus: false)
- **bonus**: Buy bonus (cost: 100.0x, feature: false, buybonus: true)

## Notes
Wilds pay on 5-Kind only by default. If the paytable includes 3/4 Kind Wild pays, the line
calculation will assign the highest base-win symbols as winning. For example, if there is a 3-Kind
Wild on the same line as a 5-Kind L4, the 3-Kind Wild will be chosen, regardless of the multiplier
on the final Wild since the base payout 3W > 5L4.
