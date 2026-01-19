"""Spy Bonanza game calculations."""

from src.executables.executables import Executables


class GameCalculations(Executables):
    """Game specific calculations for Spy Bonanza."""

    def get_board_multipliers(self, multiplier_key="multiplier"):
        """Find multiplier from board using winning positions."""
        board_mult = 0
        mult_info = []
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].check_attribute(multiplier_key):
                    board_mult += self.board[reel][row].get_attribute(multiplier_key)
                    mult_info.append({
                        "reel": reel,
                        "row": row,
                        "value": self.board[reel][row].get_attribute(multiplier_key)
                    })

        return max(1, board_mult), mult_info

    def count_scatter_symbols(self, scatter_key="scatter"):
        """Count regular scatter symbols (S) on board."""
        count = 0
        for reel in self.board:
            for symbol in reel:
                if symbol.name in self.config.special_symbols.get(scatter_key, []):
                    count += 1
        return count

    def count_ultra_scatter_symbols(self, ultra_scatter_key="ultra_scatter"):
        """Count ultra scatter symbols (U) on board."""
        count = 0
        for reel in self.board:
            for symbol in reel:
                if symbol.name in self.config.special_symbols.get(ultra_scatter_key, []):
                    count += 1
        return count

    def check_fs_condition(self):
        """Check if regular bonus trigger condition is met."""
        scatter_count = self.count_scatter_symbols()
        if self.gametype == self.config.basegame_type:
            return scatter_count >= min(self.config.freespin_triggers[self.config.basegame_type].keys())
        elif self.gametype == self.config.freegame_type:
            return scatter_count >= min(self.config.freespin_triggers[self.config.freegame_type].keys())
        return False

    def check_ultra_fs_condition(self):
        """Check if ultra bonus trigger condition is met."""
        ultra_scatter_count = self.count_ultra_scatter_symbols()
        if self.gametype == self.config.basegame_type:
            return ultra_scatter_count >= min(self.config.ultra_freespin_triggers[self.config.basegame_type].keys())
        return False

    def get_fs_award_amount(self, scatter_key="scatter"):
        """Get freespin award for regular bonus."""
        scatter_count = self.count_scatter_symbols(scatter_key)
        triggers = self.config.freespin_triggers.get(self.gametype, {})
        for count, spins in sorted(triggers.items(), reverse=True):
            if scatter_count >= count:
                return spins
        return 0

    def get_ultra_fs_award_amount(self, ultra_scatter_key="ultra_scatter"):
        """Get freespin award for ultra bonus."""
        ultra_count = self.count_ultra_scatter_symbols(ultra_scatter_key)
        triggers = self.config.ultra_freespin_triggers.get(self.gametype, {})
        for count, spins in sorted(triggers.items(), reverse=True):
            if ultra_count >= count:
                return spins
        return 0
