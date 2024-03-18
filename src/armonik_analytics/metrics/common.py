from datetime import datetime

from .base import ArmoniKMetric
from armonik.common import Task


class TotalElapsedTime(ArmoniKMetric):
    """
    A metric to compute the total elapsed time between the first task and the last task.
    """

    def __init__(self) -> None:
        self.elapsed = None

    def complete(self, start: datetime | None, end: datetime | None) -> None:
        """
        Calculate the total elapsed time.

        Args:
            start (datetime): The start time.
            end (datetime): The end time.
        """
        if isinstance(start, datetime) and isinstance(end, datetime):
            self.elapsed = (end - start).total_seconds()
        else:
            self.elapsed = None

    @property
    def values(self) -> float:
        """
        Return the total elapsed time as the metric value.

        Return:
            int: The total elasped time.
        """
        return self.elapsed


class AvgThroughput(ArmoniKMetric):
    """
    A metric to compute the average throughput.
    """

    def __init__(self) -> None:
        self.throughput = None
        self.ended = None

    def update(self, total: int, tasks: list[Task]) -> None:
        """
        Update the total number of tasks.

        Args:
            total (int): Total number of tasks.
            tasks (list[Task]): A task batch.
        """
        n_ended = len([t for t in tasks if t.ended_at])
        self.ended = self.ended + n_ended if self.ended else n_ended

    def complete(self, start: datetime | None, end: datetime | None) -> None:
        """
        Calculate the average throughput.

        Args:
            start (datetime): The start time.
            end (datetime): The end time.
        """
        if (
            isinstance(self.ended, int)
            and isinstance(start, datetime)
            and isinstance(end, datetime)
        ):
            self.throughput = self.ended / (end - start).total_seconds()
        else:
            self.throughput = None

    @property
    def values(self) -> float:
        """
        Return the average throughput as the metric value.

        Return:
            int: The average throughput.
        """
        return self.throughput
