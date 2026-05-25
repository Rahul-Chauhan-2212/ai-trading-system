from ta.momentum import RSIIndicator
from ta.trend import MACD


def add_indicators(data):
    data['EMA20'] = data['close'].ewm(span=20).mean()
    data['EMA50'] = data['close'].ewm(span=50).mean()

    rsi = RSIIndicator(close=data['close'])
    data['RSI'] = rsi.rsi()

    macd = MACD(close=data['close'])

    data['MACD'] = macd.macd()
    data['MACD_SIGNAL'] = macd.macd_signal()

    return data
