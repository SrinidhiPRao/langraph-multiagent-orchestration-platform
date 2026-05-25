#US-03: Shared State Schema
from typing import Annotated, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime,timezone
import operator,uuid


#Task Types
TaskType = Literal["research", "coding", "review", "writing", "unknown"]

#Agent Names
AgentName = Literal["supervisor", "researcher", "coder", "reviewer", "writer"]

#Workflow status
WorkflowStatus = Literal["pending","running","completed","failed"]

class AgentMessage(BaseModel):
    agent: AgentName
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskResult(BaseModel):
    agent: AgentName
    task_type: TaskType
    output: Any
    success: bool
    error: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SharedState(BaseModel):
  
    #request metadata
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    user_id: str = ""

    # The original user request
    user_request: str = ""

    # Supervisor-classified task type
    task_type: TaskType = "unknown"

    # Which agent should handle this task
    next_agent: AgentName | None = None
    
    #status
    status: WorkflowStatus = "pending"
    # All messages exchanged during the workflow
    messages: Annotated[list[AgentMessage], operator.add] = Field(default_factory=list)

    # Results from specialist agents
    results: Annotated[list[TaskResult], operator.add] = Field(default_factory=list)

    # Final consolidated output
    final_output: dict[str, Any] = Field(default_factory=dict)

    # Error info if something went wrong
    error: str | None = None
    retry_count: int = 0
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
