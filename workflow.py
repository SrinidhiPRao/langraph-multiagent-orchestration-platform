#US-2,3: Multi-Agent Architecture,Shared State Schema
#Assembles StateGraph

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from langgraph.graph import StateGraph, END

from core.state import SharedState
from agents.supervisor import supervisor_node, supervisor_router
from agents.specialists import (
    researcher_node,
    coder_node,
    reviewer_node,
    writer_node,
)

#Build and compile the multi-agent LangGraph workflow.
def build_graph() -> StateGraph:
    graph = StateGraph(SharedState)

    #Add nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("coder",      coder_node)
    graph.add_node("reviewer",   reviewer_node)
    graph.add_node("writer",     writer_node)

    #Entry point
    graph.set_entry_point("supervisor")

    #Conditional routing from supervisor
    graph.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {
            "researcher": "researcher",
            "coder":      "coder",
            "reviewer":   "reviewer",
            "writer":     "writer",
        },
    )

    #Each specialist goes to END
    graph.add_edge("researcher", END)
    graph.add_edge("coder",      END)
    graph.add_edge("reviewer",   END)
    graph.add_edge("writer",     END)
    return graph.compile()


# Singleton compiled graph
orchestrator = build_graph()

def run(user_request: str,session_id: str = "",user_id: str = "",) -> SharedState:
    initial_state = SharedState(
        user_request=user_request,
        session_id=session_id,
        user_id=user_id,
    )
    final_state = orchestrator.invoke(initial_state)
    return SharedState(**final_state)
