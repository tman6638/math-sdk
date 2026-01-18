"""Sweet Bonanza Clone executable functions"""

from copy import copy
from game_calculations import GameCalculations
from src.calculations.scatter import Scatter
from game_events import send_multiplier_collect_event, send_scatter_payout_event
from src.events.events import (
    set_win_event,
    set_total_event,
    fs_trigger_event,
    update_tumble_win_event,
    update_freespin_event,
)


class GameExecutables(GameCalculations):
    """Game specific executable functions for Sweet Bonanza Clone."""

    def get_scatterpays_update_wins(self):
        """
        Evaluate scatter pays and update wins.
        In Sweet Bonanza, we check for 8+ matching symbols anywhere on board.
        """
        self.win_data = Scatter.get_scatterpay_wins(
            self.config, self.board, global_multiplier=1  # No global multiplier in this game
        )
        Scatter.record_scatter_wins(self)
        self.win_manager.tumble_win = self.win_data["totalWin"]
        self.win_manager.update_spinwin(self.win_data["totalWin"])

    def spawn_multiplier_bombs(self):
        """
        Spawn multiplier bombs on the board during free spins.
        This is called after board is drawn but before win evaluation.
        Multiplier bombs (M symbols) should already be on the reels with multiplier attributes.
        This function can be used for additional logic if needed.
        """
        # Multiplier bombs come from the reels with attributes already assigned
        # No additional spawning needed in this implementation
        pass

    def collect_and_apply_multipliers(self):
        """
        Collect multipliers from the board when there's a win during free spins.
        Multipliers ADD together and apply to the tumble win.
        Multiplier bombs stay on board (don't explode).
        """
        if self.gametype == self.config.freegame_type and self.win_manager.tumble_win > 0:
            # Collect all multipliers from board
            total_mult, mult_info = self.collect_multipliers_from_board()
            
            if len(mult_info) > 0:
                # Save base tumble win and current spin win before multiplier
                base_tumble_win = copy(self.win_manager.tumble_win)
                old_spin_win = copy(self.win_manager.spin_win)
                
                # Apply multiplier to tumble win
                multiplied_win = base_tumble_win * total_mult
                self.win_manager.tumble_win = multiplied_win
                
                # Calculate new spin win and update using set_spin_win to maintain consistency
                new_spin_win = old_spin_win - base_tumble_win + multiplied_win
                self.win_manager.set_spin_win(new_spin_win)
                
                # Emit multiplier collect event
                send_multiplier_collect_event(
                    self,
                    total_mult,
                    mult_info,
                    base_tumble_win
                )

    def set_end_tumble_event(self):
        """
        Called after all tumbling events have finished for a spin.
        Emit final win events.
        """
        if self.win_manager.spin_win > 0:
            set_win_event(self)
        set_total_event(self)

    def update_freespin_amount(self, scatter_key: str = "scatter"):
        """
        Update free spin count based on scatter symbols.
        Base game: 4+ scatters = 10 free spins
        Free game: 3+ scatters = +5 free spins (retrigger)
        """
        scatter_count = self.count_special_symbols(scatter_key)
        
        if self.gametype == self.config.basegame_type:
            # Base game trigger
            if scatter_count >= 4:
                self.tot_fs = 10
                # Check for scatter payout
                if scatter_count in self.config.scatter_payouts:
                    payout, _ = self.config.scatter_payouts[scatter_count]
                    # Add scatter payout to wins
                    self.win_manager.update_spinwin(payout)
                    send_scatter_payout_event(self, scatter_count, payout, self.tot_fs)
                
                fs_trigger_event(self, basegame_trigger=True, freegame_trigger=False)
        else:
            # Free game retrigger
            if scatter_count >= 3:
                self.tot_fs += 5  # Add 5 spins for retrigger
                # Check for scatter payout
                if scatter_count in self.config.scatter_payouts:
                    payout, _ = self.config.scatter_payouts[scatter_count]
                    self.win_manager.update_spinwin(payout)
                    send_scatter_payout_event(self, scatter_count, payout, 5)
                
                fs_trigger_event(self, basegame_trigger=False, freegame_trigger=True)

    def update_freespin(self) -> None:
        """Called before a new reveal during freegame."""
        self.fs += 1
        update_freespin_event(self)
        self.win_manager.reset_spin_win()
        self.reset_accumulated_multiplier()  # Reset multipliers for new spin
        self.win_data = {}

    def check_retrigger(self) -> bool:
        """
        Check if retrigger condition is met (3+ scatters in free game).
        Returns True if retrigger occurred.
        """
        if self.gametype == self.config.freegame_type:
            scatter_count = self.count_special_symbols("scatter")
            if scatter_count >= 3:
                return True
        return False

    def emit_tumble_win_events(self) -> None:
        """
        Transmit win information after tumble evaluation.
        In free spins, also collect and apply multipliers.
        """
        if self.gametype == self.config.freegame_type:
            # Collect and apply multipliers if there's a win
            self.collect_and_apply_multipliers()
        
        # Emit win events
        if self.win_manager.tumble_win > 0:
            update_tumble_win_event(self)
