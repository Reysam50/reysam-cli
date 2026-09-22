from reysam.runner import run_tool
from reysam.tool import Tool


class FakeModule:
    def __init__(self):
        self.received_args = None

    def main(self, args):
        self.received_args = args
        return 0


def test_runner_passes_arguments_to_tool():
    module = FakeModule()

    tool = Tool(
        name="test",
        description="Test tool.",
        category="testing",
        module=module,
        path=None,
    )

    result = run_tool(tool, ["hello", "world"])

    assert module.received_args == ["hello", "world"]
    assert result == 0