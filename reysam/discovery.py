from pathlib import Path
import importlib.util

from .tool import Tool


REQUIRED_METADATA = {
    "name",
    "description",
    "category",
}


def load_module(path):
    """Load a Python file as a module."""

    module_name = f"reysam_tool_{path.stem}"

    spec = importlib.util.spec_from_file_location(
        module_name,
        path,
    )

    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def is_valid_tool(module, category):
    """Check whether a module follows the Reysam tool contract."""

    if not hasattr(module, "TOOL"):
        return False

    metadata = module.TOOL

    if not isinstance(metadata, dict):
        return False

    if not REQUIRED_METADATA.issubset(metadata):
        return False

    if not isinstance(metadata["name"], str):
        return False

    if not isinstance(metadata["description"], str):
        return False

    if not isinstance(metadata["category"], str):
        return False

    if not callable(getattr(module, "main", None)):
        return False

    if metadata["category"] != category:
        return False

    return True

def discover_tools(tools_directory):
    """Discover all valid Reysam tools."""

    tools_directory = Path(tools_directory)
    discovered = []

    if not tools_directory.exists():
        return discovered

    for category_directory in tools_directory.iterdir():
        if not category_directory.is_dir():
            continue

        category = category_directory.name

        for tool_file in category_directory.glob("*.py"):
            if tool_file.name.startswith("_"):
                continue

            try:
                module = load_module(tool_file)

            except Exception as exc:
                print(
                    f"Warning: could not load {tool_file}"
                )
                print(
                    f"         {type(exc).__name__}: {exc}"
                )
                continue

            if not is_valid_tool(module, category):
                continue

            metadata = module.TOOL

            discovered.append(
                Tool(
                    name=metadata["name"],
                    description=metadata["description"],
                    category=metadata["category"],
                    module=module,
                    path=tool_file,
                )
            )

    return discovered