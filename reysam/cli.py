from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

from .discovery import Tool, discover_tools
from .runner import run_tool


def project_tools_dir() -> Path:
    """Return the tools directory bundled with the project."""
    # During development this resolves to the repository's tools/ directory.
    return Path(__file__).resolve().parent.parent / "tools"


def build_parser(tools: list[Tool]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reysam",
        description="A modular personal CLI toolbox and tool runner.",
    )
    parser.add_argument("--list", action="store_true", help="List discovered tools.")
    parser.add_argument("--interactive", "-i", action="store_true", help="Open interactive mode.")
    return parser


def print_tools(tools: list[Tool]) -> None:
    if not tools:
        print("No tools discovered.")
        return

    categories: dict[str, list[Tool]] = {}
    for tool in tools:
        categories.setdefault(tool.category, []).append(tool)

    print("\nREYSAM TOOLBOX\n")
    for category, category_tools in categories.items():
        print(f"{category}/")
        for tool in category_tools:
            print(f"  {tool.name:<18} {tool.description}")
        print()


def interactive(tools: list[Tool]) -> int:
    if not tools:
        print("No tools discovered.")
        return 1

    while True:
        print("\nREYSAM TOOLBOX")
        print("=" * 40)
        for index, tool in enumerate(tools, start=1):
            print(f"{index:>2}. {tool.category}/{tool.name} - {tool.description}")
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

    # Explicit interactive mode / no arguments.
    if not argv or argv == ["-i"] or argv == ["--interactive"]:
        return interactive(tools)

    # Resolve direct command: reysam <category> <tool> [args...]
    if argv[0] in {"--list", "-l"}:
        print_tools(tools)
        return 0

    if len(argv) >= 2:
        category, name, *tool_args = argv
        matches = [t for t in tools if t.category == category and t.name == name]
        if not matches:
            print(f"Unknown tool: {category}/{name}", file=sys.stderr)
            print("Use 'reysam --list' to see discovered tools.", file=sys.stderr)
            return 2
        return run_tool(matches[0], tool_args)

    print("Usage: reysam <category> <tool> [args...]", file=sys.stderr)
    print("       reysam --interactive", file=sys.stderr)
    print("       reysam --list", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
