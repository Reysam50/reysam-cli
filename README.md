# Reysam

**Reysam** is a modular personal CLI toolbox and tool runner.

The idea is simple: when I write a useful script, I should be able to add it to the toolbox without rewriting the core CLI. Reysam discovers tools automatically and exposes them through both direct commands and an interactive terminal interface.

## Features

* Automatic tool discovery from `tools/<category>/`.
* Direct command mode for scripting and automation.
* Interactive mode for browsing and running tools.
* List discovered tools with `--list`.
* Category-based tool organization.
* Self-describing tools with a small metadata block.
* Tool contract validation during discovery.
* Tools are isolated from the core CLI engine.
* Tool arguments are passed directly to each tool.
* Integer exit codes are supported.
* Designed to grow as new utilities are added.

## Project Structure

```text
reysam/
├── reysam/
│   ├── __init__.py
│   ├── cli.py          # CLI entry point and interactive interface
│   ├── discovery.py    # Finds, loads, and validates tools
│   ├── registry.py     # Organizes and looks up discovered tools
│   ├── runner.py       # Executes discovered tools
│   └── tool.py         # Tool data model
│
├── tools/
│   └── <category>/
│       └── <tool>.py   # Individual toolbox utilities
│
├── tests/
│   ├── test_discovery.py
│   ├── test_registry.py
│   └── test_runner.py
│
├── pyproject.toml
└── README.md
```

### Architecture

Reysam separates the toolbox engine from the individual utilities.

```text
User
 │
 ▼
cli.py
 │
 ▼
discovery.py
 │
 ▼
Tool objects
 │
 ▼
registry.py
 │
 ▼
runner.py
 │
 ▼
tool.main(args)
```

The core application discovers and manages tools, while each tool is responsible for its own functionality.

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

### Interactive Mode

Start Reysam without arguments:

```bash
reysam
```

You can also explicitly request interactive mode:

```bash
reysam --interactive
```

Reysam will display the available tools and allow you to select one to run.

### List Discovered Tools

```bash
reysam --list
```

or:

```bash
reysam -l
```

### List Tools in a Category

```bash
reysam network
```

### Run a Tool Directly

```bash
reysam network ping 8.8.8.8
```

Arguments after the tool name are passed directly to the tool.

## Adding a Tool

Create a category directory under `tools/` and add a Python file containing a `TOOL` dictionary and a `main(args)` function.

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
```

Then run it directly:

```bash
reysam utilities hello
```

No changes to the core CLI are required.

## Tool Contract

For the current version, a tool must:

1. Be a `.py` file inside a category directory under `tools/`.
2. Define a `TOOL` dictionary.
3. Define the following metadata:

   * `name` — tool name as a string.
   * `description` — short description as a string.
   * `category` — category name as a string.
4. Have a callable `main(args)` function.
5. Have a `category` value matching the directory containing the tool.
6. Return `None` or an integer exit code from `main()`.

Example:

```python
TOOL = {
    "name": "ping",
    "description": "Ping a host using the system ping utility.",
    "category": "network",
}


def main(args):
    ...
```

Reysam validates this contract during tool discovery. Invalid tools are ignored rather than registered.

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

Run the test suite:

```bash
python -m pytest
```

The current test suite covers:

* Tool discovery
* Tool contract validation
* Tool registry operations
* Argument passing to tools
* Tool execution and exit codes

## Roadmap

Planned improvements include:

* Better interactive navigation by category.
* Tool-specific help and argument parsing.
* Better reporting of broken or failed tool discovery.
* Configuration support.
* Cleaner terminal output.
* Tool enable/disable support.
* Cross-platform execution improvements.
* Support for additional tool types where appropriate.
* Packaging and release automation.

## License

MIT License.
