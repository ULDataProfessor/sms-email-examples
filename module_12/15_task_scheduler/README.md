# Task Scheduler

## Project Overview
`scheduled_task.py` demonstrates running a simple job on a schedule using the `schedule` library. It prints a timestamp every minute until the program is terminated.

## Variables
The schedule interval is set within the script using `schedule.every(1).minutes` but can be modified to any frequency.

## Instructions
Install the library with `pip install schedule` and execute `python scheduled_task.py`. The script will run indefinitely, printing the current time once per minute.

## Explanation
The `schedule` package offers a lightweight way to run tasks at regular intervals. It is useful for small automation jobs where a full cron setup is unnecessary.
