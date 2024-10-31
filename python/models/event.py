from enum import Enum

class EventCategory(Enum):
    HOCKEY_EL = "Hokej - Extraliga"
    HOCKEY_SHL = "Hokej - Slovenská hokejová liga"
    BASKETBALL_SBL = "Basketball - Slovenská basketbalová liga"
    VOLLEYBALL_MEN = "Volleyball - Extraliga muži"
    VOLLEYBALL_WOMEN = "Volleyball - Extraliga ženy"
class Event:
    def __init__(self, category):
        self.category = category