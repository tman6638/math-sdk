"""Spy Bonanza game executables."""

from copy import copy
from game_calculations import GameCalculations
from src.calculations.scatter import Scatter
from game_events import send_mult_info_event
from src.events. events import (
    set_win_event,
    set_total_event,
    fs_trigger_event,
    update_tumble_win_event,
    update_global_mult_event,
    update_freespin_event,
)


class GameExecutables(GameCalculations):
    """Game specific executable functions for Spy Bonanza."""

    def set_end_tumble_event(self):
        """After all tumbling events have finished, multiply tumble-win by sum of mult symbols."""
        # Only apply board multipliers in bonus modes
        if self. gametype in [self.config.freegame_type, "ultra_freegame"]:
            board_mult, mult_info = self.get_board_multipliers()
            base_tumble_win = copy(self.win_manager.spin_win)
            self.win_manager. set_spin_win(base_tumble_win * board_mult)
            if self.win_manager.spin_win > 0 and len(mult_info) > 0:
                send_mult_info_event(
                    self,
                    board_mult,
                    mult_info,
                    base_tumble_win,
                    self.win_manager.spin_win,
                )
                update_tumble_win_event(self)

        if self.win_manager.spin_win > 0:
            set_win_event(self)
        set_total_event(self)

    def update_freespin_amount(self, scatter_key: str = "scatter"):
        """Update current and total freespin number for regular bonus."""
        self.tot_fs = self.get_fs_award_amount(scatter_key)
        fs_trigger_event(self, basegame_trigger=True, freegame_trigger=False)

    def update_ultra_freespin_amount(self, ultra_scatter_key:  str = "ultra_scatter"):
        """Update current and total freespin number for ultra bonus."""
        self.tot_fs = self.get_ultra_fs_award_amount(ultra_scatter_key)
        fs_trigger_event(self, basegame_trigger=True, freegame_trigger=False)

    def get_scatterpays_update_wins(self):
        """Evaluate scatter pays - no global multiplier in base game."""
        mult = 1 if self.gametype == self.config. basegame_type else self.global_multiplier
        self.win_data = Scatter. get_scatterpay_wins(
            self.config, self.board, global_multiplier=mult
        )
        Scatter.record_scatter_wins(self)
        self.win_manager.tumble_win = self.win_data["totalWin"]
        self.win_manager.update_spinwin(self.win_data["totalWin"])

    def update_freespin(self) -> None:
        """Called before a new reveal during regular freegame."""
        self.fs += 1
        update_freespin_event(self)
        self.global_multiplier = 1
        update_global_mult_event(self)
        self.win_manager.reset_spin_win()
        self.tumblewin_mult = 0
        self.win_data = {}

    def update_ultra_freespin(self) -> None:
        """Called before a new reveal during ultra freegame."""
        self.fs += 1
        update_freespin_event(self)
        self.global_multiplier = 1
        update_global_mult_event(self)
        self.win_manager.reset_spin_win()
        self.tumblewin_mult = 0
        self.win_data = {}

    def update_fs_retrigger_amt(self):
        """Retrigger freespins in regular bonus."""
        additional_spins = self.get_fs_award_amount()
        self.tot_fs += additional_spins
        fs_trigger_event(self, basegame_trigger=False, freegame_trigger=True)

    def update_ultra_fs_retrigger_amt(self):
        """Retrigger freespins in ultra bonus."""
        additional_spins = self.get_ultra_fs_award_amount()
        self.tot_fs += additional_spins
        fs_trigger_event(self, basegame_trigger=False, freegame_trigger=True)