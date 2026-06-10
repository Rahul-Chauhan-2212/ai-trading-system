import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(bind=engine)


# ==========================================================
# SAVE OHLCV DATA
# ==========================================================
def save_ohlcv(df, symbol, exchange="NSE"):
    query = text("""
        INSERT INTO ohlcv (
            timestamp,
            symbol,
            exchange,
            open,
            high,
            low,
            close,
            volume
        )
        VALUES (
            :timestamp,
            :symbol,
            :exchange,
            :open,
            :high,
            :low,
            :close,
            :volume
        )
        ON CONFLICT (timestamp, symbol)
        DO UPDATE SET
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume
    """)

    with engine.begin() as conn:
        for index, row in df.iterrows():
            conn.execute(query, {
                "timestamp": row["timestamp"],
                "symbol": symbol,
                "exchange": exchange,
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": int(row["volume"])
            })

    print(f"Saved {len(df)} rows for {symbol}")


# ==========================================================
# GET LAST STORED TIMESTAMP
# ==========================================================
def get_last_timestamp(symbol):
    query = text("""
        SELECT MAX(timestamp)
        FROM ohlcv
        WHERE symbol = :symbol
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "symbol": symbol
        }).scalar()

    return result
