from .tool import Tool


class ToolRegistry:
    def __init__(self, tools: list[Tool]):
        self.tools = tools

    def all(self):
        """Return all registered tools."""
        return self.tools

    def categories(self):
        """Return all available tool categories."""

        return sorted({
            tool.category
            for tool in self.tools
        })

    def get(self, category, name):
        """Find a tool by category and name."""

        for tool in self.tools:
            if tool.category == category and tool.name == name:
                return tool

        return None

    def in_category(self, category):
        """Return all tools belonging to a category."""

        return [
            tool
            for tool in self.tools
            if tool.category == category
        ]