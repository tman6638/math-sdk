"""Set conditions/parameters for optimization program."""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructFenceBias,
    ConstructConditions,
    verify_optimization_input,
)


class OptimizationSetup:
    """Handle all game mode optimization parameters for Spy Bonanza."""

    def __init__(self, game_config):
        self.game_config = game_config
        self.game_config.opt_params = {
            "base": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, av_win=10000, search_conditions=10000).return_dict(),
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.30, hr=150, search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    "ultra_freegame": ConstructConditions(
                        rtp=0.10, hr=400, search_conditions={"symbol": "ultra_scatter"}
                    ).return_dict(),
                    "basegame": ConstructConditions(hr=3.0, rtp=0.55).return_dict(),
                },
                "scaling": ConstructScaling([
                    {"criteria": "basegame", "scale_factor": 1.2, "win_range": (1, 3), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 1.4, "win_range": (15, 30), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 0.9, "win_range": (500, 1000), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 1.1, "win_range": (2000, 4000), "probability": 1.0},
                    {"criteria": "ultra_freegame", "scale_factor": 0.85, "win_range": (1000, 2000), "probability": 1.0},
                    {"criteria": "ultra_freegame", "scale_factor": 1.15, "win_range": (4000, 8000), "probability": 1.0},
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[50, 100, 200],
                    test_weights=[0.3, 0.4, 0.3],
                    score_type="rtp",
                    max_trial_dist=15,
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["basegame"],
                    bias_ranges=[(2.5, 5.0)],
                    bias_weights=[0.5],
                ).return_dict(),
            },
            "bonus": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, av_win=10000, search_conditions=10000).return_dict(),
                    "freegame": ConstructConditions(rtp=0.95, hr="x").return_dict(),
                },
                "scaling": ConstructScaling([
                    {"criteria": "freegame", "scale_factor": 1.1, "win_range": (2000, 4000), "probability": 1.0},
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.5, 0.3, 0.2],
                    score_type="rtp",
                    max_trial_dist=15,
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["freegame"],
                    bias_ranges=[(80.0, 120.0)],
                    bias_weights=[0.15],
                ).return_dict(),
            },
            "ultra_bonus": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, av_win=10000, search_conditions=10000).return_dict(),
                    "ultra_freegame": ConstructConditions(rtp=0.95, hr="x").return_dict(),
                },
                "scaling": ConstructScaling([
                    {"criteria": "ultra_freegame", "scale_factor": 1.1, "win_range": (3000, 6000), "probability": 1.0},
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.5, 0.3, 0.2],
                    score_type="rtp",
                    max_trial_dist=15,
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["ultra_freegame"],
                    bias_ranges=[(300.0, 450.0)],
                    bias_weights=[0.1],
                ).return_dict(),
            },
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)