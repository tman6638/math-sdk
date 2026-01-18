import sys
sys.path.insert(0, '/home/runner/work/math-sdk/math-sdk')

from gamestate import GameState
from game_config import GameConfig

if __name__ == "__main__":
    # Initialize
    config = GameConfig()
    gamestate = GameState(config)
    
    # Test freegame criteria (should force bonus)
    gamestate.betmode = "base"
    gamestate.criteria = "freegame"
    
    print('Testing bonus trigger simulation...')
    try:
        gamestate.run_spin(0)
        print(f'Spin completed successfully!')
        print(f'Final win: {gamestate.final_win}')
        print(f'Bonus triggered: {gamestate.win_manager.cumulative_free_wins > 0}')
    except Exception as e:
        print(f'Error during spin: {e}')
        import traceback
        traceback.print_exc()
