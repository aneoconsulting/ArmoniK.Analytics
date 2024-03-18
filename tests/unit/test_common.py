from datetime import datetime

import pytest

from armonik.common import Task

from armonik_analytics.metrics import AvgThroughput, TotalElapsedTime

from conftest import test_cases


@pytest.mark.parametrize(
    ["tasks", "start", "end", "value"],
    [
        (test_case["tasks"], test_case["start"], test_case["end"], test_case["avg_throughput"])
        for test_case in test_cases
    ],
)
def test_avg_throughput(tasks: list[Task], start: datetime, end: datetime, value: float | None):
    th = AvgThroughput()
    th.update(len(tasks), tasks)
    th.complete(start, end)
    assert th.values == value


@pytest.mark.parametrize(
    ["tasks", "start", "end", "value"],
    [
        (test_case["tasks"], test_case["start"], test_case["end"], test_case["total_elapsed_time"])
        for test_case in test_cases
    ],
)
def test_total_elapsed_time(tasks: list[Task], start: datetime, end: datetime, value: float | None):
    tet = TotalElapsedTime()
    tet.update(len(tasks), tasks)
    tet.complete(start, end)
    assert tet.values == value
