from typing import Annotated, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import operator
import uuid


TaskType = Literal[
    "research",
    "coding",
    "review",
    "writing",
    "unknown"
]

AgentName = Literal[
    "supervisor",
    "researcher",
    "coder",
    "reviewer",
    "writer",
    "recovery",
    "approval"
]

WorkflowStatus = Literal[
    "pending",
    "running",
    "waiting_approval",
    "completed",
    "failed"
]


class AgentMessage(BaseModel):
    agent: AgentName
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class TaskResult(BaseModel):
    agent: AgentName
    task_type: TaskType
    output: Any
    success: bool
    error: str | None = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class SharedState(BaseModel):

    request_id: str = Field(
        default_factory=lambda: str(uuid.uuid4())
    )

    session_id: str = ""
    user_id: str = ""

    user_request: str = ""

    task_type: TaskType = "unknown"

    next_agent: AgentName | None = None

    current_agent: AgentName | None = None

    status: WorkflowStatus = "pending"

    retry_count: int = 0
    max_retries: int = 3

    needs_recovery: bool = False

    requires_approval: bool = False
    approval_status: str = "pending"
    approval_reason: str = ""

    messages: Annotated[
        list[AgentMessage],
        operator.add
    ] = Field(default_factory=list)

    results: Annotated[
        list[TaskResult],
        operator.add
    ] = Field(default_factory=list)

    final_output: dict[str, Any] = Field(default_factory=dict)

    error: str | None = None

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    ended_at: datetime | None = None