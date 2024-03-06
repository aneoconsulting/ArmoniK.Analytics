from enum import IntEnum


class TaskTimestamps(IntEnum):
    CREATED = 0
    SUBMITTED = 1
    RECEIVED = 2
    ACQUIRED = 3
    FETCHED = 4
    STARTED = 5
    PROCESSED = 6
    ENDED = 7
