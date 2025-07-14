import os
import requests
from datetime import datetime

# hard-wired API key
EVENTREG_API_KEY = os.getenv("EVENTREG_API_KEY")
EVENTS_URL       = "https://eventregistry.org/api/v1/event/getEvents"

def get_events_text(keyword, page=1, count=10):
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    payload = {
        "apiKey":                 EVENTREG_API_KEY,
        "resultType":             "events",
        "keyword":                keyword,
        "eventsPage":             page,
        "eventsCount":            count,
        "eventsSortBy":           "rel",
        "eventsSortByAsc":        False,
        "eventsArticleBodyLen":   -1,
        "forceMaxDataTimeWindow": 31
    }

    resp = requests.post(EVENTS_URL, json=payload)
    if not resp.ok:
        return f"Error fetching events: HTTP {resp.status_code}"

    body   = resp.json()
    events = body.get("events", {}).get("results", [])

    if not events:
        return f"No events found for “{keyword}.”"

    # build your header + empty line
    lines = [f"Top Events for “{keyword}” — {today_str}", ""]

    for i, ev in enumerate(events, 1):
        # unwrap title if it's a dict, else take it directly
        raw_title = ev.get("title") or ev.get("label", "")
        if isinstance(raw_title, dict):
            title = raw_title.get("eng") or next(iter(raw_title.values()))
        else:
            title = raw_title

        # only append the numbered headline
        lines.append(f"{i}. {title}")

    return "\n".join(lines)
