import yfinance as yf

NSE_STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "TATAMOTORS.NS"
]


def fetch_stock_data(symbol):
    data = yf.download(
        symbol,
        period="6mo",
        interval="1d"
    )

    data.reset_index(inplace=True)

    print(data.columns)

    data.columns = [col[0].lower() for col in data.columns]

    data = data.rename(columns={'index': 'timestamp'})

    print(data.columns)

    data.columns = [
        'timestamp',
        'close',
        'high',
        'low',
        'open',
        'volume'
    ]

    # Round OHLC prices to 2 decimal places
    price_columns = ['close', 'high', 'low', 'open']

    data[price_columns] = data[price_columns].round(2)

    data['symbol'] = symbol
    data['exchange'] = 'NSE'

    print(f"data fetched : symbol : {symbol}")
    print(data.head())
    return data
