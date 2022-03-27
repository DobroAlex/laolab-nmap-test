from dataclasses import dataclass

from core.cli import ProgramArgs


@dataclass
class Context:
    program_args: 'ProgramArgs'
