from datetime import datetime

import pytest

from armonik.common import Task

from armonik_analytics.metrics import TimestampsTransition
from armonik_analytics.utils import TaskTimestamps

from conftest import test_cases


def test_constructor():
    TimestampsTransition(TaskTimestamps.CREATED, TaskTimestamps.SUBMITTED)

    with pytest.raises(ValueError):
        TimestampsTransition(TaskTimestamps.CREATED, "wrong")

    with pytest.raises(ValueError):
        TimestampsTransition(TaskTimestamps.SUBMITTED, TaskTimestamps.CREATED)


@pytest.mark.parametrize(
    ["tasks", "start", "end", "value"],
    [
        (
            test_case["tasks"],
            test_case["start"],
            test_case["end"],
            test_case["created_to_submitted"],
        )
        for test_case in test_cases
    ],
)
def test_timestamps_transition(
    tasks: list[Task], start: datetime, end: datetime, value: dict[str, float | None]
):
    st = TimestampsTransition(TaskTimestamps.CREATED, TaskTimestamps.SUBMITTED)
    st.update(len(tasks), tasks)
    st.complete(start, end)
    assert st.values == value
