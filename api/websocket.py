from fastapi import APIRouter, WebSocket
from storage.repository import get_workflow
import asyncio

router = APIRouter()


@router.websocket("/ws/{request_id}")
async def workflow_updates(
    websocket: WebSocket,
    request_id: str
):

    await websocket.accept()

    try:

        while True:

            workflow = get_workflow(request_id)

            if workflow:

                await websocket.send_json({
                    "request_id": workflow.request_id,
                    "status": workflow.status,
                    "retry_count": workflow.retry_count,
                    "approval_status": workflow.approval_status,
                    "error": workflow.error,
                    "final_output": workflow.final_output
                })

                if workflow.status in [
                    "completed",
                    "failed"
                ]:
                    break

            await asyncio.sleep(2)

    except Exception as e:

        await websocket.close()