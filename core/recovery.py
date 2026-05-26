from datetime import datetime, timezone

from core.state import SharedState, AgentMessage

from observability.metrics import workflow_retry


def recovery_node(state: SharedState):

    if state.retry_count >= state.max_retries:

        return {
            "status": "failed",
            "error": "Maximum retries exceeded",
            "ended_at": datetime.now(timezone.utc),
            "messages": [
                AgentMessage(
                    agent="recovery",
                    content="Workflow failed permanently."
                )
            ]
        }

    workflow_retry.inc()

    return {
        "retry_count": state.retry_count + 1,
        "needs_recovery": False,
        "messages": [
            AgentMessage(
                agent="recovery",
                content=f"Retrying {state.current_agent}"
            )
        ],
        "next_agent": state.current_agent
    }