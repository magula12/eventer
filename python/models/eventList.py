from .event import Event
from typing import Union

class EventList:
    def __init__(self, events: list[Event]):
        self.events = events

    def __iter__(self):
        return iter(self.events)

    def get_events(self) -> list[Event]:
        return self.events

    def get_event(self, index: int) -> Event:
        return self.events[index]

    def add_event(self, event: Event):
        self.events.append(event)

    def remove_event(self, item: Union[int, "Event"]):
        if isinstance(item, int):
            if 0 <= item < len(self.events):
                del self.events[item]
            else:
                raise IndexError("Index out of range.")
        elif isinstance(item, Event):
            try:
                self.events.remove(item)
            except ValueError:
                raise ValueError("Event not found in list.")
        else:
            raise TypeError("Argument must be an int (index) or an Event object.")

    def sort(self):
        self.events.sort()