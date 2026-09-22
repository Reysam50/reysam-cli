from reysam import cli


class FakeTool:
    def __init__(self):
        self.received_args = None

        self.name = "test"
        self.description = "Test tool."
        self.category = "testing"

        class FakeModule:
            def __init__(inner_self):
                inner_self.received_args = None

            def main(inner_self, args):
                self.received_args = args
                return 0

        self.module = FakeModule()
        self.path = None


def test_main_runs_direct_tool(monkeypatch):
    tool = FakeTool()

    monkeypatch.setattr(
        cli,
        "discover_tools",
        lambda directory: [tool],
    )

    result = cli.main(
        ["testing", "test", "hello", "world"]
    )

    assert tool.received_args == ["hello", "world"]
    assert result == 0
    
def test_main_lists_tools_in_category(monkeypatch, capsys):
    tool = FakeTool()

    monkeypatch.setattr(
        cli,
        "discover_tools",
        lambda directory: [tool],
    )

    result = cli.main(["testing"])

    captured = capsys.readouterr()

    assert result == 0
    assert "TESTING TOOLS" in captured.out
    assert "test" in captured.out
    assert "Test tool." in captured.out


def test_main_lists_all_tools(monkeypatch, capsys):
    tool = FakeTool()

    monkeypatch.setattr(
        cli,
        "discover_tools",
        lambda directory: [tool],
    )

    result = cli.main(["--list"])

    captured = capsys.readouterr()

    assert result == 0
    assert "REYSAM TOOLBOX" in captured.out
    assert "testing/" in captured.out
    assert "test" in captured.out


def test_main_rejects_unknown_tool(monkeypatch, capsys):
    tool = FakeTool()

    monkeypatch.setattr(
        cli,
        "discover_tools",
        lambda directory: [tool],
    )

    result = cli.main(
        ["testing", "does-not-exist"]
    )

    captured = capsys.readouterr()

    assert result == 2
    assert "Unknown tool: testing/does-not-exist" in captured.err
    assert "reysam --list" in captured.err


def test_main_rejects_unknown_category(monkeypatch, capsys):
    tool = FakeTool()

    monkeypatch.setattr(
        cli,
        "discover_tools",
        lambda directory: [tool],
    )

    result = cli.main(["does-not-exist"])

    captured = capsys.readouterr()

    assert result == 2
    assert "Usage:" in captured.err


def test_main_interactive_mode(monkeypatch):
    tool = FakeTool()

    monkeypatch.setattr(
        cli,
        "discover_tools",
        lambda directory: [tool],
    )

    inputs = iter([
        "1",
        "hello world",
        "q",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(inputs),
    )

    result = cli.main([])

    assert result == 0
    assert tool.received_args == ["hello", "world"]


def test_main_explicit_interactive_mode(monkeypatch):
    tool = FakeTool()

    monkeypatch.setattr(
        cli,
        "discover_tools",
        lambda directory: [tool],
    )

    inputs = iter([
        "q",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(inputs),
    )

    result = cli.main(["--interactive"])

    assert result == 0