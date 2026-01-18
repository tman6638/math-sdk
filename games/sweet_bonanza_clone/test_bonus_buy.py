"""Test bonus buy mode specifically."""
import sys
sys.path.insert(0, '/home/runner/work/math-sdk/math-sdk')

from gamestate import GameState
from game_config import GameConfig

if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)
    
    # Set betmode and criteria manually for testing
    gamestate.betmode = "bonus_buy"
    gamestate.criteria = "freegame"
    
    print('Testing bonus buy simulation...')
    try:
        gamestate.run_spin(0)
        print(f'Spin completed successfully!')
        print(f'Final win: {gamestate.final_win}')
        print(f'Base game wins: {gamestate.win_manager.basegame_wins}')
        print(f'Free game wins: {gamestate.win_manager.freegame_wins}')
        print(f'Running bet win: {gamestate.win_manager.running_bet_win}')
        print(f'Book basegame wins: {gamestate.book.basegame_wins}')
        print(f'Book freegame wins: {gamestate.book.freegame_wins}')
        print(f'Book payout: {gamestate.book.payout_multiplier}')
    except Exception as e:
        print(f'Error during spin: {e}')
        import traceback
        traceback.print_exc()
