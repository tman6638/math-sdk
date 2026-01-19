"""Main execution script for Sweet Bonanza Clone game."""
import sys
import os

# Add repository root to path to enable src imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from gamestate import GameState
from game_config import GameConfig
# from game_optimization import OptimizationSetup  # Commented out - version incompatibility
# from optimization_program.run_script import OptimizationExecution
# from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":

    # Execution parameters
    num_threads = 10
    rust_threads = 20
    batch_size = 10000
    compression = True
    profiling = False

    # Number of simulations per bet mode
    # Run comprehensive tests to achieve 96.4% RTP target
    num_sim_args = {
        "base": 100000,
        "ante": 100000,
        "bonus_buy": 100000,
        "super_bonus": 100000,
    }

    # Control which steps to run
    run_conditions = {
        "run_sims": True,
        "run_optimization": False,  # Skip for now
        "run_analysis": False,  # Skip for now
        "run_format_checks": True,  # Enable to catch payout mismatches
    }
    
    # Target bet modes to process
    target_modes = ["base", "ante", "bonus_buy", "super_bonus"]

    # Initialize game configuration and state
    config = GameConfig()
    gamestate = GameState(config)
    
    # if run_conditions["run_optimization"] or run_conditions["run_analysis"]:
    #     optimization_setup_class = OptimizationSetup(config)

    # Step 1: Run simulations to generate books
    if run_conditions["run_sims"]:
        print("\n=== Running Simulations ===")
        create_books(
            gamestate,
            config,
            num_sim_args,
            batch_size,
            num_threads,
            compression,
            profiling,
        )

    # Generate configuration files
    generate_configs(gamestate)

    # Step 2: Run optimization
    # if run_conditions["run_optimization"]:
    #     print("\n=== Running Optimization ===")
    #     OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
    #     generate_configs(gamestate)

    # Step 3: Run analysis
    # if run_conditions["run_analysis"]:
    #     print("\n=== Running Analysis ===")
    #     custom_keys = [{"symbol": "scatter"}, {"symbol": "multiplier"}]
    #     create_stat_sheet(gamestate, custom_keys=custom_keys)

    # Step 4: Run format checks/verification
    if run_conditions["run_format_checks"]:
        print("\n=== Running Format Checks ===")
        execute_all_tests(config)

    print("\n=== Sweet Bonanza Clone - Execution Complete ===")
    print(f"Output files (books and lookup tables) can be found in: {config.publish_path}")
