import requests
import feedparser
from typing import List, Dict


def fetch_events(feed_url: str) -> List[Dict[str, str]]:
    """Fetch events from an RSS or iCal feed."""
    resp = requests.get(feed_url, timeout=10)
    resp.raise_for_status()
    parsed = feedparser.parse(resp.text)
    events = []
    for entry in parsed.entries:
        events.append(
            {
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "tags": [t.term for t in entry.get("tags", [])],
            }
        )
    return events


def filter_events(events: List[Dict[str, str]], keywords: List[str]) -> List[Dict[str, str]]:
    """Return events containing any keyword in the title or tags."""
    kw_lower = [k.lower() for k in keywords]
    filtered = []
    for event in events:
        title = event.get("title", "").lower()
        tags = [t.lower() for t in event.get("tags", [])]
        if any(k in title or k in tags for k in kw_lower):
            filtered.append(event)
    return filtered
