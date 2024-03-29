from abc import ABC, abstractproperty
from datetime import datetime

from armonik.common import Task


class ArmoniKMetric(ABC):
    """
    Abstract base class for ArmoniK metrics.
    """

    def update(self, total: int, tasks: list[Task]) -> None:
        """
        Abstract method to be override.
        Update the metric with a given task batch.

        Args:
            total (int): Total number of task on which the metric is computed.
            tasks (list[Task]): A task batch.
        """
        pass

    def complete(self, start: datetime, end: datetime) -> None:
        """
        Complete the metric computation.

        Args:
            start (datetime): The start datetime.
            end (datetime): The end datetime.
        """
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractproperty
    def values(self) -> any:
        """
        Abstract method to be override.
        Property to access the values of the metric.

        Return:
            any: The values of the metric.
        """
        pass
