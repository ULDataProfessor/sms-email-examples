"""Simple CRM API client used by the onboarding video pipeline."""

from __future__ import annotations

import os
import requests
from typing import Dict, List

CRM_API_URL = os.getenv("CRM_API_URL")
CRM_API_KEY = os.getenv("CRM_API_KEY")


class CRMClient:
    """Client for querying customer records from the CRM service."""

    def __init__(self) -> None:
        if not CRM_API_URL or not CRM_API_KEY:
            raise EnvironmentError("CRM_API_URL and CRM_API_KEY must be set")
        self.base_url = CRM_API_URL.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {CRM_API_KEY}"})

    def query_customers(self, start_date: str, end_date: str) -> List[Dict[str, str]]:
        """Return all customers with signups between start and end dates."""
        customers: List[Dict[str, str]] = []
        params = {"start_date": start_date, "end_date": end_date}
        url = f"{self.base_url}/customers"
        while url:
            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            customers.extend(data.get("results", []))
            url = data.get("next_page")
            params = None  # next_page already contains query parameters
        return customers
