from .eventCategory import EventCategory
from .person import Person
from .role import Role
from datetime import datetime, timedelta

class Event:
    def __init__(self, id :int, category: EventCategory, priority: int, name: str,
                 start_date: datetime, end_date: datetime = None, description: str = ""):
        self.id = id
        self.category = category
        self.priority = priority
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.participants = {}
        self.description = description

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return self.priority == other.priority

    def __lt__(self, other) -> bool:
        return self.priority < other.priority

    def __gt__(self, other) -> bool:
        return self.priority > other.priority

    def __ge__(self, other) -> bool:
        return self.priority >= other.priority

    def __le__(self, other) -> bool:
        return self.priority <= other.priority

    def __hash__(self) -> int:
        return self.priority

    def is_same_event(self, other) -> bool:
        return self.id == other.id

    def set_category(self, category: EventCategory) -> None:
        self.category = category

    def set_name(self, name: str) -> None:
        self.name = name

    def set_start_date(self, start_date: datetime) -> None:
        self.start_date = start_date

    def set_end_date(self, end_date: datetime) -> None:
        self.end_date = end_date

    def set_participants(self, participants: list[Person]) -> None:
        self.participants = participants

    def set_description(self, description: str) -> None:
        self.description = description

    def get_category(self) -> EventCategory:
        return self.category

    def get_name(self) -> str:
        return self.name

    def get_start_date(self) -> datetime:
        return self.start_date

    def get_end_date(self) -> datetime:
        return self.end_date

    def get_participants(self) -> list[Person]:
        return list(self.participants.values())

    def get_description(self) -> str:
        return self.description

    def add_participant(self, participant: Person, role : Role) -> None:
        self.participants[role] = participant

    def remove_participant(self, participant: Person) -> None:
        for role, p in self.participants.items():
            if p == participant:
                del self.participants[role]
                return

    def is_participant(self, participant: Person) -> bool:
        return any([p == participant for p in self.participants.values()])