"""Sweet Bonanza Clone game calculations"""

from src.executables.executables import Executables


class GameCalculations(Executables):
    """Game specific calculations for Sweet Bonanza Clone."""

    def get_multiplier_bomb_positions(self, multiplier_key: str = "multiplier") -> list:
        """
        Find all multiplier bomb positions on the board.
        Returns list of (reel, row, value) tuples for all multiplier bombs.
        """
        mult_positions = []
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].check_attribute(multiplier_key):
                    mult_value = self.board[reel][row].get_attribute(multiplier_key)
                    mult_positions.append({
                        "reel": reel,
                        "row": row,
                        "value": mult_value
                    })
        return mult_positions

    def collect_multipliers_from_board(self, multiplier_key: str = "multiplier") -> tuple:
        """
        Collect all multiplier values from the board and sum them.
        Returns (total_multiplier, mult_info_list).
        Multipliers ADD together (not multiply).
        """
        total_mult = 0
        mult_info = []
        
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].check_attribute(multiplier_key):
                    mult_value = self.board[reel][row].get_attribute(multiplier_key)
                    total_mult += mult_value
                    mult_info.append({
                        "reel": reel,
                        "row": row,
                        "value": mult_value
                    })
        
        # Return accumulated multiplier (minimum 1x if no multipliers present)
        return max(1, total_mult), mult_info

    def calculate_accumulated_multiplier(self) -> int:
        """
        Calculate the total accumulated multiplier for the current tumble.
        Used during free spins to apply collected multipliers to wins.
        """
        if not hasattr(self, 'accumulated_multiplier'):
            self.accumulated_multiplier = 0
        return max(1, self.accumulated_multiplier)

    def reset_accumulated_multiplier(self):
        """Reset accumulated multiplier at the start of each free spin."""
        self.accumulated_multiplier = 0

    def add_to_accumulated_multiplier(self, amount: int):
        """Add multiplier value to the accumulated total."""
        if not hasattr(self, 'accumulated_multiplier'):
            self.accumulated_multiplier = 0
        self.accumulated_multiplier += amount
