import numpy as np
from armonik.common import Task

from .base import ArmoniKMetric
from ..utils import TaskTimestamps


class TimestampsTransition(ArmoniKMetric):
    """
    Metric to compute statistics on transitions between two timestamps in tasks.
    """

    def __init__(self, timestamp_1: str, timestamp_2: str) -> None:
        """
        Initialize the metric.

        Args:
            timestamp_1 (str): The first timestamp.
            timestamp_2 (str): The second timestamp.
        """
        self.timestamps = (timestamp_1, timestamp_2)
        self.avg = None
        self.min = None
        self.max = None

    @property
    def name(self) -> str:
        return f"{self.timestamps[0].name.capitalize()}To{self.timestamps[1].name.capitalize()}"

    @property
    def timestamps(self) -> tuple[TaskTimestamps, TaskTimestamps]:
        """
        Get the timestamps.

        Returns:
            tuple[str, str]: A tuple containing two timestamps.
        """
        return self.__timestamps

    @timestamps.setter
    def timestamps(self, __value: tuple[TaskTimestamps, TaskTimestamps]) -> None:
        """
        Set the timestamps.

        Args:
            __value (tuple[str, str]): A tuple containing two timestamps.

        Raises:
            ValueError: If the timestamps are not valid or in inconsistent order.
        """
        for timestamp in __value:
            TaskTimestamps(timestamp)
        if __value[0] > __value[1]:
            raise ValueError(
                f"Inconsistent timestamp order '{__value[0].name}' is not prior to '{__value[1].name}'."
            )
        self.__timestamps = __value

    def update(self, total: int, tasks: list[Task]) -> None:
        """
        Update the metric with new data.
        Update the average, minimum, and maximum transition times between the two timestamps.

        Args:
            total (int): Total number of tasks.
            tasks (list[Task]): List of tasks.
        """
        deltas = [
            (
                getattr(t, f"{self.timestamps[1].name.lower()}_at")
                - getattr(t, f"{self.timestamps[0].name.lower()}_at")
            ).total_seconds()
            for t in tasks
            if (
                getattr(t, f"{self.timestamps[1].name.lower()}_at") is not None
                and getattr(t, f"{self.timestamps[0].name.lower()}_at") is not None
            )
        ]
        if deltas:
            self.avg = (
                self.avg + np.sum(deltas) / len(deltas)
                if self.avg
                else np.sum(deltas) / len(deltas)
            )
            min = np.min(deltas)
            max = np.max(deltas)
            if self.max is None or self.max < max:
                self.max = max
            if self.min is None or self.min > min:
                self.min = min

    @property
    def values(self) -> dict[str, float]:
        """
        Get the computed values.

        Returns:
            dict[str, float]: A dictionary containing the average, minimum, and maximum transition times.
        """
        return {"avg": self.avg, "min": self.min, "max": self.max}
