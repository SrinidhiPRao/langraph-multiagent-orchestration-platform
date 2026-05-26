from core.state import SharedState
from storage.repository import (
    save_workflow,
    get_workflow
)


def persist_state(state: SharedState):

    save_workflow(state)


def load_state(request_id: str):

    return get_workflow(request_id)