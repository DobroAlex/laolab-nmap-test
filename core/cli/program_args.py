from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProgramArgs:
    scan_target: str
    output_file: Path
