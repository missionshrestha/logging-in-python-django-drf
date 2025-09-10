# api/my_jobs.py
import sys, os, logging
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path
from scoped_logging.decorators import scoped_function_log
from scoped_logging.context import get_logger, start_scope, end_scope

# Ensure the "app" logger actually records INFO
logging.getLogger("app").setLevel(logging.INFO)

@scoped_function_log("nightly-maintenance")
def run_job():
    logger = get_logger(__name__)
    logger.info("🔧 Doing background job…")
    # ... your job code ...

if __name__ == "__main__":
    # Optional: wrap the whole script in a "task" scope so you also get a task log file
    start_scope("task", Path("logs"), "nightly-maintenance", base_logger_name="app", reuse_if_exists=False)
    try:
        run_job()  # this also creates a functions-scope file via the decorator
        print("✅ Job finished!")
    finally:
        logfile = end_scope("app")
        if logfile:
            print(f"🗂️ Task log file: {logfile}")
