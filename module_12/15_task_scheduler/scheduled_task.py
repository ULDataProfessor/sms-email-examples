"""Run a job every minute."""
from __future__ import annotations

import schedule
import time
from datetime import datetime


def job() -> None:
    print(f"Job executed at {datetime.now():%Y-%m-%d %H:%M:%S}")


def main() -> None:
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
