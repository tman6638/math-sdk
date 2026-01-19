"""Custom events for Spy Bonanza."""

from src.events.event_constants import EventConstants


def send_mult_info_event(gamestate, board_mult, mult_info, base_win, final_win):
    """Send multiplier information event."""
    event = {
        "index": len(gamestate.book.events),
        "type": "multiplierApplied",
        "boardMultiplier": board_mult,
        "multiplierPositions": mult_info,
        "baseWin": int(round(base_win * 100, 0)),
        "finalWin": int(round(final_win * 100, 0)),
        "bonusType": getattr(gamestate, 'bonus_type', None),
    }
    gamestate.book.add_event(event)


def send_bonus_trigger_event(gamestate, bonus_type, scatter_count, spins_awarded):
    """Send bonus trigger event."""
    event = {
        "index": len(gamestate.book.events),
        "type": "bonusTrigger",
        "bonusType": bonus_type,
        "scatterCount": scatter_count,
        "spinsAwarded": spins_awarded,
    }
    gamestate.book.add_event(event)