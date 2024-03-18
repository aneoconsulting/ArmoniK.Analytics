from datetime import datetime

import numpy as np
from armonik.common import Task

from .base import ArmoniKMetric
from ..utils import TaskTimestamps


class TasksInStatusOverTime(ArmoniKMetric):
    """
    A metric to track tasks in a particular status over time.
    """

    def __init__(
        self, timestamp: TaskTimestamps, next_timestamp: TaskTimestamps | None = None
    ) -> None:
        """
        Initialize the metric.

        Args:
            timestamp (str): The current timestamp of the tasks.
            next_timestamp (str, optional): The next timestamp of the tasks. Defaults to None.
        """
        self.timestamp = timestamp
        self.next_timestamp = next_timestamp
        self.timestamps = None
        self.steps = None
        self.index = 0

    @property
    def name(self) -> str:
        return f"{self.timestamp.name.capitalize()}TasksOverTime"

    @property
    def timestamp(self) -> TaskTimestamps:
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, __value: TaskTimestamps) -> None:
        __value = TaskTimestamps(__value)
        self.__timestamp = __value

    @property
    def next_timestamp(self) -> TaskTimestamps:
        return self.__next_timestamp

    @next_timestamp.setter
    def next_timestamp(self, __value: TaskTimestamps) -> None:
        if __value is not None:
            __value = TaskTimestamps(__value)
            if __value < self.timestamp:
                raise ValueError(
                    f"Inconsistent timestamp order '{self.timestamp.name}' is not prior to '{__value.name}'."
                )
        self.__next_timestamp = __value

    def update(self, total: int, tasks: list[Task]) -> None:
        """
        Update the metric.

        Args:
            total (int): Total number of tasks.
            tasks (list[Task]): A task batch.
        """
        n_tasks = len(tasks)
        if self.timestamps is None:
            n = (2 * total) + 1 if self.next_timestamp else total + 1
            self.timestamps = np.memmap(
                f"{self.name}_timestamps.dat", dtype=datetime, mode="w+", shape=(n,)
            )
            self.steps = np.memmap(f"{self.name}_steps.dat", dtype=np.int8, mode="w+", shape=(n,))
            self.index = 1
        self.timestamps[self.index : self.index + n_tasks] = [
            getattr(t, f"{self.timestamp.name.lower()}_at") for t in tasks
        ]
        self.steps[self.index : self.index + n_tasks] = n_tasks * [1]
        self.index += n_tasks
        if self.next_timestamp:
            self.timestamps[self.index : self.index + n_tasks] = [
                getattr(t, f"{self.next_timestamp.name.lower()}_at") for t in tasks
            ]
            self.steps[self.index : self.index + n_tasks] = n_tasks * [-1]
            self.index += n_tasks

    def complete(self, start: datetime | None, end: datetime | None) -> None:
        """
        Complete the metric calculation.

        Args:
            start (datetime): The start time.
            end (datetime): The end time.
        """
        if start is None or self.timestamps.shape[0] == 1:
            self.timestamps = None
            self.steps = None
            return
        # Add start date with no step
        self.timestamps[0] = start
        self.steps[0] = 0
        # Remove inconsistent data (due to missing timestamps in task metadata)
        inconsistent_values = np.atleast_1d(self.timestamps == np.array(None)).nonzero()[0]
        self.timestamps = np.delete(self.timestamps, inconsistent_values)
        self.steps = np.delete(self.steps, inconsistent_values)
        # Sort the arrays by timestamp dates
        sort_indices = self.timestamps.argsort()
        self.timestamps = self.timestamps[sort_indices]
        self.steps = self.steps[sort_indices]
        # Compute the number of task in the given timestamp over time
        self.steps = np.cumsum(self.steps)

    @property
    def values(self):
        """
        Return the timestamps as the metric values.
        """
        if self.timestamps is None:
            return None
        return np.vstack((self.timestamps, self.steps))
