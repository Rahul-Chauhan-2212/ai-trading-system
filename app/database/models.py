from sqlalchemy import text
from app.database.db import engine

with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS ohlcv (
        timestamp TIMESTAMPTZ,
        symbol TEXT,
        exchange TEXT,
        open DOUBLE PRECISION,
        high DOUBLE PRECISION,
        low DOUBLE PRECISION,
        close DOUBLE PRECISION,
        volume BIGINT,
        PRIMARY KEY (timestamp, symbol)
    );
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS news (
        timestamp TIMESTAMPTZ,
        symbol TEXT,
        headline TEXT,
        sentiment DOUBLE PRECISION,
        source TEXT
    );
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS signals (
        timestamp TIMESTAMPTZ,
        symbol TEXT,
        signal TEXT,
        confidence DOUBLE PRECISION,
        holding_days INTEGER,
        target DOUBLE PRECISION,
        stop_loss DOUBLE PRECISION,
        reason TEXT
    );
    """))
