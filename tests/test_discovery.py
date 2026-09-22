from pathlib import Path

from reysam.discovery import discover_tools


def test_discovers_sample_tool():
    tools = discover_tools(Path(__file__).parents[1] / "tools")
    assert any(t.category == "network" and t.name == "ping" for t in tools)

from types import SimpleNamespace

from reysam.discovery import is_valid_tool


def test_rejects_tool_with_invalid_name():
    module = SimpleNamespace(
        TOOL={
            "name": 123,
            "description": "Test tool.",
            "category": "network",
        },
        main=lambda args: None,
    )

    assert is_valid_tool(module, "network") is False


def test_rejects_tool_with_invalid_description():
    module = SimpleNamespace(
        TOOL={
            "name": "test",
            "description": ["Not a string"],
            "category": "network",
        },
        main=lambda args: None,
    )

    assert is_valid_tool(module, "network") is False


def test_rejects_tool_with_invalid_category():
    module = SimpleNamespace(
        TOOL={
            "name": "test",
            "description": "Test tool.",
            "category": 123,
        },
        main=lambda args: None,
    )

    assert is_valid_tool(module, "network") is False


def test_rejects_tool_without_main():
    module = SimpleNamespace(
        TOOL={
            "name": "test",
            "description": "Test tool.",
            "category": "network",
        }
    )

    assert is_valid_tool(module, "network") is False