import datetime
from typing import Union


def timestamp_to_date(timestamp_: Union[str, float, datetime.datetime]) -> datetime.datetime:
    try:
        if isinstance(timestamp_, str):
            timestamp_ = float(timestamp_)
    except (TypeError, ValueError) as err:
        raise ValueError(
            f'Cant convert {timestamp_} (type: {type(timestamp_)} to float'
        ) from err

    return datetime.datetime.fromtimestamp(timestamp_)
