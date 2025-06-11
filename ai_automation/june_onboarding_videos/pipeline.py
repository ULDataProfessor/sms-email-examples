"""Generate onboarding videos for June 2025 signups."""

from __future__ import annotations

import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict

import boto3

from crm_client import CRMClient
from video_client import VideoClient
from mailer import send_email
from report import Report, Result

START_DATE = "2025-06-01"
END_DATE = "2025-06-30"
VIDEO_TEMPLATE_ID = os.getenv("VIDEO_TEMPLATE_ID", "default")
S3_BUCKET = os.getenv("S3_BUCKET")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "5"))


class RateLimiter:
    def __init__(self, rate: int, per: float) -> None:
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.monotonic()
        self.lock = threading.Lock()

    def wait(self) -> None:
        while True:
            with self.lock:
                current = time.monotonic()
                elapsed = current - self.last_check
                self.last_check = current
                self.allowance += elapsed * (self.rate / self.per)
                if self.allowance > self.rate:
                    self.allowance = self.rate
                if self.allowance >= 1:
                    self.allowance -= 1
                    return
            time.sleep(0.01)


def upload_video(s3_client: boto3.client, customer_id: str, data: bytes) -> str:
    key = f"onboarding/{customer_id}.mp4"
    s3_client.put_object(Bucket=S3_BUCKET, Key=key, Body=data, ContentType="video/mp4")
    return f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"


def process_customer(customer: Dict[str, str], video_client: VideoClient, s3_client: boto3.client, limiter: RateLimiter, report: Report) -> None:
    start = time.monotonic()
    cid = str(customer.get("id"))
    try:
        name = customer.get("name", "Customer")
        plan = customer.get("plan", "our service")
        email = customer.get("email")
        script = f"Hi {name}, welcome to {plan}! We're excited to have you."
        limiter.wait()
        video_data = video_client.generate_video(script, VIDEO_TEMPLATE_ID)
        link = upload_video(s3_client, cid, video_data)
        if email:
            body = f"<p>Your onboarding video is ready: <a href='{link}'>watch here</a>.</p>"
            send_email(email, "Welcome to our service", body)
        report.add(Result(cid, True, time.monotonic() - start))
    except Exception as exc:  # pragma: no cover - simple example
        report.add(Result(cid, False, time.monotonic() - start, str(exc)))


def main() -> None:
    if not S3_BUCKET:
        raise EnvironmentError("S3_BUCKET must be set")
    crm = CRMClient()
    video_client = VideoClient()
    s3_client = boto3.client("s3")
    limiter = RateLimiter(rate=5, per=1.0)
    report = Report()

    customers = crm.query_customers(START_DATE, END_DATE)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_customer, c, video_client, s3_client, limiter, report) for c in customers]
        for f in as_completed(futures):
            pass

    print(report.summary())


if __name__ == "__main__":
    main()

