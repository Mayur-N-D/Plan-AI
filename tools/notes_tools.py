try:
    from multi_agent_task_manager.db.firestore import get_db
except ImportError:
    from db.firestore import get_db

db = get_db()

# --- SAVE NOTE ---

def save_note(content: str) -> dict:
    note = {
        "content": content
    }

    db.collection("notes").add(note)

    return {"message": "Note saved successfully 📝"}


# --- GET NOTES ---

def get_notes() -> dict:
    docs = db.collection("notes").stream()

    notes = []
    for doc in docs:
        note = doc.to_dict()
        note["id"] = doc.id
        notes.append(note)

    return {"notes": notes}