try:
    from multi_agent_task_manager.db.firestore import get_db
except ImportError:
    from db.firestore import get_db

db = get_db()

# --- ADD TASK ---

def add_task(title: str, due_date: str = "") -> dict:
    task = {
        "title": title,
        "due_date": due_date,
        "status": "pending"
    }

    db.collection("tasks").add(task)

    return {"message": f"Task '{title}' saved ✅"}


# --- GET TASKS ---

def get_tasks() -> dict:
    docs = db.collection("tasks").stream()

    tasks = []
    for doc in docs:
        task = doc.to_dict()
        task["id"] = doc.id
        tasks.append(task)

    return {"tasks": tasks}


# --- UPDATE TASK ---

def update_task(task_id: str, status: str) -> dict:
    db.collection("tasks").document(task_id).update({
        "status": status
    })

    return {"message": f"Task {task_id} updated to {status} ✅"}