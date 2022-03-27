import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Optional


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
