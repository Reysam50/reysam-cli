from reysam.registry import ToolRegistry
from reysam.tool import Tool


def test_registry_finds_tool():
    tool = Tool(
        name="ping",
        description="Ping a host.",
        category="network",
        module=None,
        path=None,
    )

    registry = ToolRegistry([tool])

    result = registry.get("network", "ping")

    assert result is not None
    assert result.name == "ping"


def test_registry_returns_categories():
    tools = [
        Tool(
            name="ping",
            description="Ping a host.",
            category="network",
            module=None,
            path=None,
        ),
        Tool(
            name="organize",
            description="Organize files.",
            category="files",
            module=None,
            path=None,
        ),
    ]

    registry = ToolRegistry(tools)

    assert registry.categories() == ["files", "network"]