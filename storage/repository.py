from storage.db import get_connection
from core.state import SharedState
from datetime import datetime


def save_workflow(state: SharedState):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO workflows
    VALUES (?, ?, ?, ?)
    """, (
        state.request_id,
        state.status,
        state.model_dump_json(),
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()


def get_workflow(request_id: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT state_json FROM workflows
    WHERE request_id = ?
    """, (request_id,))

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return SharedState.model_validate_json(row[0])