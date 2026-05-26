from langgraph.graph import StateGraph, END

from core.persistence import persist_state
from core.state import SharedState

from agents.supervisor import (
    supervisor_node,
    supervisor_router
)

from agents.specialists import (
    researcher_node,
    coder_node,
    reviewer_node,
    writer_node
)

from observability.metrics import (
    workflow_success,
    workflow_failure,
    workflow_retry
)

from core.recovery import recovery_node
from core.approval import approval_node


def should_recover(state: SharedState):

    if state.error:
        return "recovery"

    return "continue"


def review_router(state: SharedState):

    if state.error:
        return "recovery"

    return "writer"


def recovery_router(state: SharedState):

    # Safe fallback routing
    if state.next_agent:
        return state.next_agent

    return "writer"


def build_graph():

    graph = StateGraph(SharedState)

    # Nodes
    graph.add_node("supervisor", supervisor_node)

    graph.add_node("researcher", researcher_node)

    graph.add_node("coder", coder_node)

    graph.add_node("reviewer", reviewer_node)

    graph.add_node("writer", writer_node)

    graph.add_node("recovery", recovery_node)

    graph.add_node("approval", approval_node)

    # Entry point
    graph.set_entry_point("supervisor")

    # Supervisor Routing
    graph.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {
            "researcher": "researcher",
            "coder": "coder",
            "reviewer": "reviewer",
            "writer": "writer"
        }
    )

    # Research Flow
    graph.add_edge("researcher", END)

    # Coding Flow
    graph.add_conditional_edges(
        "coder",
        should_recover,
        {
            "recovery": "recovery",
            "continue": "reviewer"
        }
    )

    # Review Flow
    graph.add_conditional_edges(
        "reviewer",
        review_router,
        {
            "recovery": "recovery",
            "writer": "writer"
        }
    )

    # Writer Ends Workflow
    graph.add_edge("writer", END)

    # Recovery Routing
    graph.add_conditional_edges(
        "recovery",
        recovery_router,
        {
            "coder": "coder",
            "reviewer": "reviewer",
            "writer": "writer"
        }
    )

    return graph.compile()


# Compile Graph
orchestrator = build_graph()


def run(user_request: str):

    initial_state = SharedState(
        user_request=user_request
    )

    try:

        # Execute Workflow
        result = orchestrator.invoke(initial_state)

        # Convert to SharedState
        final_state = SharedState(**result)

        # Persist Workflow
        persist_state(final_state)

        # Success Metric
        if final_state.status == "completed":
            workflow_success.inc()

        return final_state

    except Exception as e:

        # Failure Metric
        workflow_failure.inc()

        raise e