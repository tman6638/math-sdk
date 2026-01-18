"""Test run with minimal simulations for all bet modes."""
import sys
sys.path.insert(0, '/home/runner/work/math-sdk/math-sdk')

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    num_threads = 1
    batching_size = 100
    compression = False
    profiling = False

    # Minimal simulations for testing all modes
    num_sim_args = {
        "base": 100,
        "ante": 100,
        "bonus_buy": 100,
        "super_bonus": 100,
    }

    config = GameConfig()
    gamestate = GameState(config)

    print("\n=== Running Test Simulations for All Bet Modes ===")
    create_books(
        gamestate,
        config,
        num_sim_args,
        batching_size,
        num_threads,
        compression,
        profiling,
    )
    
    print("\n=== Generating Config Files ===")
    generate_configs(gamestate)
    
    print("\n=== Test Complete ===")
