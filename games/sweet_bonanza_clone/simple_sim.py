"""Simple simulation test without optimization."""
import sys
sys.path.insert(0, '/home/runner/work/math-sdk/math-sdk')

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books

if __name__ == "__main__":
    num_threads = 1
    batching_size = 100
    compression = False
    profiling = False

    # Only test basegame criteria to avoid forced conditions
    num_sim_args = {
        "base": 100,
    }

    config = GameConfig()
    
    # Simplify distributions to avoid forced conditions
    # Keep only the basegame distribution
    base_mode = config.bet_modes[0]
    from src.config.distributions import Distribution
    base_mode._distributions = [
        Distribution(
            criteria="basegame",
            quota=1.0,
            conditions={
                "reel_weights": {config.basegame_type: {"BR0": 1}},
                "mult_values": {config.basegame_type: {1: 1}},
                "force_wincap": False,
                "force_freegame": False,
            },
        ),
    ]
    
    gamestate = GameState(config)

    print("\n=== Running Simple Simulations ===")
    try:
        create_books(
            gamestate,
            config,
            num_sim_args,
            batching_size,
            num_threads,
            compression,
            profiling,
        )
        print("\n=== Simulation Complete ===")
        print(f"Output files created in: {config.game_path}/outputs/")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
