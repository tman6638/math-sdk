#!/usr/bin/env python3
"""Quick test to verify new reels produce better RTP"""

from games.sweet_bonanza_clone.gamestate import GameState
from games.sweet_bonanza_clone.game_config import GameConfig
from src.state.run_sims import create_books

if __name__ == "__main__":
    # Test with 1000 simulations first
    num_sim_args = {
        "base": 1000,
        "ante": 1000,
        "bonus_buy": 1000,
        "super_bonus": 1000,
    }
    
    config = GameConfig()
    gamestate = GameState(config)
    
    print("Testing new reel strips with 1000 simulations...")
    print("=" * 60)
    
    create_books(
        gamestate,
        config,
        num_sim_args,
        batching_size=1000,
        num_threads=4,
        compression=False,
        profiling=False,
    )
    
    print("\n" + "=" * 60)
    print("Test complete! Check RTP values in output.")
    print("If RTP is closer to 96%, we can run full simulations.")
