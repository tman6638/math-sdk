"""Sweet Bonanza Clone game state overrides"""

from game_executables import GameExecutables
from src.events.events import update_freespin_event
from src.calculations.statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    """
    Override or extend universal state.py functions for Sweet Bonanza Clone.
    """

    def reset_book(self):
        """Reset global values used across multiple spins."""
        super().reset_book()
        self.tumble_win = 0
        self.accumulated_multiplier = 0

    def reset_fs_spin(self):
        """Reset values at the start of free spin round."""
        super().reset_fs_spin()
        self.accumulated_multiplier = 0

    def assign_special_sym_function(self):
        """
        Define functions to assign special attributes to symbols.
        M (multiplier bomb) symbols get random multiplier values.
        """
        self.special_symbol_functions = {"M": [self.assign_mult_property]}

    def assign_mult_property(self, symbol):
        """
        Assign multiplier attribute to multiplier bomb symbol.
        Uses betmode conditions to determine which multiplier distribution to use.
        """
        # Get the current betmode's multiplier distribution
        mult_values = self.get_current_distribution_conditions()["mult_values"][self.gametype]
        
        # Select a random multiplier value based on the distribution
        multiplier_value = get_random_outcome(mult_values)
        
        # Assign the multiplier attribute to the symbol
        symbol.assign_attribute({"multiplier": multiplier_value})

    def check_game_repeat(self):
        """
        Verify final win matches required betmode conditions.
        Used for forced win conditions in distributions.
        """
        if self.repeat == False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True

    def update_fs_retrigger_amt(self):
        """
        Update free spin count when retrigger occurs.
        In Sweet Bonanza, 3+ scatters during free spins adds 5 more spins.
        """
        scatter_count = self.count_special_symbols("scatter")
        if scatter_count >= 3:
            self.tot_fs += 5
            # Update free spin event to reflect new total
            update_freespin_event(self)
