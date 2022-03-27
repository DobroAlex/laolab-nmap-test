import argparse
from pathlib import Path

import core.utils


def validate_path_arg(val) -> Path:
    try:
        return core.utils.get_abs_path(val)
    except TypeError as err:
        raise argparse.ArgumentTypeError(
            f'Cant convert {val} to a path'
        ) from err
