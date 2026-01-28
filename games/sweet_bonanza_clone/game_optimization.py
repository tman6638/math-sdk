"""Sweet Bonanza Clone optimization parameters"""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructFenceBias,
    ConstructConditions,
    verify_optimization_input,
)


class OptimizationSetup:
    """Handle all game mode optimization parameters for Sweet Bonanza Clone."""

    def __init__(self, game_config):
        self.game_config = game_config
        self.game_config.opt_params = {
            # Base mode - standard bet with natural bonus trigger
            "base": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.01,
                        av_win=5000,
                        search_conditions=5000
                    ).return_dict(),
                    "0": ConstructConditions(
                        rtp=0,
                        av_win=0,
                        search_conditions=0
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.40,
                        hr=200,
                        search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    "basegame": ConstructConditions(
                        hr=3.5,
                        rtp=0.55
                    ).return_dict(),
                },
                "scaling": ConstructScaling([
                    {
                        "criteria": "basegame",
                        "scale_factor": 1.2,
                        "win_range": (1, 2),
                        "probability": 1.0,
                    },
                    {
                        "criteria": "basegame",
                        "scale_factor": 1.5,
                        "win_range": (10, 20),
                        "probability": 1.0,
                    },
                    {
                        "criteria": "freegame",
                        "scale_factor": 0.8,
                        "win_range": (1000, 2000),
                        "probability": 1.0,
                    },
                    {
                        "criteria": "freegame",
                        "scale_factor": 1.2,
                        "win_range": (3000, 4000),
                        "probability": 1.0,
                    },
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
                    bias_ranges=[(3.0, 5.0)],
                    bias_weights=[0.5],
                ).return_dict(),
            },
            
            # Ante mode - increased scatter frequency
            "ante": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.01,
                        av_win=5000,
                        search_conditions=5000
                    ).return_dict(),
                    "0": ConstructConditions(
                        rtp=0,
                        av_win=0,
                        search_conditions=0
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.45,
                        hr=150,  # Higher bonus hit rate
                        search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    "basegame": ConstructConditions(
                        hr=3.5,
                        rtp=0.50
                    ).return_dict(),
                },
                "scaling": ConstructScaling([
                    {
                        "criteria": "basegame",
                        "scale_factor": 1.2,
                        "win_range": (1, 2),
                        "probability": 1.0,
                    },
                    {
                        "criteria": "freegame",
                        "scale_factor": 0.8,
                        "win_range": (1000, 2000),
                        "probability": 1.0,
                    },
                    {
                        "criteria": "freegame",
                        "scale_factor": 1.2,
                        "win_range": (3000, 4000),
                        "probability": 1.0,
                    },
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
                    bias_ranges=[(3.0, 5.0)],
                    bias_weights=[0.5],
                ).return_dict(),
            },
            
            # Bonus buy mode - 100x cost, standard multipliers
            "bonus_buy": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.01,
                        av_win=5000,
                        search_conditions=5000
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.96,
                        hr="x"
                    ).return_dict(),
                },
                "scaling": ConstructScaling([
                    {
                        "criteria": "freegame",
                        "scale_factor": 1.2,
                        "win_range": (3000, 4000),
                        "probability": 1.0,
                    },
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                    max_trial_dist=15,
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["freegame"],
                    bias_ranges=[(90.0, 150.0)],
                    bias_weights=[0.1],
                ).return_dict(),
            },
            
            # Super bonus mode - 500x cost, high multipliers only
            "super_bonus": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.01,
                        av_win=5000,
                        search_conditions=5000
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.96,
                        hr="x"
                    ).return_dict(),
                },
                "scaling": ConstructScaling([
                    {
                        "criteria": "freegame",
                        "scale_factor": 1.3,
                        "win_range": (3000, 4500),
                        "probability": 1.0,
                    },
                    {
                        "criteria": "freegame",
                        "scale_factor": 0.7,
                        "win_range": (500, 1000),
                        "probability": 1.0,
                    },
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                    max_trial_dist=15,
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["freegame"],
                    bias_ranges=[(200.0, 400.0)],
                    bias_weights=[0.15],
                ).return_dict(),
            },
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
