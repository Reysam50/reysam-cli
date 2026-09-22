import asyncio
import itertools
from typing import Optional

from ..runner import run_tool
from ..tool import Tool
from .task import Task, TaskState


class ExecutionManager:
    """Owns the lifecycle of running tasks.

    A Task wraps a single tool invocation. Starting a task schedules it on
    the asyncio event loop and returns immediately - the caller does not
    block waiting for the tool to finish.
    """

    def __init__(self):
        self._tasks: dict[str, Task] = {}
        self._id_counter = itertools.count(1)

    def start(self, tool: Tool, args: list[str]) -> Task:
        """Create and schedule a new task for the given tool. Returns immediately."""
        task_id = str(next(self._id_counter))
        task = Task(id=task_id, tool=tool, args=args)
        self._tasks[task_id] = task

        task._asyncio_task = asyncio.create_task(self._run(task))
        return task

    async def _run(self, task: Task) -> None:
        task.state = TaskState.RUNNING
        try:
            loop = asyncio.get_running_loop()
            exit_code = await loop.run_in_executor(None, run_tool, task.tool, task.args)
            task.exit_code = exit_code
            task.state = TaskState.COMPLETED
        except asyncio.CancelledError:
            task.state = TaskState.CANCELLED
            raise
        except Exception as exc:
            task.error = str(exc)
            task.state = TaskState.FAILED

    def get(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def all(self) -> list[Task]:
        return list(self._tasks.values())

    def cancel(self, task_id: str) -> bool:
        """Request cancellation of a task. Returns False if the task doesn't exist
        or has already finished."""
        task = self._tasks.get(task_id)
        if task is None or task._asyncio_task is None:
            return False
        return task._asyncio_task.cancel()