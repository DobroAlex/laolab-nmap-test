import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Optional

import core.enums


def get_abs_path(path_: Union[str, Path]) -> Path:
    return Path(str(path_)).expanduser().resolve().absolute()


@dataclass
class FinishedProcess:
    command: str
    work_dir: str
    process: 'subprocess.Popen'
    stdout: str
    stderr: Optional[str]


def spawn_and_communicate_with_subprocess(
        command: str,
        work_dir: Union[str, Path],
        return_error: bool = True,
        with_shell: bool = False,
        _encoding: str = 'utf-8',
        _errors: str = 'ignore',
) -> FinishedProcess:
    work_dir = str(work_dir)
    with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=work_dir,
            shell=with_shell,
    ) as process:
        output, error = process.communicate()

        _output = output.decode(_encoding, _errors)
        _error = error.decode(_encoding, _errors)

        if not process.returncode or return_error:
            return FinishedProcess(command, work_dir, process, _output, _error)

        raise RuntimeError(
            f'{command} at {work_dir} caused the following error:\n'
            f'{error}\n'
            f'Return code: {process.returncode}'
        )


def get_current_os() -> 'core.enums.PlatformVersion':
    """

    :return: Tries to return an enum representing the current os.
    Supported OSes are:
            * Windows
            * Linux
            * Mac (Darwin)

    :rtype: core.enums.PlatformVersion
    """
    current_os = platform.system()
    try:
        return core.enums.PlatformVersion(current_os)
    except ValueError as err:
        # noinspection PyUnresolvedReferences
        supported_oses: list[str] = [p.value for p in core.enums.PlatformVersion]
        raise OSError(
            f'Unsupported system: {current_os}\n'
            f'Supported systems are: {", ".join(supported_oses)}'
        ) from err
