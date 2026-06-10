import threading
from datetime import datetime

import streamlit as st

from app.ingestion.scheduler import run_scheduler
from app.main import run

# -----------------------------
# START SCHEDULER ONCE
# -----------------------------
if "scheduler_started" not in st.session_state:
    scheduler_thread = threading.Thread(
        target=run_scheduler,
        daemon=True
    )
    scheduler_thread.start()

    st.session_state["scheduler_started"] = True

# -----------------------------
# UI
# -----------------------------
st.title("AI Swing Trading Dashboard")

if st.button("Run Main Method"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Running main() at {now}")
    run()
    st.session_state["last_run"] = now

    st.success("main() executed manually")

st.write("Last Run:", st.session_state.get("last_run", "Never"))
