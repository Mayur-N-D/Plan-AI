try:
    from multi_agent_task_manager.db.firestore import get_db
except ImportError:
    from db.firestore import get_db

db = get_db()

# --- CREATE EVENT ---

def create_event(title: str, datetime: str = "") -> dict:
    event = {
        "title": title,
        "datetime": datetime
    }

    db.collection("events").add(event)

    return {"message": f"Event '{title}' scheduled ✅"}


# --- GET EVENTS ---

def get_events() -> dict:
    docs = db.collection("events").stream()

    events = []
    for doc in docs:
        event = doc.to_dict()
        event["id"] = doc.id
        events.append(event)

    return {"events": events}