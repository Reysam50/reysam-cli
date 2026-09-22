from .tool import Tool


def run_tool(tool: Tool, args: list[str]) -> int:
    """Run a Reysam tool with the supplied arguments."""

    result = tool.module.main(args)

    if isinstance(result, int):
        return result

    return 0