from app.ingestion.fetch_nse_data import NSEDataFetcher
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

fetcher = NSEDataFetcher()

SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS"
]


# ==========================================================
# DAILY JOB
# ==========================================================
def run_daily_sync():
    print("=" * 50)
    print("STARTING NSE SYNC")
    print("=" * 50)

    fetcher.sync_all_symbols(SYMBOLS)

    print("=" * 50)
    print("NSE SYNC COMPLETED")
    print("=" * 50)


# ==========================================================
# RUN DAILY 6 PM
# ==========================================================
scheduler.add_job(
    run_daily_sync,
    trigger="cron",
    hour=18,
    minute=0
)

print("Scheduler Started")

# run immediately also
run_daily_sync()

scheduler.start()
