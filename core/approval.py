from core.state import SharedState, AgentMessage


def approval_node(state: SharedState):

    return {
        "status": "waiting_approval",
        "messages": [
            AgentMessage(
                agent="approval",
                content="Waiting for human approval"
            )
        ]
    }