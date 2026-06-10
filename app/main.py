import asyncio

from app.database.models import init_db
from app.indicators.technical_indicators import add_indicators
from app.ingestion.fetch_nse_data import NSEDataFetcher
from app.ingestion.save_data import save_to_db
from app.notifications.telegram_bot import send_telegram_message
from app.strategy.signal_generator import generate_signal

SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS"
]

# ==========================================================
# INIT DB
# ==========================================================
init_db()

# ==========================================================
# FETCH DATA
# ==========================================================
fetcher = NSEDataFetcher()

fetcher.sync_all_symbols(SYMBOLS)


def run():
    for stock in SYMBOLS:
        data = fetcher(stock)

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
