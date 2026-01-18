"""Test simulation with multiprocessing fix"""
import sys
sys.path.insert(0, '/home/runner/work/math-sdk/math-sdk')

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books

# Small test
num_sim_args = {'base': 100}

config = GameConfig()
gamestate = GameState(config)

print('Starting 100 simulations for base mode...')
print('Reels loaded:', list(config.reels.keys()))

try:
    create_books(
        gamestate,
        config,
        num_sim_args,
        100,  # batch_size
        4,    # num_threads
        False,  # compression
        False,  # profiling
    )
    print('\n✅ SUCCESS! Simulations completed.')
    
    # Check if books were created
    import os
    books_path = os.path.join(config.library_path, 'books', 'books_base.json')
    if os.path.exists(books_path):
        print(f'✅ Books file created: {books_path}')
        
        # Read and show some stats
        import json
        with open(books_path, 'r') as f:
            data = json.load(f)
            print(f'   Total spins: {len(data)}')
            
            # Calculate basic RTP
            total_bet = len(data)
            total_win = sum(spin.get('totalWin', 0) for spin in data)
            rtp = (total_win / total_bet * 100) if total_bet > 0 else 0
            print(f'   Total bet: {total_bet}')
            print(f'   Total win: {total_win:.2f}')
            print(f'   RTP: {rtp:.2f}%')
            
            # Count wins > 0
            wins = [s for s in data if s.get('totalWin', 0) > 0]
            print(f'   Winning spins: {len(wins)} ({len(wins)/len(data)*100:.1f}%)')
            
    else:
        print(f'⚠️  Books file not found at {books_path}')
        
except Exception as e:
    print(f'\n❌ ERROR: {e}')
    import traceback
    traceback.print_exc()
