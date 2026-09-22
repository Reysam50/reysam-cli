from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ..tool import Tool


class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    id: str
    tool: Tool
    args: list[str]
    state: TaskState = TaskState.PENDING
    exit_code: Optional[int] = None
    error: Optional[str] = None

    # Internal handle to the underlying asyncio.Task, used for cancellation.
    # Not part of the task's public "data", so it's excluded from repr/equality.
    _asyncio_task: object = field(default=None, repr=False, compare=False)