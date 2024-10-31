from .event import Event
from .person import Person
from .role import Role
from .eventCategory import EventCategory

class EventPerson:
    def __init__(self, event: Event, person: Person):
        self.event = event
        self.person = person

    def get_event(self) -> Event:
        return self.event

    def get_person(self) -> Person:
        return self.person

    def __eq__(self, other):
        return self.event == other.event and self.person == other.person

    def __hash__(self):
        return hash((self.event, self.person))

    def __str__(self):
        return f"{self.person.get_full_name()} is participating in {self.event.name}"

    def __repr__(self):
        return f"EventPerson({self.event}, {self.person})"

class PersonRoleQualification:
    def __init__(self, person: Person, role: Role, category: EventCategory, qualified: bool):
        self.person = person
        self.role = role
        self.category = category
        self.qualified = qualified

    def set_qualified(self, qualified: bool):
        self.qualified = qualified

    def __hash__(self):
        return hash((self.person, self.role, self.category))

    def __str__(self):
        return f"{self.person.get_full_name()} is qualified as {self.role.name} for {self.category.techName}"

    def __repr__(self):
        return f"PersonRoleQualification({self.person}, {self.role}, {self.category}, {self.qualified})"

    def get_person(self) -> Person:
        return self.person

    def get_role(self) -> Role:
        return self.role

    def get_category(self) -> EventCategory:
        return self.category

    def is_qualified(self) -> bool:
        return self.qualified