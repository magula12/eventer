from ..models.eventList import EventList
from ..models.person import Person
from ..models.event import Event
from ..models.role import Role

# toto nie je algorithmus, je len priradovanie po rade
def get_best_person(people : list[Person], event : Event, role : Role) -> Person:
    best_person = None
    for person in people:
        if person.is_free(event.start_date, event.end_date):
            if person.has_role(role):
                if best_person is None or person.get_role_rating(role) > best_person.get_role_rating(role):
                    best_person = person
    return best_person

def assign_events(events : EventList, people : list[Person]) -> None:
    # Sort events by priority
    events.sort()

    for event in events:
        # Get the best person for the event
        for role in event.category.get_roles():
            person = get_best_person(people, event, role)
            if person is not None:
                event.add_participant(person, role)
                person.add_off_time(event.start_date, event.end_date)
                break
        else:
            print(f"No person available for event {event.name}.")