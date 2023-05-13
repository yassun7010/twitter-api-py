from typing_extensions import Literal

DmEventType = Literal[
    "MessageCreate",
    "ParticipantsJoin",
    "ParticipantsLeave",
]

ALL_DM_EVENT_TYPES: list[DmEventType] = [
    "MessageCreate",
    "ParticipantsJoin",
    "ParticipantsLeave",
]
