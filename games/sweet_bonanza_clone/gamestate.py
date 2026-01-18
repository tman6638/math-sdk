"""Sweet Bonanza Clone game state management"""

from game_override import GameStateOverride
from src.calculations.scatter import Scatter


class GameState(GameStateOverride):
    """Gamestate for Sweet Bonanza Clone - handles spin and free spin logic."""

    def run_spin(self, sim: int, simulation_seed=None):
        """
        Execute a single base game spin with tumbling mechanics.
        
        For bonus buy modes, skip base game and go directly to free spins.
        
        Flow:
        1. Draw initial board
        2. Evaluate scatter pays
        3. Tumble winning symbols and repeat until no wins
        4. Check for bonus trigger (4+ scatters)
        5. Run free spins if triggered
        """
        self.reset_seed(sim)
        self.repeat = True
        
        # Check if this is a bonus buy mode - if so, skip to bonus
        if self.get_current_betmode().get_buybonus():
            # Bonus buy: go directly to free spins
            while self.repeat:
                self.reset_book()
                # Mark that we triggered freegame for validation
                self.triggered_freegame = True
                # Award 10 free spins for bonus buy
                self.tot_fs = 10
                # Run the free spin bonus
                self.run_freespin()
                # Finalize
                self.evaluate_finalwin()
                self.check_repeat()
            self.imprint_wins()
            return
        
        # Normal base game flow
        while self.repeat:
            self.reset_book()
            self.draw_board()

            # Evaluate wins
            self.get_scatterpays_update_wins()
            self.emit_tumble_win_events()

            # Continue tumbling while there are wins
            while self.win_data["totalWin"] > 0 and not (self.wincap_triggered):
                self.tumble_game_board()
                self.get_scatterpays_update_wins()
                self.emit_tumble_win_events()

            # Finalize spin
            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            # Check for bonus trigger
            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            # Finalize and check repeat conditions
            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        """
        Execute free spin bonus round with multiplier bombs.
        
        Flow for each free spin:
        1. Draw board (with multiplier bombs from reels)
        2. Evaluate scatter pays
        3. If win: collect multipliers and apply to win
        4. Tumble and repeat until no wins
        5. Check for retrigger (3+ scatters = +5 spins)
        6. Continue until all free spins complete
        """
        self.reset_fs_spin()
        
        while self.fs < self.tot_fs:
            # Start new free spin
            self.update_freespin()
            self.draw_board()

            # Spawn multiplier bombs (already on reels, but call for consistency)
            self.spawn_multiplier_bombs()

            # Evaluate wins
            self.get_scatterpays_update_wins()
            self.emit_tumble_win_events()  # This also collects/applies multipliers

            # Continue tumbling while there are wins
            while self.win_data["totalWin"] > 0 and not (self.wincap_triggered):
                self.tumble_game_board()
                self.get_scatterpays_update_wins()
                self.emit_tumble_win_events()  # Multipliers applied each tumble

            # Finalize spin
            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            # Check for retrigger
            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

        self.end_freespin()
