from enum import Enum
from App.modules.event import Event, Event_type
from App.modules.thermoelectric import ThermoElectric, ThermoElectric_State
import numpy as np


class Circuit_State(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class Circuit:
    def __init__(self, id: int, demand: float, days: int):
        self.id: int = id
        self.demand: float = demand
        self.future_events = []
        self.deficit_history: list[float] = np.zeros(days)
        self.total_deficit: float = 0
        self.days_disconnected: int = 0
        self.days: int = days

    def disconnect(self, percentage: float, current_day: int):
        print(f"Disconnecting {self.demand * percentage} from circuit {self.id} on day {current_day}")
        self.total_deficit += self.demand * percentage
        print(f"Total deficit: {self.total_deficit}")
        self.deficit_history[current_day] = self.demand * percentage
        print(f"Today's deficit: {self.deficit_history[current_day]}")
        self.days_disconnected += 1
        print(f"Days disconnected: {self.days_disconnected}")

    # def is_connected(self):
    #     for thermoelectric in self.associated_thermoelectric:
    #         if thermoelectric.is_working():
    #             return True
    #     return False

    # def is_disconnected(self):
    #     return not self.is_connected()

    # def get_state(self):
    #     return (
    #         Circuit_State.CONNECTED
    #         if self.is_connected()
    #         else Circuit_State.DISCONNECTED
    #     )

    # def get_current_demand(self):
    #     if self.is_disconnected():
    #         return 0
    #     return self.demand

    def get_next_future_event_day(self) -> int:
        pass

    def pop_next_future_event(self) -> Event:
        pass

    def __generate_next_event(self, flip_flop: bool) -> Event:
        pass

    def planificate_events(
        self, days: int, initial_state_flip_flop: bool = False
    ) -> None:
        pass

    def repair_and_replanificate(self, days_to_replanificate) -> None:
        pass

    def get_history(self) -> "list[Event]":
        pass

    def get_distributions_info(self):
        pass

    def plot(self, from_day=0, to_day=None):  # WARNING IN PROCESS
        pass

    def __str__(self):
        return f"Circuit {self.id} with demand {self.demand} and {self.days_disconnected} days disconnected"
