from fastapi import FastAPI
from pydantic import BaseModel

from agent import root_agent

app = FastAPI()


# ✅ Root endpoint (fixes 404 issue)
@app.get("/")
def home():
    return {"message": "Task Manager API running 🚀"}


# ✅ Request model
class ChatRequest(BaseModel):
    message: str


# ✅ Chat endpoint (fully fixed)
@app.post("/chat")
async def chat(req: ChatRequest):
    response = ""

    try:
        async for event in root_agent.run_async(req.message):
            # Debug (optional)
            print("EVENT:", event)

            # Handle different ADK event formats safely
            if isinstance(event, dict):
                if "content" in event and event["content"]:
                    response += event["content"]

                elif "output_text" in event and event["output_text"]:
                    response += event["output_text"]

    except Exception as e:
        return {"error": str(e)}

    return {"response": response.strip()}