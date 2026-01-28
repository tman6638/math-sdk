"""Custom events for Sweet Bonanza Clone"""

MULTIPLIER_COLLECT = "multiplierCollect"
SCATTER_PAY = "scatterPay"


def send_multiplier_collect_event(gamestate, collected_mult: int, mult_info: list, tumble_win: float):
    """
    Emit event when multipliers are collected during a tumble in free spins.
    
    Args:
        gamestate: Current game state
        collected_mult: Total multiplier collected this tumble
        mult_info: List of multiplier positions and values
        tumble_win: Win amount before multiplier applied
    """
    multiplier_info = {}
    multiplier_info["positions"] = []
    
    if gamestate.config.include_padding:
        for m in mult_info:
            multiplier_info["positions"].append({
                "reel": m["reel"],
                "row": m["row"] + 1,  # Add 1 for padding
                "multiplier": m["value"]
            })
    else:
        for m in mult_info:
            multiplier_info["positions"].append({
                "reel": m["reel"],
                "row": m["row"],
                "multiplier": m["value"]
            })

    event = {
        "index": len(gamestate.book.events),
        "type": MULTIPLIER_COLLECT,
        "multiplierInfo": multiplier_info,
        "totalMultiplier": collected_mult,
        "tumbleWin": int(round(min(tumble_win, gamestate.config.wincap) * 100)),
    }
    gamestate.book.add_event(event)


def send_scatter_payout_event(gamestate, scatter_count: int, payout: float, free_spins: int):
    """
    Emit event when scatter symbols award a payout and/or free spins.
    
    Args:
        gamestate: Current game state
        scatter_count: Number of scatter symbols
        payout: Payout amount in bet multiplier
        free_spins: Number of free spins awarded
    """
    event = {
        "index": len(gamestate.book.events),
        "type": SCATTER_PAY,
        "scatterCount": scatter_count,
        "payout": int(round(min(payout, gamestate.config.wincap) * 100)),
        "freeSpins": free_spins,
    }
    gamestate.book.add_event(event)
