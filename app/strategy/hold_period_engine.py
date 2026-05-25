def estimate_hold_period(volatility):
    if volatility < 2:
        return 10

    elif volatility < 4:
        return 7

    return 5
