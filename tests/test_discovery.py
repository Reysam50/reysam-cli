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
    
def test_warns_when_tool_fails_to_load(tmp_path, capsys):
    tools_dir = tmp_path / "tools"
    network_dir = tools_dir / "network"
    network_dir.mkdir(parents=True)

    broken_tool = network_dir / "broken.py"

    broken_tool.write_text(
        "raise RuntimeError('broken tool')\n",
        encoding="utf-8",
    )

    tools = discover_tools(tools_dir)

    captured = capsys.readouterr()

    assert tools == []
    assert "Warning: could not load" in captured.out
    assert "RuntimeError: broken tool" in captured.out
    
def test_broken_tool_does_not_stop_valid_tools(tmp_path, capsys):
    tools_dir = tmp_path / "tools"
    network_dir = tools_dir / "network"
    network_dir.mkdir(parents=True)

    broken_tool = network_dir / "broken.py"
    broken_tool.write_text(
        "raise RuntimeError('broken tool')\n",
        encoding="utf-8",
    )

    valid_tool = network_dir / "good.py"
    valid_tool.write_text(
        """
TOOL = {
    "name": "good",
    "description": "A valid test tool.",
    "category": "network",
}


def main(args):
    return 0
""",
        encoding="utf-8",
    )

    tools = discover_tools(tools_dir)

    captured = capsys.readouterr()

    assert any(
        tool.name == "good"
        for tool in tools
    )

    assert "Warning: could not load" in captured.out
    assert "RuntimeError: broken tool" in captured.out