import argparse
import json

import grpc
import matplotlib.pyplot as plt

from armonik.client import TaskFieldFilter
from armonik.stats import ArmoniKStatistics
from armonik.stats.metrics import AvgThroughput, TotalElapsedTime, TimestampsTransition, TasksInStatusOverTime


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Compute statistics for tasks of a given session.")
    parser.add_argument("--endpoint", "-e", type=str, help="ArmoniK controle plane endpoint")
    parser.add_argument("--session-id", "-s", type=str, help="ID of the session")
    args = parser.parse_args()

    if args.endpoint.startswith("http://"):
        args.endpoint = args.endpoint.removeprefix("http://")

    with grpc.insecure_channel(args.endpoint) as channel:
        stats = ArmoniKStatistics(
            channel=channel,
            task_filter=TaskFieldFilter.SESSION_ID == args.session_id,
            metrics=[
                AvgThroughput(),
                TotalElapsedTime(),
                TimestampsTransition("created", "submitted"),
                TimestampsTransition("submitted", "received"),
                TimestampsTransition("received", "acquired"),
                TimestampsTransition("acquired", "fetched"),
                TimestampsTransition("fetched", "started"),
                TimestampsTransition("started", "processed"),
                TimestampsTransition("processed", "ended"),
                TasksInStatusOverTime("processed", "ended"),
                TasksInStatusOverTime("ended"),
            ]
        )
        stats.compute()

        plt.figure()
        for metric_name in stats.values.keys():
            if metric_name.endswith("OverTime"):
                values = stats.values[metric_name]
                X = values[0,:]
                Y = values[1,:]
                X = [(x - X[0]).total_seconds() for x in X]
                plt.plot(X, Y, label=metric_name)
        plt.savefig(f"metrics.png")

        print(json.dumps({name: value for name, value in stats.values.items() if not name.endswith("OverTime")}))
