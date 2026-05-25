from app.indicators.technical_indicators import add_indicators
from app.ingestion.fetch_nse_data import fetch_stock_data
from app.ingestion.save_data import save_to_db
from app.notifications.telegram_bot import send_telegram_message
from app.strategy.signal_generator import generate_signal
import asyncio

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS"
]


def run():
    for stock in stocks:
        data = fetch_stock_data(stock)

        save_to_db(data)

        data = add_indicators(data)

        sentiment_score = 0.75

        signal_data = generate_signal(
            data,
            sentiment_score
        )

        message = f"""
        🚀 SWING ALERT

        📈 Stock: {stock}
        📊 Signal: {signal_data['signal']}
        🎯 Confidence: {signal_data['confidence']}%
        📅 Hold Days: {signal_data['holding_days']}
        """.strip()

        asyncio.run(send_telegram_message(message))
