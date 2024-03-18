import os

from datetime import datetime, timezone

import numpy as np
import pytest

from armonik.common import Task


test_cases = [
    {
        "tasks": [],
        "start": None,
        "end": None,
        "avg_throughput": None,
        "total_elapsed_time": None,
        "created_to_submitted": {"avg": None, "min": None, "max": None},
        "ended_over_time": None,
        "created_over_time": None,
    },
    {
        "tasks": [
            Task(
                id=0,
                created_at=datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                submitted_at=datetime(1, 1, 1, 1, 1, 2, tzinfo=timezone.utc),
                ended_at=datetime(1, 1, 1, 1, 1, 3, tzinfo=timezone.utc),
            )
        ],
        "start": datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
        "end": datetime(1, 1, 1, 1, 1, 3, tzinfo=timezone.utc),
        "avg_throughput": 0.5,
        "total_elapsed_time": 2.0,
        "created_to_submitted": {"avg": 1.0, "min": 1.0, "max": 1.0},
        "ended_over_time": np.array(
            [
                [
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 3, tzinfo=timezone.utc),
                ],
                [0, 1],
            ]
        ),
        "created_over_time": np.array(
            [
                [
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 2, tzinfo=timezone.utc),
                ],
                [0, 1, 0],
            ]
        ),
    },
    {
        "tasks": [
            Task(
                id=0,
                created_at=datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                submitted_at=datetime(1, 1, 1, 1, 1, 3, tzinfo=timezone.utc),
                ended_at=datetime(1, 1, 1, 1, 1, 6, tzinfo=timezone.utc),
            ),
            Task(
                id=1,
                created_at=datetime(1, 1, 1, 1, 1, 2, tzinfo=timezone.utc),
                submitted_at=datetime(1, 1, 1, 1, 1, 4, tzinfo=timezone.utc),
                ended_at=datetime(1, 1, 1, 1, 1, 5, tzinfo=timezone.utc),
            ),
            Task(
                id=2,
                created_at=datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                submitted_at=datetime(1, 1, 1, 1, 1, 5, tzinfo=timezone.utc),
                ended_at=datetime(1, 1, 1, 1, 1, 4, tzinfo=timezone.utc),
            ),
        ],
        "start": datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
        "end": datetime(1, 1, 1, 1, 1, 6, tzinfo=timezone.utc),
        "avg_throughput": 3 / 5.0,
        "total_elapsed_time": 5.0,
        "created_to_submitted": {"avg": 8 / 3, "min": 2.0, "max": 4.0},
        "ended_over_time": np.array(
            [
                [
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 4, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 5, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 6, tzinfo=timezone.utc),
                ],
                [0, 1, 2, 3],
            ]
        ),
        "created_over_time": np.array(
            [
                [
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 2, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 3, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 4, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 5, tzinfo=timezone.utc),
                ],
                [0, 1, 2, 3, 2, 1, 0],
            ]
        ),
    },
    {
        "tasks": [
            Task(
                id=0,
                created_at=datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                submitted_at=datetime(1, 1, 1, 1, 1, 3, tzinfo=timezone.utc),
                ended_at=datetime(1, 1, 1, 1, 1, 6, tzinfo=timezone.utc),
            ),
            Task(id=1),
            Task(
                id=2,
                created_at=datetime(1, 1, 1, 1, 1, 2, tzinfo=timezone.utc),
                submitted_at=datetime(1, 1, 1, 1, 1, 4, tzinfo=timezone.utc),
                ended_at=datetime(1, 1, 1, 1, 1, 5, tzinfo=timezone.utc),
            ),
            Task(id=3),
            Task(
                id=4,
                created_at=datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                submitted_at=datetime(1, 1, 1, 1, 1, 5, tzinfo=timezone.utc),
                ended_at=datetime(1, 1, 1, 1, 1, 4, tzinfo=timezone.utc),
            ),
        ],
        "start": datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
        "end": datetime(1, 1, 1, 1, 1, 6, tzinfo=timezone.utc),
        "avg_throughput": 3 / 5.0,
        "total_elapsed_time": 5.0,
        "created_to_submitted": {"avg": 8 / 3, "min": 2.0, "max": 4.0},
        "ended_over_time": np.array(
            [
                [
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 4, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 5, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 6, tzinfo=timezone.utc),
                ],
                [0, 1, 2, 3],
            ]
        ),
        "created_over_time": np.array(
            [
                [
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 2, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 3, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 4, tzinfo=timezone.utc),
                    datetime(1, 1, 1, 1, 1, 5, tzinfo=timezone.utc),
                ],
                [0, 1, 2, 3, 2, 1, 0],
            ]
        ),
    },
    {
        "tasks": [
            Task(id=0),
            Task(id=1),
        ],
        "start": None,
        "end": None,
        "avg_throughput": None,
        "total_elapsed_time": None,
        "created_to_submitted": {"avg": None, "min": None, "max": None},
        "ended_over_time": None,
        "created_over_time": None,
    },
]


@pytest.fixture(scope="session", autouse=True)
def clean_up():
    yield

    for file in os.listdir(os.getcwd()):
        if file.endswith(".dat"):
            os.remove(os.path.join(os.getcwd(), file))
