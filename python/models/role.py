class Role:
    def __init__(self,id: int, name: str, priority: int):
        self.id = id
        self.name = name
        self.priority = priority

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_priority(self) -> int:
        return self.priority

    def set_priority(self, priority: int) -> None:
        self.priority = priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __ne__(self, other):
        return self.priority != other.priority

    def __hash__(self):
        return hash(self.priority)
