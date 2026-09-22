from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


@dataclass
class Tool:
    name: str
    description: str
    category: str
    module: ModuleType
    path: Path