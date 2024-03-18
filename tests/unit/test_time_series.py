from datetime import datetime

import numpy as np
import pytest

from armonik.common import Task

from armonik_analytics.metrics import TasksInStatusOverTime
from armonik_analytics.utils import TaskTimestamps

from conftest import test_cases


def test_constructor():
    TasksInStatusOverTime(TaskTimestamps.ENDED)
    TasksInStatusOverTime(TaskTimestamps.CREATED, TaskTimestamps.SUBMITTED)

    with pytest.raises(ValueError):
        TasksInStatusOverTime("wrong")

    with pytest.raises(ValueError):
        TasksInStatusOverTime(TaskTimestamps.CREATED, "wrong")

    with pytest.raises(ValueError):
        TasksInStatusOverTime(TaskTimestamps.SUBMITTED, TaskTimestamps.CREATED)


@pytest.mark.parametrize(
    ["tasks", "start", "end", "value"],
    [
        (test_case["tasks"], test_case["start"], test_case["end"], test_case["ended_over_time"])
        for test_case in test_cases
    ],
)
def test_task_in_status_over_time_no_next_status(
    tasks: list[Task], start: datetime, end: datetime, value: np.ndarray
):
    tisot = TasksInStatusOverTime(TaskTimestamps.ENDED)
    tisot.update(len(tasks), tasks)
    tisot.complete(start, end)
    assert np.array_equal(tisot.values, value)


@pytest.mark.parametrize(
    ["tasks", "start", "end", "value"],
    [
        (test_case["tasks"], test_case["start"], test_case["end"], test_case["created_over_time"])
        for test_case in test_cases
    ],
)
def test_task_in_status_over_time_with_next_status(
    tasks: list[Task], start: datetime, end: datetime, value: np.ndarray
):
    tisot = TasksInStatusOverTime(TaskTimestamps.CREATED, TaskTimestamps.SUBMITTED)
    tisot.update(len(tasks), tasks)
    tisot.complete(start, end)
    assert np.array_equal(tisot.values, value)
