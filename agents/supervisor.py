#US-4: Supervisor Agent
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.state import SharedState, AgentMessage, TaskType


#Keyword-based classifier
ROUTING_RULES: dict[str, list[str]] = {
    "coding":   ["code", "implement", "algorithm", "function to", "write a function",
                 "write a class", "debug", "fix bug", "script", "program", "develop",
                 "build", "class", "def ", "sort", "binary search"],
    "review":   ["review", "check", "validate", "evaluate", "quality",
                 "feedback", "assess", "inspect"],
    "research": ["research", "find", "search", "what is", "explain",
                 "summarize", "look up", "gather", "information"],
    "writing":  ["write", "draft", "report", "document", "content",
                 "article", "blog", "essay", "readme", "generate text"],
}

#Priority order for tie-breaking
PRIORITY_ORDER = ["coding", "review", "research", "writing"]

def classify_task(user_request: str) -> TaskType:
    request_lower = user_request.lower()
    scores: dict[str, int] = {task: 0 for task in ROUTING_RULES}
    for task_type, keywords in ROUTING_RULES.items():
        for keyword in keywords:
            if keyword.lower() in request_lower:
                scores[task_type] += 1
    max_score = max(scores.values())
    # If no keywords matched at all, return unknown
    if max_score == 0:
        return "unknown"
    # Among tied winners, pick highest-priority one
    for task_type in PRIORITY_ORDER:
        if scores[task_type] == max_score:
            return task_type 
    return "writing"


def supervisor_node(state: SharedState) -> dict:
    user_request = state.user_request
    task_type = classify_task(user_request)

    #Map task type to agent name
    agent_map = {
        "research": "researcher",
        "coding":   "coder",
        "review":   "reviewer",
        "writing":  "writer",
        "unknown":  "writer",  # fallback
    }

    next_agent = agent_map[task_type]

    message = AgentMessage(
        agent="supervisor",
        content=(
            f"Task classified as '{task_type}'. "
            f"Routing to '{next_agent}' agent."
        ),
        metadata={"task_type": task_type, "next_agent": next_agent},
    )

    return {
        "task_type": task_type,
        "next_agent": next_agent,
        "messages": [message],
        "status": "running"
    }
#Conditional edge function
def supervisor_router(state: SharedState) -> str:
    return state.next_agent or "writer"
