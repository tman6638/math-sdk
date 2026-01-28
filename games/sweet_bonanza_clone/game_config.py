"""Sweet Bonanza Clone Game Configuration"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    """Load all game specific parameters and elements for Sweet Bonanza Clone"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "sweet_bonanza_clone"
        self.game_name = "sweet_bonanza_clone"
        self.provider_number = 0
        self.working_name = "Sweet Bonanza Clone - Tumbling Slot"
        self.wincap = 10000.0  # Max win 10,000x
        self.win_type = "scatter"
        self.rtp = 0.9640  # Target 96.4% RTP
        
        # Call construct_paths - handle both versions
        try:
            self.construct_paths()
        except TypeError:
            # Newer version requires game_id parameter
            import inspect
            if 'game_id' in inspect.signature(self.construct_paths).parameters:
                self.construct_paths(self.game_id)
            else:
                raise

        # Game Dimensions - 6 reels x 5 rows
        self.num_reels = 6
        self.num_rows = [5] * self.num_reels
        
        # Paytable - Scatter pay groupings (REDUCED for 96.4% RTP)
        # Groups: (8-9), (10-11), (12-14), (15+)
        # Values reduced by ~70% from original to balance RTP with tumbling
        t1, t2, t3, t4 = (8, 9), (10, 11), (12, 14), (15, 30)
        pay_group = {
            # High pays (candy symbols) - reduced significantly
            (t1, "H1"): 2.5,   # was 10.0
            (t2, "H1"): 6.0,   # was 25.0
            (t3, "H1"): 12.0,  # was 50.0
            (t4, "H1"): 100.0, # was 500.0
            (t1, "H2"): 2.0,   # was 8.0
            (t2, "H2"): 5.0,   # was 20.0
            (t3, "H2"): 10.0,  # was 40.0
            (t4, "H2"): 60.0,  # was 250.0
            (t1, "H3"): 1.5,   # was 5.0
            (t2, "H3"): 4.0,   # was 15.0
            (t3, "H3"): 8.0,   # was 30.0
            (t4, "H3"): 40.0,  # was 150.0
            (t1, "H4"): 1.2,   # was 4.0
            (t2, "H4"): 3.0,   # was 10.0
            (t3, "H4"): 6.0,   # was 20.0
            (t4, "H4"): 25.0,  # was 100.0
            # Low pays (fruit symbols) - reduced significantly
            (t1, "L1"): 0.8,   # was 2.5
            (t2, "L1"): 2.0,   # was 5.0
            (t3, "L1"): 4.0,   # was 10.0
            (t4, "L1"): 15.0,  # was 50.0
            (t1, "L2"): 0.6,   # was 2.0
            (t2, "L2"): 1.5,   # was 4.0
            (t3, "L2"): 3.0,   # was 8.0
            (t4, "L2"): 12.0,  # was 40.0
            (t1, "L3"): 0.5,   # was 1.5
            (t2, "L3"): 1.2,   # was 3.0
            (t3, "L3"): 2.5,   # was 6.0
            (t4, "L3"): 10.0,  # was 30.0
            (t1, "L4"): 0.4,   # was 1.0
            (t2, "L4"): 1.0,   # was 2.0
            (t3, "L4"): 2.0,   # was 4.0
            (t4, "L4"): 8.0,   # was 20.0
        }
        self.paytable = self.convert_range_table(pay_group)

        self.include_padding = True
        self.special_symbols = {
            "wild": ["W"],
            "scatter": ["S"],
            "multiplier": ["M"]
        }

        # Scatter payouts: count -> (payout, free_spins)
        self.scatter_payouts = {
            4: (3.0, 10),
            5: (5.0, 10),
            6: (100.0, 10),
        }

        # Free spin triggers
        # Base game: 4+ scatters trigger bonus
        # Free game: 3+ scatters retrigger for +5 spins
        self.freespin_triggers = {
            self.basegame_type: {
                4: 10,
                5: 10,
                6: 10,
            },
            self.freegame_type: {
                3: 5,  # Retrigger adds 5 spins
                4: 5,
                5: 5,
                6: 5,
            },
        }
        
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }

        # Multiplier distributions
        # Standard multipliers for base/ante/bonus_buy
        self.standard_mult_values = {
            2: 0.30,    # 30%
            3: 0.20,    # 20%
            4: 0.15,    # 15%
            5: 0.12,    # 12%
            6: 0.08,    # 8%
            8: 0.05,    # 5%
            10: 0.04,   # 4%
            12: 0.025,  # 2.5%
            15: 0.015,  # 1.5%
            20: 0.01,   # 1%
            25: 0.005,  # 0.5%
            50: 0.003,  # 0.3%
            100: 0.002, # 0.2%
        }

        # Super multipliers for super_bonus mode
        self.super_mult_values = {
            10: 0.35,   # 35%
            12: 0.20,   # 20%
            15: 0.15,   # 15%
            20: 0.10,   # 10%
            25: 0.08,   # 8%
            50: 0.06,   # 6%
            75: 0.03,   # 3%
            100: 0.02,  # 2%
            250: 0.008, # 0.8%
            500: 0.002, # 0.2%
        }

        # Convert probabilities to weights for random selection
        self.standard_mult_weights = {k: int(v * 1000) for k, v in self.standard_mult_values.items()}
        self.super_mult_weights = {k: int(v * 1000) for k, v in self.super_mult_values.items()}

        # Reels
        reels = {
            "BR0": "BR0.csv",  # Base game reels
            "AR0": "AR0.csv",  # Ante bet reels (higher scatter frequency)
            "FR0": "FR0.csv",  # Free spin reels
            "WCAP": "WCAP.csv" # Win cap reels
        }
        self.reels = {}
        for r, f in reels.items():
            reel_path = os.path.join(self.reels_path, f)
            if os.path.exists(reel_path):
                self.reels[r] = self.read_reels_csv(reel_path)

        self.padding_reels[self.basegame_type] = self.reels.get("BR0", {})
        self.padding_reels[self.freegame_type] = self.reels.get("FR0", {})

        # Bet Modes Configuration
        self.bet_modes = [
            # 1. Base Mode - Standard 1x bet
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
                        criteria="basegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": {
                                self.basegame_type: {1: 1},
                                self.freegame_type: self.standard_mult_weights,
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
            # 2. Ante Bet Mode - 1.25x bet with increased scatter frequency
            BetMode(
                name="ante",
                cost=1.25,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="basegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"AR0": 1}},  # Use ante reels
                            "mult_values": {
                                self.basegame_type: {1: 1},
                                self.freegame_type: self.standard_mult_weights,
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
            # 3. Bonus Buy Mode - 100x bet, starts in bonus
            BetMode(
                name="bonus_buy",
                cost=100.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="freegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "mult_values": {
                                self.basegame_type: {1: 1},
                                self.freegame_type: self.standard_mult_weights,
                            },
                            "force_wincap": False,
                            "force_freegame": False,  # Bonus buy skips base, no need to force
                        },
                    ),
                ],
            ),
            # 4. Super Bonus Buy Mode - 500x bet, high multipliers only
            BetMode(
                name="super_bonus",
                cost=500.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="freegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "mult_values": {
                                self.basegame_type: {1: 1},
                                self.freegame_type: self.super_mult_weights,
                            },
                            "force_wincap": False,
                            "force_freegame": False,  # Bonus buy skips base, no need to force
                        },
                    ),
                ],
            ),
        ]
    
    def __getstate__(self):
        """Custom pickle support - save reel file paths instead of loaded reels"""
        state = self.__dict__.copy()
        # Store the reel mapping for reconstruction
        state['_reel_files'] = {
            "BR0": "BR0.csv",
            "AR0": "AR0.csv",
            "FR0": "FR0.csv",
            "WCAP": "WCAP.csv"
        }
        return state
    
    def __setstate__(self, state):
        """Custom unpickle support - reload reels from files"""
        self.__dict__.update(state)
        # Reconstruct reels from files if they're missing
        if not self.reels or len(self.reels) == 0:
            reel_files = state.get('_reel_files', {
                "BR0": "BR0.csv",
                "AR0": "AR0.csv",
                "FR0": "FR0.csv",
                "WCAP": "WCAP.csv"
            })
            self.reels = {}
            for r, f in reel_files.items():
                reel_path = os.path.join(self.reels_path, f)
                if os.path.exists(reel_path):
                    self.reels[r] = self.read_reels_csv(reel_path)
            
            # Update padding reels after reconstruction
            self.padding_reels[self.basegame_type] = self.reels.get("BR0", {})
            self.padding_reels[self.freegame_type] = self.reels.get("FR0", {})
