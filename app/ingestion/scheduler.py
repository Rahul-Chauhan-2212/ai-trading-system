import schedule
import time
from app.main import run


def run_scheduler():
    schedule.every(1).minutes.do(run)

    # schedule.every().monday.at("21:00").do(run)
    # schedule.every().tuesday.at("21:00").do(run)
    # schedule.every().wednesday.at("21:00").do(run)
    # schedule.every().thursday.at("21:00").do(run)
    # schedule.every().friday.at("21:00").do(run)

    while True:
        schedule.run_pending()
        time.sleep(60)
