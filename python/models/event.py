from .eventCategory import EventCategory
from .person import Person
from datetime import date, time

class Event:
    def __init__(self, id :int, category: EventCategory, priority: int, name: str, date: date, time: time, description: str):
        self.id = id
        self.category = category
        self.priority = priority
        self.name = name
        self.date = date
        self.time = time
        self.participants = []
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
        return self.date == other.date and self.time == other.time and self.name == other.name

    def set_category(self, category: EventCategory) -> None:
        self.category = category

    def set_name(self, name: str) -> None:
        self.name = name

    def set_date(self, date: date) -> None:
        self.date = date

    def set_time(self, time: time) -> None:
        self.time = time

    def set_participants(self, participants: list[Person]) -> None:
        self.participants = participants

    def set_description(self, description: str) -> None:
        self.description = description

    def get_category(self) -> EventCategory:
        return self.category

    def get_name(self) -> str:
        return self.name

    def get_date(self) -> date:
        return self.date

    def get_time(self) -> time:
        return self.time

    def get_participants(self) -> list[Person]:
        return self.participants

    def get_description(self) -> str:
        return self.description

    def add_participant(self, participant: Person) -> None:
        self.participants.append(participant)

    def remove_participant(self, participant: Person) -> None:
        self.participants.remove(participant)

    def is_participant(self, participant: Person) -> bool:
        return participant in self.participants

    def is_happening_today(self) -> bool:
        return self.date == date.today()

    def is_happening_now(self) -> bool:
        return self.date == date.today() and self.time == time.now()

    def is_happening_soon(self) -> bool:
        return self.date == date.today() and self.time == time.now() + 1