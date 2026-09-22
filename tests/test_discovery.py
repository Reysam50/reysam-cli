from pathlib import Path

from reysam.discovery import discover_tools


def test_discovers_sample_tool():
    tools = discover_tools(Path(__file__).parents[1] / "tools")
    assert any(t.category == "network" and t.name == "ping" for t in tools)
