from __future__ import annotations

import shlex
import sys
from pathlib import Path

from .discovery import discover_tools
from .registry import ToolRegistry
from .runner import run_tool
from .tool import Tool


def project_tools_dir() -> Path:
    """Return the tools directory bundled with the project."""

    return Path(__file__).resolve().parent.parent / "tools"


def print_tools(registry: ToolRegistry) -> None:
    """Print all discovered tools grouped by category."""

    tools = registry.all()

    if not tools:
        print("No tools discovered.")
        return

    categories: dict[str, list[Tool]] = {}

    for tool in tools:
        categories.setdefault(tool.category, []).append(tool)

    print("\nREYSAM TOOLBOX\n")

    for category in sorted(categories):
        print(f"{category}/")

        for tool in sorted(categories[category], key=lambda t: t.name):
            print(f"  {tool.name:<18} {tool.description}")

        print()

def print_category(registry: ToolRegistry, category: str) -> None:
    """Print all tools belonging to a category."""

    tools = registry.in_category(category)

    if not tools:
        print(f"Unknown category: {category}")
        return

    print(f"\n{category.upper()} TOOLS\n")

    for tool in sorted(tools, key=lambda t: t.name):
        print(f"  {tool.name:<18} {tool.description}")

    print()


def interactive(registry: ToolRegistry) -> int:
    """Run Reysam in interactive mode."""

    tools = registry.all()

    if not tools:
        print("No tools discovered.")
        return 1

    while True:
        print("\nREYSAM TOOLBOX")
        print("=" * 40)

        for index, tool in enumerate(tools, start=1):
            print(
                f"{index:>2}. "
                f"{tool.category}/{tool.name} - "
                f"{tool.description}"
            )

        print(" q. Quit")

        choice = input("\nSelect a tool: ").strip().lower()

        if choice == "q":
            return 0

        try:
            index = int(choice) - 1
            tool = tools[index]
        except (ValueError, IndexError):
            print("Invalid selection.")
            continue

        raw_args = input("Arguments (leave blank for none): ").strip()

        try:
            tool_args = shlex.split(raw_args)
        except ValueError as exc:
            print(f"Invalid arguments: {exc}")
            continue

        print()

        try:
            code = run_tool(tool, tool_args)
        except Exception as exc:
            print(f"Tool failed: {exc}")
            continue

        print(f"\nTool exited with code {code}.")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    tools = discover_tools(project_tools_dir())
    registry = ToolRegistry(tools)

    # No arguments → interactive mode.
    if not argv:
        return interactive(registry)

    # Explicit interactive mode.
    if argv in (["-i"], ["--interactive"]):
        return interactive(registry)

    # List discovered tools.
    if argv in (["--list"], ["-l"]):
        print_tools(registry)
        return 0

    # Category command:
    # reysam <category>
    if len(argv) == 1:
        category = argv[0]

        if category in registry.categories():
            print_category(registry, category)
            return 0

    # Direct command:
    # reysam <category> <tool> [args...]
    if len(argv) >= 2:
        category, name, *tool_args = argv

        tool = registry.get(category, name)

        if tool is None:
            print(
                f"Unknown tool: {category}/{name}",
                file=sys.stderr,
            )
            print(
                "Use 'reysam --list' to see discovered tools.",
                file=sys.stderr,
            )
            return 2

        return run_tool(tool, tool_args)

    print(
        "Usage: reysam <category> <tool> [args...]",
        file=sys.stderr,
    )
    print(
        "       reysam --interactive",
        file=sys.stderr,
    )
    print(
        "       reysam --list",
        file=sys.stderr,
    )

    return 2


if __name__ == "__main__":
    raise SystemExit(main())