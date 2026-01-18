"""Test multiple bonus buy simulations."""
import sys
sys.path.insert(0, '/home/runner/work/math-sdk/math-sdk')

from gamestate import GameState
from game_config import GameConfig

if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)
    
    # Set betmode and criteria
    gamestate.betmode = "bonus_buy"
    gamestate.criteria = "freegame"
    
    print('Testing multiple bonus buy simulations...')
    for i in range(5):
        try:
            gamestate.run_spin(i)
            print(f'Sim {i}: Final win={gamestate.final_win}, base={gamestate.win_manager.basegame_wins}, free={gamestate.win_manager.freegame_wins}')
        except AssertionError as e:
            print(f'Sim {i}: Assertion failed!')
            print(f'  Base game wins: {gamestate.win_manager.basegame_wins}')
            print(f'  Free game wins: {gamestate.win_manager.freegame_wins}')
            print(f'  Running bet win: {gamestate.win_manager.running_bet_win}')
            print(f'  Sum: {gamestate.win_manager.basegame_wins + gamestate.win_manager.freegame_wins}')
            break
        except Exception as e:
            print(f'Sim {i}: Error: {e}')
            import traceback
            traceback.print_exc()
            break
