from datetime import datetime

import grpc
import pytest

from armonik.client import ArmoniKTasks, TaskFieldFilter
from armonik.common import Direction, Filter, Task
from armonik.protogen.common.sort_direction_pb2 import SortDirection

from armonik_analytics.stats import ArmoniKStatistics
from armonik_analytics.metrics.base import ArmoniKMetric

from conftest import test_cases


class DummyMetric(ArmoniKMetric):
    def __init__(self):
        self.updates = 0
        self.completes = 0
        self.total = None
        self.tasks = []
        self.start = None
        self.end = None

    def update(self, total: int, tasks: list[Task]) -> None:
        self.updates += 1
        self.total = total
        self.tasks.append(tasks)

    def complete(self, start: datetime, end: datetime) -> None:
        self.start = start
        self.end = end
        self.completes += 1

    @property
    def values(self):
        return "value"


class DummyArmoniKTasks(ArmoniKTasks):
    __call_count = 0

    def __init__(self, grpc_channel: grpc.Channel, tasks: list[Task]):
        super().__init__(grpc_channel)
        self.tasks = tasks
        self.total = 2 * len(tasks)

    def list_tasks(
        self,
        task_filter: Filter | None = None,
        with_errors: bool = False,
        page: int = 0,
        page_size: int = 1000,
        sort_field: Filter = TaskFieldFilter.TASK_ID,
        sort_direction: SortDirection = Direction.ASC,
        detailed: bool = True,
    ) -> tuple[int, list[Task]]:
        self.__call_count += 1
        if self.__call_count <= 2:
            return self.total, self.tasks
        return self.total, []


def test_constructor():
    with grpc.insecure_channel("url") as channel:
        ArmoniKStatistics(
            channel=channel,
            task_filter=TaskFieldFilter.SESSION_ID == "session-id",
            metrics=[DummyMetric()],
        )

        with pytest.raises(TypeError):
            ArmoniKStatistics(
                channel=channel,
                task_filter=TaskFieldFilter.SESSION_ID == "session-id",
                metrics="a",
            )

        with pytest.raises(TypeError):
            ArmoniKStatistics(
                channel=channel,
                task_filter=TaskFieldFilter.SESSION_ID == "session-id",
                metrics=[],
            )

        with pytest.raises(TypeError):
            ArmoniKStatistics(
                channel=channel,
                task_filter=TaskFieldFilter.SESSION_ID == "session-id",
                metrics=["a", DummyMetric()],
            )

        with pytest.raises(TypeError):
            ArmoniKStatistics(
                channel=channel,
                task_filter=TaskFieldFilter.SESSION_ID == "session-id",
                metrics=[DummyMetric],
            )


@pytest.mark.parametrize(
    ["tasks", "start", "end"],
    [
        (test_case["tasks"], test_case["start"], test_case["end"])
        for test_case in test_cases
        if len(test_case["tasks"]) > 0
    ],
)
def test_compute(tasks: list[Task], start: datetime, end: datetime):
    with grpc.insecure_channel("url") as channel:
        dummy = DummyMetric()
        stats = ArmoniKStatistics(
            channel=channel,
            task_filter=TaskFieldFilter.SESSION_ID == "session-id",
            metrics=[dummy],
        )
        stats.client = DummyArmoniKTasks(channel, tasks=tasks)
        stats.compute()

        assert dummy.updates == 2
        assert dummy.completes == 1
        assert stats.values == {"DummyMetric": "value"}
        assert dummy.total == 2 * len(tasks)
        assert dummy.start == start
        assert dummy.end == end
