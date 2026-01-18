"""Minimal test run for Sweet Bonanza Clone."""
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

    # Very minimal simulations for testing
    num_sim_args = {
        "base": 100,
    }

    config = GameConfig()
    gamestate = GameState(config)

    print("\n=== Running Minimal Test Simulations ===")
    create_books(
        gamestate,
        config,
        num_sim_args,
        batching_size,
        num_threads,
        compression,
        profiling,
    )
    
    print("\n=== Test Complete ===")
    print(f"Output files created in: {config.game_path}/outputs/")
