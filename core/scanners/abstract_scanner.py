import abc
import os
from pathlib import Path
from typing import Optional, Union

import core.utils
from core.utils import FinishedProcess
from core.context import Context


class AbstractBaseScanner(abc.ABC):
    def __init__(self, context: 'Context'):
        self.context = context
        self.process: Optional[FinishedProcess] = None
        self.work_dir: Union[str, Path] = Path(os.getcwd())

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def executable_path(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def cli_args(self) -> str:
        ...

    @property
    def full_command(self) -> str:
        command = f'{self.executable_path} {self.cli_args}'
        if core.utils.get_current_os() == core.enums.PlatformVersion.LINUX:
            command = 'sudo ' + command
        return command

    @property
    @abc.abstractmethod
    def is_return_code_ok(self) -> bool:
        ...

    @abc.abstractmethod
    def parse_output(self):
        ...

    def run(self) -> None:
        print(f'Starting {self.name} from {self.work_dir} with the following args:\n{self.full_command}')
        self.process = core.utils.spawn_and_communicate_with_subprocess(
            self.full_command,
            self.work_dir,
            with_shell=True,
        )
