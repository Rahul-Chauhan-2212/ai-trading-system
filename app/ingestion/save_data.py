from app.database.db import engine


def save_to_db(dataframe):
    dataframe.to_sql(
        'ohlcv',
        engine,
        if_exists='append',
        index=False
    )
