import asyncio

import pytest

from reysam.execution.manager import ExecutionManager
from reysam.execution.task import TaskState
from reysam.tool import Tool


def make_tool(module):
    return Tool(
        name="test",
        description="Test tool.",
        category="testing",
        module=module,
        path=None,
    )


class SlowModule:
    """A fake tool that blocks briefly, so we have time to observe RUNNING
    state and to cancel it before it finishes."""

    def main(self, args):
        import time
        time.sleep(0.2)
        return 0


class FailingModule:
    def main(self, args):
        raise ValueError("boom")


@pytest.mark.asyncio
async def test_task_completes_successfully():
    manager = ExecutionManager()
    tool = make_tool(SlowModule())

    task = manager.start(tool, [])
    assert task.state in (TaskState.PENDING, TaskState.RUNNING)

    await task._asyncio_task

    assert task.state == TaskState.COMPLETED
    assert task.exit_code == 0


@pytest.mark.asyncio
async def test_task_records_failure():
    manager = ExecutionManager()
    tool = make_tool(FailingModule())

    task = manager.start(tool, [])
    await task._asyncio_task

    assert task.state == TaskState.FAILED
    assert "boom" in task.error


@pytest.mark.asyncio
async def test_task_can_be_cancelled():
    manager = ExecutionManager()
    tool = make_tool(SlowModule())

    task = manager.start(tool, [])
    await asyncio.sleep(0.01)  # let it reach RUNNING
    manager.cancel(task.id)

    with pytest.raises(asyncio.CancelledError):
        await task._asyncio_task

    assert task.state == TaskState.CANCELLED


@pytest.mark.asyncio
async def test_manager_tracks_multiple_tasks():
    manager = ExecutionManager()
    tool = make_tool(SlowModule())

    task_a = manager.start(tool, [])
    task_b = manager.start(tool, [])

    assert manager.get(task_a.id) is task_a
    assert {t.id for t in manager.all()} == {task_a.id, task_b.id}

    await task_a._asyncio_task
    await task_b._asyncio_task