from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    category: str
    path: Path
    module: ModuleType


def discover_tools(tools_dir: Path) -> list[Tool]:
    """Discover Python tools under tools/<category>/*.py."""
    discovered: list[Tool] = []

    if not tools_dir.exists():
        return discovered

    for category_dir in sorted(tools_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith("_"):
            continue

        for path in sorted(category_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue

            module = _load_module(path)
            metadata: dict[str, Any] = getattr(module, "TOOL", {})
            name = metadata.get("name", path.stem)
            description = metadata.get("description", "No description provided.")
            category = metadata.get("category", category_dir.name)

            if not callable(getattr(module, "main", None)):
                continue

            discovered.append(Tool(name, description, category, path, module))

    return discovered


def _load_module(path: Path) -> ModuleType:
    module_name = f"reysam_dynamic_{path.stem}_{abs(hash(path))}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load tool: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
