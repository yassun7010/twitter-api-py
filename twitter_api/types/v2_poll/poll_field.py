from typing_extensions import Literal

PollField = Literal[
    "duration_minutes",
    "end_datetime",
    "id",
    "options",
    "voting_status",
]


ALL_POLL_FIELDS: list[PollField] = [
    "duration_minutes",
    "end_datetime",
    "id",
    "options",
    "voting_status",
]
