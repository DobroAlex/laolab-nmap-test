import abc

from core.db.models import Base


class ScannerConverter(abc.ABC):
    """
    An interface that provides a single method `to_db_repr`
    that should return a list of DB records
    """

    @property
    @abc.abstractmethod
    def to_db_repr(self) -> list['Base']:
        """
        A method that converts a single scanner run result into a list of DB records
        representing this single run.
        NOTE: order of elements in this list matters as records are added
        to the DB according to this order


        :return: A list of records to save in DB

        :rtype: list['Base']
        """
        ...
