import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    """Spy Bonanza - 6x5 tumbling scatter-pay game with regular and ultra bonus modes."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "spy_bonanza"
        self.game_name = "spy_bonanza"
        self.provider_number = 0
        self.working_name = "Spy Bonanza"
        self.wincap = 10000.0
        self.win_type = "scatter"
        self.rtp = 0.9600
        self.construct_paths()

        # Game Dimensions - 6 reels, 5 rows
        self.num_reels = 6
        self.num_rows = [5] * self.num_reels

        # Symbol payouts - pay anywhere, grouped by cluster sizes
        t1, t2, t3, t4 = (8, 9), (10, 11), (12, 14), (15, 30)
        pay_group = {
            # High paying symbols
            (t1, "H1"): 10.0,
            (t2, "H1"): 25.0,
            (t3, "H1"): 50.0,
            (t4, "H1"): 150.0,
            (t1, "H2"): 5.0,
            (t2, "H2"): 12.5,
            (t3, "H2"): 25.0,
            (t4, "H2"): 100.0,
            (t1, "H3"): 3.0,
            (t2, "H3"): 8.0,
            (t3, "H3"): 15.0,
            (t4, "H3"): 75.0,
            (t1, "H4"): 2.0,
            (t2, "H4"): 5.0,
            (t3, "H4"): 10.0,
            (t4, "H4"): 50.0,
            # Low paying symbols
            (t1, "L1"): 1.0,
            (t2, "L1"): 2.5,
            (t3, "L1"): 5.0,
            (t4, "L1"): 25.0,
            (t1, "L2"): 0.8,
            (t2, "L2"): 2.0,
            (t3, "L2"): 4.0,
            (t4, "L2"): 20.0,
            (t1, "L3"): 0.6,
            (t2, "L3"): 1.5,
            (t3, "L3"): 3.0,
            (t4, "L3"): 15.0,
            (t1, "L4"): 0.4,
            (t2, "L4"): 1.0,
            (t3, "L4"): 2.0,
            (t4, "L4"): 10.0,
            (t1, "L5"): 0.25,
            (t2, "L5"): 0.5,
            (t3, "L5"): 1.0,
            (t4, "L5"): 5.0,
        }
        self.paytable = self.convert_range_table(pay_group)

        self.include_padding = True
        self.special_symbols = {
            "wild": ["W"],
            "scatter": ["S"],
            "ultra_scatter": ["U"],
            "multiplier": ["M"],
        }

        # Regular bonus triggers - 4+ scatters
        self.freespin_triggers = {
            self.basegame_type: {
                4: 10,
                5: 12,
                6: 15,
            },
            self.freegame_type: {
                3: 5,
                4: 5,
                5: 5,
                6: 5,
            },
        }

        # Ultra bonus triggers - 4+ ultra scatters
        self.ultra_freespin_triggers = {
            self.basegame_type: {
                4: 10,
                5: 12,
                6: 15,
            },
            self.freegame_type: {
                3: 5,
                4: 5,
                5: 5,
                6: 5,
            },
        }

        self.anticipation_triggers = {
            self.basegame_type: 3,
            self.freegame_type: 2,
        }

        # Multiplier values for bonus modes
        self.regular_mult_values = {2: 40, 3: 25, 4: 15, 5: 10, 10: 5, 25: 3, 50: 1.5, 100: 0.4, 500: 0.08, 1000: 0.02}
        self.ultra_mult_values = {10: 30, 25: 25, 50: 20, 100: 15, 250: 6, 500: 3, 1000: 1}

        # Reels
        reels = {
            "BR0": "BR0.csv",
            "FR0": "FR0.csv",
            "UFR0": "UFR0.csv",
            "WCAP": "WCAP.csv",
        }
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]
        self.padding_reels["ultra_freegame"] = self.reels["UFR0"]

        # Bet modes
        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1, "WCAP": 5},
                            },
                            "mult_values": {
                                self.basegame_type: {},
                                self.freegame_type: {100: 10, 500: 5, 1000: 2},
                            },
                            "scatter_triggers": {5: 2, 6: 1},
                            "force_wincap": True,
                            "force_freegame": True,
                            "bonus_type": "regular",
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.08,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {4: 10, 5: 3, 6: 1},
                            "mult_values": {
                                self.basegame_type: {},
                                self.freegame_type: self.regular_mult_values,
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "bonus_type": "regular",
                        },
                    ),
                    Distribution(
                        criteria="ultra_freegame",
                        quota=0.02,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                "ultra_freegame": {"UFR0": 1},
                            },
                            "ultra_scatter_triggers": {4: 10, 5: 3, 6: 1},
                            "mult_values": {
                                self.basegame_type: {},
                                "ultra_freegame": self.ultra_mult_values,
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "bonus_type": "ultra",
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.40,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": {self.basegame_type: {}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "bonus_type": None,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.499,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": {self.basegame_type: {}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "bonus_type": None,
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus",
                cost=100.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1, "WCAP": 5},
                            },
                            "mult_values": {
                                self.basegame_type: {},
                                self.freegame_type: {100: 10, 500: 5, 1000: 2},
                            },
                            "scatter_triggers": {4: 1},
                            "force_wincap": True,
                            "force_freegame": True,
                            "bonus_type": "regular",
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.999,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {4: 10, 5: 3, 6: 1},
                            "mult_values": {
                                self.basegame_type: {},
                                self.freegame_type: self.regular_mult_values,
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "bonus_type": "regular",
                        },
                    ),
                ],
            ),
            BetMode(
                name="ultra_bonus",
                cost=500.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                "ultra_freegame": {"UFR0": 1, "WCAP": 5},
                            },
                            "mult_values": {
                                self.basegame_type: {},
                                "ultra_freegame": {100: 10, 500: 5, 1000: 2},
                            },
                            "ultra_scatter_triggers": {4: 1},
                            "force_wincap": True,
                            "force_freegame": True,
                            "bonus_type": "ultra",
                        },
                    ),
                    Distribution(
                        criteria="ultra_freegame",
                        quota=0.999,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                "ultra_freegame": {"UFR0": 1},
                            },
                            "ultra_scatter_triggers": {4: 10, 5: 3, 6: 1},
                            "mult_values": {
                                self.basegame_type: {},
                                "ultra_freegame": self.ultra_mult_values,
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "bonus_type": "ultra",
                        },
                    ),
                ],
            ),
        ]
