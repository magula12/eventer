from .role import Role

class EventCategory:
    def __init__(self,id: int, techName: str, description: str, priority : int):
        self.id = id
        self.techName = techName
        self.description = description
        self.priority = priority
        self.roles = []

    def __str__(self) -> str:
        return f"{self.techName} ({self.priority})"

    def __repr__(self) -> str:
        return f"{self.techName} ({self.priority})"

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

    def get_techName(self) -> str:
        return self.techName

    def get_description(self) -> str:
        return self.description

    def get_priority(self) -> int:
        return self.priority

    def set_techName(self, techName: str) -> None:
        self.techName = techName

    def set_description(self, description: str) -> None:
        self.description = description

    def set_priority(self, priority: int) -> None:
        self.priority = priority

    def add_role(self, role : Role) -> None:
        self.roles.append(role)

    def get_roles(self) -> list[Role]:
        return self.roles