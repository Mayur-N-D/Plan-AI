# 🤖 Plan-AI — Multi-Functional AI Agent

Plan-AI is a modular AI agent system designed to intelligently manage tasks, calendar events, and notes using a structured multi-agent workflow. It leverages a sequential agent architecture to analyze user intent and execute the appropriate actions via integrated tools.

---

## 🚀 Live Demo  
🔗 View Agent:  https://multi-agent-task-manager-76736746121.asia-south1.run.app

---

## 🚀 Overview

Plan-AI acts as a personal productivity assistant, capable of:

- Understanding user intent from natural language prompts
- Routing requests to specialized agents
- Performing task management, scheduling, and note-taking operations

The system is built using Google ADK agents, making it scalable and adaptable for real-world AI applications.

---

## 🧠 Architecture

The project follows a multi-agent pipeline architecture:

User Input → Intent Analyzer → Specialized Agent → Tool Execution → Response

🔹 Core Flow:

1. User provides a prompt
2. Intent Analyzer classifies the request
3. Request is routed to:
- Task Agent
- Calendar Agent
- Notes Agent
5. Corresponding tools are executed
6. Output is returned to the user

---

## ⚙️ Features
1. ✅ Intelligent Intent Detection
- Classifies user input into: TASK, CALENDAR, NOTES

2. 📋 Task Management
- Add tasks
- Retrieve tasks
- Update existing tasks
  
3. 📅 Calendar Integration
- Create events
- Fetch scheduled events

4. 📝 Notes Management
- Save notes
- Retrieve stored notes
  
5. 🔄 Modular Design
- Easily extendable with new agents or tools
- Supports both: ADK mode, Local/FastAPI mode

6. ☁️ Cloud Logging
- Integrated with Google Cloud Logging for monitoring

---

## 🏗️ Project Structure

- Plan-AI/
- │── agent.py                # Main multi-agent workflow
- │── tools/
- │   ├── task_tools.py       # Task operations
- │   ├── calendar_tools.py   # Calendar operations
- │   ├── notes_tools.py      # Notes operations
- │── requirements.txt        # Dependencies
- │── .env                    # Environment variables

---

## 🧩 Key Components

🔹 Intent Analyzer Agent
- Classifies user input into predefined categories
- Ensures correct routing of requests

🔹 Task Agent
- Handles all task-related operations
- Uses task tools for CRUD actions

🔹 Calendar Agent
- Manages scheduling and events

🔹 Notes Agent
- Handles note storage and retrieval

🔹 ToolContext State Management
- Maintains session state (e.g., user prompt)

---

### ⭐ Don’t forget to give this project a star if you like it!
