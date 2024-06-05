from enum import Enum

class Event_type(Enum):
    BREAK = "break"
    REPAIR = "repair"

class Event:
    def __init__(self, event_type: Event_type, event_day: float) -> None:
        self.event_type = event_type
        self.event_day = event_day

