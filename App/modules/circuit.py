from enum import Enum
from event import Event, Event_type
from thermoelectric import ThermoElectric, ThermoElectric_State


class Circuit_State(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class Circuit:
    def __init__(self, demand: float, associated_thermoelectric: list[ThermoElectric]):
        self.demand = demand
        self.associated_thermoelectric = associated_thermoelectric
        self.future_events = []
        self.history = []

    def is_connected(self):
        for thermoelectric in self.associated_thermoelectric:
            if thermoelectric.is_working():
                return True
        return False

    def is_disconnected(self):
        return not self.is_connected()

    def get_state(self):
        return (
            Circuit_State.CONNECTED
            if self.is_connected()
            else Circuit_State.DISCONNECTED
        )

    def get_current_demand(self):
        if self.is_disconnected():
            return 0
        return self.demand

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

    def get_history(self) -> list[Event]:
        pass

    def get_distributions_info(self):
        pass

    def plot(self, from_day=0, to_day=None):  # WARNING IN PROCESS
        pass
