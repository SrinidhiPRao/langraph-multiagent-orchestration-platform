from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.workflow import run
from storage.repository import (
    save_workflow,
    get_workflow
)

router = APIRouter()


class WorkflowRequest(BaseModel):
    query: str


@router.post("/workflow/start")
def start_workflow(payload: WorkflowRequest):

    query = payload.query

    result = run(query)

    save_workflow(result)

    return {
        "message": "Workflow started",
        "request_id": result.request_id,
        "status": result.status,
        "result": result
    }

@router.get("/workflow/{request_id}")
def workflow_status(request_id: str):

    workflow = get_workflow(request_id)

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return workflow


@router.post("/workflow/{request_id}/approve")
def approve_workflow(request_id: str):

    workflow = get_workflow(request_id)

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    workflow.approval_status = "approved"
    workflow.status = "running"

    save_workflow(workflow)

    return {
        "message": "Workflow approved",
        "request_id": request_id
    }


@router.post("/workflow/{request_id}/reject")
def reject_workflow(request_id: str):

    workflow = get_workflow(request_id)

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    workflow.approval_status = "rejected"
    workflow.status = "failed"

    save_workflow(workflow)

    return {
        "message": "Workflow rejected",
        "request_id": request_id
    }