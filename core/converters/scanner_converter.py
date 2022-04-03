import abc
from typing import Generator

import core.db.models as db_models


class ScannerConverter(abc.ABC):
    """
    An interface that provides a single method `to_db_repr`
    that should return a list of DB records
    """

    @property
    @abc.abstractmethod
    def to_db_repr(self) -> Generator['db_models.Base']:
        """
        A method that converts a single scanner run result into a generator with DB records
        representing this single run.
        NOTE: order of elements in this generator matters as records are added
        to the DB according to this order.
        NOTE: it's important to yield and flush an element to ensure it will have an ID or
        any other value that is provided by SQL Alchemy


        :return: A list of records to save in DB

        :rtype: list['Base']
        """
        ...
