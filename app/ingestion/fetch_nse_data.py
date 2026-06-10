from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import yfinance as yf

from app.database.db import (
    save_ohlcv,
    get_last_timestamp
)


class NSEDataFetcher:

    # ==========================================================
    # FETCH 2 YEARS DATA
    # ==========================================================
    def fetch_historical_data(self, symbol):

        print(f"Fetching 2 years data for {symbol}")

        end_date = datetime.now()

        start_date = end_date - timedelta(days=730)

        df = yf.download(
            symbol,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"),
            interval="1d",
            progress=False,
            auto_adjust=False
        )

        if df.empty:
            print(f"No data found for {symbol}")
            return

        df.reset_index(inplace=True)

        print(df.columns)

        # ======================================================
        # CLEAN COLUMNS
        # ======================================================
        df.columns = [col[0].lower() for col in df.columns]

        data = df.rename(columns={'index': 'timestamp'})

        # remove adj close
        if 'adj close' in data.columns:
            data.drop(columns=['adj close'], inplace=True)

        print(data.columns)

        # ======================================================
        # REORDER COLUMNS
        # ======================================================
        data = data[
            [
                'timestamp',
                'open',
                'high',
                'low',
                'close',
                'volume'
            ]
        ]

        # Round OHLC prices to 2 decimal places
        price_columns = ['close', 'high', 'low', 'open']

        data[price_columns] = data[price_columns].round(2)

        data['symbol'] = symbol
        data['exchange'] = 'NSE'

        save_ohlcv(data, symbol)

        print(f"Historical data stored for {symbol}")

    # ==========================================================
    # FETCH DAILY INCREMENTAL DATA
    # ==========================================================
    def fetch_incremental_data(self, symbol):

        last_timestamp = get_last_timestamp(symbol)

        # ==========================================
        # FIRST TIME RUN
        # ==========================================
        if not last_timestamp:
            print(f"{symbol} not initialized")

            self.fetch_historical_data(symbol)

            return

        fetch_from = last_timestamp + timedelta(days=1)

        print(f"Fetching latest data for {symbol}")

        df = yf.download(
            symbol,
            start=fetch_from.strftime("%Y-%m-%d"),
            interval="1d",
            progress=False,
            auto_adjust=False
        )

        if df.empty:
            print(f"No new data for {symbol}")

            return

        df.reset_index(inplace=True)

        print(df.columns)

        # ======================================================
        # CLEAN COLUMNS
        # ======================================================
        df.columns = [col[0].lower() for col in df.columns]

        data = df.rename(columns={'index': 'timestamp'})

        # remove adj close
        if 'adj close' in data.columns:
            data.drop(columns=['adj close'], inplace=True)

        print(data.columns)

        # ======================================================
        # REORDER COLUMNS
        # ======================================================
        data = data[
            [
                'timestamp',
                'open',
                'high',
                'low',
                'close',
                'volume'
            ]
        ]

        # Round OHLC prices to 2 decimal places
        price_columns = ['close', 'high', 'low', 'open']

        data[price_columns] = data[price_columns].round(2)

        data['symbol'] = symbol
        data['exchange'] = 'NSE'

        save_ohlcv(df, symbol)

        print(f"Incremental update completed for {symbol}")

    # ==========================================================
    # MAIN SYNC LOGIC
    # ==========================================================
    def sync_symbol(self, symbol):

        try:

            last_timestamp = get_last_timestamp(symbol)

            if not last_timestamp:
                self.fetch_historical_data(symbol)

            else:
                self.fetch_incremental_data(symbol)

        except Exception as e:

            print(f"Error syncing {symbol}: {e}")

    # ==========================================================
    # BULK SYNC
    # ==========================================================
    def sync_all_symbols(self, symbols):

        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.sync_symbol, symbols)
