import os
import logging
import google.cloud.logging
from dotenv import load_dotenv
# ✅ FIX: dual import support
try:
    # ADK mode
    from multi_agent_task_manager.tools.task_tools import add_task, get_tasks, update_task
    from multi_agent_task_manager.tools.calendar_tools import create_event, get_events
    from multi_agent_task_manager.tools.notes_tools import save_note, get_notes
except ImportError:
    # FastAPI / local mode
    from tools.task_tools import add_task, get_tasks, update_task
    from tools.calendar_tools import create_event, get_events
    from tools.notes_tools import save_note, get_notes

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

# --- Setup Logging and Environment ---

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")

# --- TOOL: Save user prompt ---

def add_prompt_to_state(
    tool_context: ToolContext, prompt: str
) -> dict:
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[STATE] Saved PROMPT: {prompt}")
    return {"status": "saved"}

# --- AGENT 1: Intent Analyzer ---
intent_agent = Agent(
    name="intent_analyzer",
    model=model_name,
    description="Detects user intent",
    instruction="""
    Analyze the PROMPT and classify it strictly as:
    - TASK → if user wants to add/do/manage tasks
    - CALENDAR → scheduling, meetings, events
    - NOTES → saving or retrieving notes

    Output ONLY one word: TASK / CALENDAR / NOTES

    PROMPT:
    { PROMPT }
    """,
    output_key="intent"
)


task_agent = Agent(
    name="task_agent",
    model=model_name,
    description="Handles task operations",
    instruction="""
    You manage tasks using tools.

    Based on user PROMPT:

    1. If user wants to ADD → use add_task
    2. If user wants to VIEW → use get_tasks
    3. If user wants to UPDATE → use update_task

    Extract required fields carefully.

    PROMPT:
    { PROMPT }
    """,
    tools=[add_task, get_tasks, update_task],
    output_key="task_result"
)

calendar_agent = Agent(
    name="calendar_agent",
    model=model_name,
    description="Handles calendar operations",
    instruction="""
    You manage calendar events.

    Based on user PROMPT:

    - If user wants to schedule → use create_event
    - If user wants to view events → use get_events

    Extract title and datetime properly.

    PROMPT:
    { PROMPT }
    """,
    tools=[create_event, get_events],
    output_key="calendar_result"
)

notes_agent = Agent(
    name="notes_agent",
    model=model_name,
    description="Handles notes operations",
    instruction="""
    You manage notes.

    Based on user PROMPT:

    - If user wants to save a note → use save_note
    - If user wants to view notes → use get_notes

    Extract content properly.

    PROMPT:
    { PROMPT }
    """,
    tools=[save_note, get_notes],
    output_key="notes_result"
)


# Orchestrator agent
orchestrator_agent = Agent(
    name="orchestrator",
    model=model_name,
    description="Routes request to correct agent",
    instruction="""
    You are an orchestrator.

    Rules:
    - TASK → task_agent
    - CALENDAR → calendar_agent
    - NOTES → notes_agent

    Call ONLY ONE agent.
    Do not generate extra text.

    INTENT:
    { intent }
    """,
    sub_agents=[]
)

orchestrator_agent.sub_agents = [task_agent, calendar_agent, notes_agent]

# --- AGENT 2: Response Generator ---

response_agent = Agent(
    name="response_generator",
    model=model_name,
    description="Generates final response",
    instruction="""
    You are a helpful assistant.

    Based on the previous action:

    - If a task was created → confirm it
    - If an event was scheduled → confirm it
    - Otherwise respond helpfully

    Do NOT rely on fixed variable names.
    """
)

# --- WORKFLOW ---

workflow = SequentialAgent(
    name="task_workflow",
    description="Smart routing workflow",
    sub_agents=[
        intent_agent,
        orchestrator_agent,
        response_agent
    ]
)

# --- ROOT AGENT ---

root_agent = Agent(
    name="task_manager_assistant",
    model=model_name,
    description="Main entry point",
    instruction="""
    - Greet the user
    - ALWAYS save user input using add_prompt_to_state
    - Then pass control to the workflow
    """,
    tools=[add_prompt_to_state],
    sub_agents=[workflow]
)