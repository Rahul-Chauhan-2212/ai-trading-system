def generate_signal(data, sentiment_score):
    latest = data.iloc[-1]

    signal = "HOLD"
    confidence = 50
    holding_days = 5

    bullish = (
            latest['EMA20'] > latest['EMA50'] and
            latest['RSI'] > 55 and
            latest['MACD'] > latest['MACD_SIGNAL']
    )

    bearish = (
            latest['EMA20'] < latest['EMA50'] and
            latest['RSI'] < 40
    )

    if bullish and sentiment_score > 0.6:

        signal = "BUY"
        confidence = 84
        holding_days = 7

    elif bearish:

        signal = "SELL"
        confidence = 79
        holding_days = 5

    return {
        "signal": signal,
        "confidence": confidence,
        "holding_days": holding_days
    }
