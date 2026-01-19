from game_executables import GameExecutables
from src.events.events import update_freespin_event, update_global_mult_event
from src.calculations. statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    """Override class for Spy Bonanza specific game logic."""

    def reset_book(self):
        super().reset_book()
        self.tumble_win = 0
        self.bonus_type = None

    def reset_fs_spin(self):
        """Reset for regular bonus."""
        super().reset_fs_spin()
        self.global_multiplier = 1
        self. bonus_type = "regular"

    def reset_ultra_fs_spin(self):
        """Reset for ultra bonus."""
        super().reset_fs_spin()
        self.global_multiplier = 1
        self.bonus_type = "ultra"

    def assign_special_sym_function(self):
        """Assign special symbol functions."""
        self.special_symbol_functions = {"M": [self.assign_mult_property]}

    def assign_mult_property(self, symbol):
        """Assign multiplier value based on bonus type."""
        if self.bonus_type == "ultra":
            mult_values = self.config.ultra_mult_values
        elif self.bonus_type == "regular": 
            mult_values = self.config.regular_mult_values
        else:
            # No multipliers in base game
            return

        conditions = self.get_current_distribution_conditions()
        gametype_mults = conditions.get("mult_values", {}).get(self.gametype, mult_values)
        if gametype_mults: 
            multiplier_value = get_random_outcome(gametype_mults)
            symbol.assign_attribute({"multiplier": multiplier_value})

    def check_freespin_entry(self):
        """Verify bonus entry conditions for regular bonus."""
        conditions = self.get_current_distribution_conditions()
        if conditions.get("force_freegame", False):
            if conditions.get("bonus_type") == "regular":
                return True
        return self.check_fs_condition()

    def check_ultra_freespin_entry(self):
        """Verify bonus entry conditions for ultra bonus."""
        conditions = self. get_current_distribution_conditions()
        if conditions.get("force_freegame", False):
            if conditions.get("bonus_type") == "ultra":
                return True
        return self.check_ultra_fs_condition()

    def end_freespin(self):
        """End regular freespin mode."""
        self. gametype = self.config.basegame_type
        self.bonus_type = None

    def end_ultra_freespin(self):
        """End ultra freespin mode."""
        self.gametype = self.config.basegame_type
        self.bonus_type = None

    def check_game_repeat(self):
        """Verify final win matches required betmode conditions."""
        if not self.repeat:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria: 
                self.repeat = True