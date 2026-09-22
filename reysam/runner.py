from __future__ import annotations

from typing import Sequence

from .discovery import Tool


def run_tool(tool: Tool, args: Sequence[str]) -> int:
    """Run a discovered tool and return its exit code."""
    result = tool.module.main(list(args))

    if result is None:
        return 0
    if isinstance(result, int):
        return result

    raise TypeError(
        f"Tool '{tool.name}' returned {type(result).__name__}; expected int or None."
    )
