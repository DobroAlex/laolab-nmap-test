from dataclasses import dataclass, field
from typing import Optional

import core.config
from core.cli import ProgramArgs


@dataclass
class Context:
    program_args: 'ProgramArgs'
    __config: Optional['core.config.Config'] = field(default=None)

    @property
    def config(self) -> Optional['core.config.Config']:
        if not self.__config:
            self.__config = core.config.Config()
        return self.__config
