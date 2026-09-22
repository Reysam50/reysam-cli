# Reysam

**Reysam** is a modular personal CLI toolbox and tool runner.

The idea is simple: when I write a useful script, I should be able to add it to the toolbox without rewriting the core CLI. Reysam discovers tools automatically and exposes them through both direct commands and an interactive terminal interface.

## Features

- Automatic tool discovery from `tools/<category>/`.
- Direct command mode for scripting and automation.
- Interactive mode for browsing and running tools.
- Self-describing tools with a small metadata block.
- Tools are isolated from the core CLI engine.
- Designed to grow as new utilities are added.

## Project structure

```text
reysam/
├── reysam/
│   ├── cli.py          # CLI entry point and interactive interface
│   ├── discovery.py    # Finds and loads tools
│   └── runner.py       # Executes discovered tools
│
├── tools/
│   └── <category>/
│       └── <tool>.py   # Individual toolbox utilities
│
├── tests/
├── pyproject.toml
└── README.md
```

## Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/Reysam50/reysam.git
cd reysam
python -m pip install -e .
```

Editable installation means changes to the project are immediately reflected without reinstalling the package.

If your Python installation does not put its script directory on `PATH`, add that directory to `PATH` or use a virtual environment and activate it before running Reysam.

## Usage

Start interactive mode:

```bash
reysam
```

List discovered tools:

```bash
reysam --list
```

Run a tool directly:

```bash
reysam network ping 8.8.8.8
```

## Adding a tool

Create a category directory under `tools/` and add a Python file with a `TOOL` dictionary and a `main(args)` function.

Example:

```python
TOOL = {
    "name": "hello",
    "description": "Print a greeting.",
    "category": "utilities",
}


def main(args: list[str]) -> int:
    print("Hello from Reysam!")
    return 0
```

Save it as:

```text
tools/utilities/hello.py
```

Restart Reysam and it will be discovered automatically:

```bash
reysam --list
reysam utilities hello
```

## Tool contract

For the current version, a tool must:

1. Be a `.py` file inside a category directory under `tools/`.
2. Define `TOOL` metadata.
3. Define a callable `main(args)` function.
4. Return `None` or an integer exit code from `main()`.

The core application does not need to be modified when a new tool is added.

## Development

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Install the project:

```bash
python -m pip install -e .
```

Run tests:

```bash
python -m pytest
```

## Roadmap

Planned improvements include:

- Better interactive navigation by category.
- Tool-specific help and argument parsing.
- Configuration support.
- Cleaner terminal output.
- Tool enable/disable support.
- Cross-platform execution improvements.
- Support for additional tool types where appropriate.
- Packaging and release automation.

## License

MIT License.
