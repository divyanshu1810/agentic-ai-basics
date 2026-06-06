import os
from datetime import date, datetime
import requests
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Assistant Service")

EVENTS_URL = os.getenv("EVENT_SERVICE_URL", "http://localhost:8001")

@app.get("/", tags=["health"])
def health():
    return {"service": "assistant-service", "status": "ok"}

def fetch_events():
    try:
        r = requests.get(f"{EVENTS_URL}/events/", timeout=3)
        r.raise_for_status()	
        return r.json()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Event service unavailable")

@app.post("/assistant")
def assistant_post(q: str = Query(..., description="Ask about events")):
    # Reuse same logic as GET for simplicity
    return _answer(q)

@app.get("/assistant")
def assistant_get(q: str = Query(..., description="Ask about events")):
    return _answer(q)
    
def _answer(q: str):
    q_low = q.lower().strip()
    events = fetch_events()
    # Normalize date fields to date objects for comparison
    for e in events:
        if isinstance(e.get("date"), str):
            try:
                e["_date_obj"] = datetime.strptime(e["date"], "%Y-%m-%d").date()
            except ValueError:
                e["_date_obj"] = None
        else:
            e["_date_obj"] = e.get("date")
    today = date.today()
    # 1) Next event
    if "next event" in q_low or "first upcoming" in q_low:
        upcoming = [e for e in events if e.get("_date_obj") and e["_date_obj"] >= today]
        upcoming.sort(key=lambda x: x["_date_obj"])
        if not upcoming:
            return {"answer": "No upcoming events found."}
        e = upcoming[0]
        return {"answer": f"Next event is '{e['title']}' in {e['city']} on {e['date']}."}
    # 2) Upcoming events
    if "upcoming" in q_low or "future events" in q_low:
        upcoming = [e for e in events if e.get("_date_obj") and e["_date_obj"] >= today]
        upcoming.sort(key=lambda x: x["_date_obj"])
        if not upcoming:
            return {"answer": "No upcoming events found."}
        return {
            "answer": f"{len(upcoming)} upcoming event(s).",
            "events": [{"title": e["title"], "city": e["city"], "date": e["date"]} for e in upcoming]
        }
    # 3) Events by city
    if "in " in q_low:
        # crude city extraction: after 'in ' take the word(s)
        idx = q_low.rfind(" in ")
        city = q_low[idx + 4 :].strip().strip("?.,")
        by_city = [e for e in events if e["city"].lower() == city.lower()]
        if not by_city:
            return {"answer": f"No events found in {city}."}
        return {
            "answer": f"Found {len(by_city)} event(s) in {city}.",
            "events": [{"title": e["title"], "date": e["date"]} for e in by_city]
        }
    # 4) Events on a specific date (YYYY-MM-DD)
    import re
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", q_low)
    if m:
        dstr = m.group(1)
        on_date = [e for e in events if e.get("date") == dstr]
        if not on_date:
            return {"answer": f"No events scheduled on {dstr}."}
        return {
            "answer": f"Found {len(on_date)} event(s) on {dstr}.",
            "events": [{"title": e["title"], "city": e["city"]} for e in on_date]
        }
    # 5) Count
    if "how many" in q_low or "count" in q_low:
        return {"answer": f"There are {len(events)} total event(s)."}
    # Default: help
    return {
        "answer": "Try queries like: 'What is the next event?', 'Show upcoming events', 'Events in Chennai', 'Events on 2025-12-10', 'How many events are scheduled?'"
    }
