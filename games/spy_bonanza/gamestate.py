from game_override import GameStateOverride
from src.calculations.scatter import Scatter


class GameState(GameStateOverride):
    """Gamestate for Spy Bonanza - handles both regular and ultra bonus modes."""

    def run_spin(self, sim:  int, simulation_seed=None):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_board()

            # No multipliers in base game
            self.get_scatterpays_update_wins()
            self.emit_tumble_win_events()

            while self.win_data["totalWin"] > 0 and not self.wincap_triggered:
                self. tumble_game_board()
                self. get_scatterpays_update_wins()
                self. emit_tumble_win_events()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            # Check for regular bonus (S scatters)
            if self.check_fs_condition() and self.check_freespin_entry():
                self. run_freespin_from_base()
            # Check for ultra bonus (U scatters)
            elif self. check_ultra_fs_condition() and self.check_ultra_freespin_entry():
                self.run_ultra_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        """Regular bonus mode - multipliers 2x-1000x."""
        self.reset_fs_spin()
        self.bonus_type = "regular"
        while self.fs < self.tot_fs:
            self.update_freespin()
            self.draw_board()

            self.get_scatterpays_update_wins()
            self.emit_tumble_win_events()

            while self. win_data["totalWin"] > 0 and not self.wincap_triggered:
                self.tumble_game_board()
                self.update_global_mult()

                self.get_scatterpays_update_wins()
                self.emit_tumble_win_events()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

        self.end_freespin()

    def run_ultra_freespin(self):
        """Ultra bonus mode - multipliers 10x-1000x."""
        self.reset_ultra_fs_spin()
        self.bonus_type = "ultra"
        while self.fs < self.tot_fs:
            self.update_ultra_freespin()
            self.draw_board()

            self.get_scatterpays_update_wins()
            self.emit_tumble_win_events()

            while self. win_data["totalWin"] > 0 and not self.wincap_triggered:
                self.tumble_game_board()
                self.update_global_mult()

                self.get_scatterpays_update_wins()
                self.emit_tumble_win_events()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_ultra_fs_condition():
                self.update_ultra_fs_retrigger_amt()

        self.end_ultra_freespin()

    def run_freespin_from_base(self):
        """Transition from base game to regular freespin."""
        self.update_freespin_amount()
        self.gametype = self.config.freegame_type
        self.run_freespin()

    def run_ultra_freespin_from_base(self):
        """Transition from base game to ultra freespin."""
        self. update_ultra_freespin_amount()
        self.gametype = "ultra_freegame"
        self.run_ultra_freespin()