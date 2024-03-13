import argparse
import json

import grpc
import matplotlib.pyplot as plt

from armonik.client import TaskFieldFilter
from armonik_analytics import ArmoniKStatistics
from armonik_analytics.metrics import (
    AvgThroughput,
    TotalElapsedTime,
    TimestampsTransition,
    TasksInStatusOverTime,
)

from armonik_analytics.utils import TaskTimestamps


def plot_metrics(stats):
    plt.figure()
    plt.xlabel("Time (s)")
    plt.ylabel("Number of tasks")
    plt.legend(loc="upper right")
    plt.title("Tasks in status over time")
    for metric_name in stats.values.keys():
        if metric_name.endswith("OverTime"):
            values = stats.values[metric_name]
            X = values[0, :]
            Y = values[1, :]
            X = [(x - X[0]).total_seconds() for x in X]
            plt.plot(X, Y, label=metric_name)
    plt.savefig("metrics.png")


def print_metrics(stats):
    print(
        json.dumps(
            {name: value for name, value in stats.values.items() if not name.endswith("OverTime")}
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Compute statistics for tasks of a given session.")
    parser.add_argument("--endpoint", "-e", type=str, help="ArmoniK controle plane endpoint")
    parser.add_argument("--session-id", "-s", type=str, help="ID of the session")
    args = parser.parse_args()

    args.endpoint = args.endpoint.removeprefix("http://")

    with grpc.insecure_channel(args.endpoint) as channel:
        stats = ArmoniKStatistics(
            channel=channel,
            task_filter=TaskFieldFilter.SESSION_ID == args.session_id,
            metrics=[
                AvgThroughput(),
                TotalElapsedTime(),
                TimestampsTransition(TaskTimestamps.CREATED, TaskTimestamps.SUBMITTED),
                TimestampsTransition(TaskTimestamps.SUBMITTED, TaskTimestamps.RECEIVED),
                TimestampsTransition(TaskTimestamps.RECEIVED, TaskTimestamps.ACQUIRED),
                TimestampsTransition(TaskTimestamps.ACQUIRED, TaskTimestamps.FETCHED),
                TimestampsTransition(TaskTimestamps.FETCHED, TaskTimestamps.STARTED),
                TimestampsTransition(TaskTimestamps.STARTED, TaskTimestamps.PROCESSED),
                TimestampsTransition(TaskTimestamps.PROCESSED, TaskTimestamps.ENDED),
                TasksInStatusOverTime(TaskTimestamps.CREATED, TaskTimestamps.SUBMITTED),
                TasksInStatusOverTime(TaskTimestamps.SUBMITTED, TaskTimestamps.RECEIVED),
                TasksInStatusOverTime(TaskTimestamps.RECEIVED, TaskTimestamps.ACQUIRED),
                TasksInStatusOverTime(TaskTimestamps.ACQUIRED, TaskTimestamps.FETCHED),
                TasksInStatusOverTime(TaskTimestamps.FETCHED, TaskTimestamps.STARTED),
                TasksInStatusOverTime(TaskTimestamps.STARTED, TaskTimestamps.PROCESSED),
                TasksInStatusOverTime(TaskTimestamps.PROCESSED, TaskTimestamps.ENDED),
                TasksInStatusOverTime(TaskTimestamps.ENDED),
            ],
        )
        stats.compute()

        plot_metrics(stats)
        print_metrics(stats)
