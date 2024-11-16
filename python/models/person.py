from .role import Role
from datetime import datetime, timedelta

class Person:
    def __init__(self, id: int, name: str, surname: str, admin: bool, email: str, phone_number: str):
        self.id = id
        self.name = name
        self.surname = surname
        self.admin = admin
        self.email = email
        self.phone_number = phone_number
        self.roles = []
        self.off_times = []

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"

    def __repr__(self) -> str:
        return f"{self.name} {self.surname}"

    def __eq__(self, other) -> bool:
        return (self.name == other.name and
                self.email == other.email and
                self.phone_number == other.phone_number)

    def set_name(self, name: str) -> None:
        self.name = name

    def set_surname(self, surname: str) -> None:
        self.surname = surname

    def set_admin(self, admin: bool) -> None:
        self.admin = admin

    def set_email(self, email: str) -> None:
        self.email = email

    def set_phone_number(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def get_name(self) -> str:
        return self.name

    def get_surname(self) -> str:
        return self.surname

    def get_full_name(self) -> str:
        return f"{self.name} {self.surname}"

    def get_admin(self) -> bool:
        return self.admin

    def get_email(self) -> str:
        return self.email

    def get_phone_number(self) -> str:
        return self.phone_number

    def is_admin(self) -> bool:
        return self.admin

    def add_role(self, role: Role, rating: int = None):
        self.roles.append({"role": role, "rating": rating})

    def remove_role(self, role: Role):
        self.roles = [r for r in self.roles if r["role"] != role]

    def get_roles(self):
        return self.roles

    def has_role(self, role: Role):
        return any([r["role"] == role for r in self.roles])

    def get_role_rating(self, role: Role):
        for r in self.roles:
            if r["role"] == role:
                return r["rating"]
        return None

    """If the role is not in the list, it will be added. If it is, it will be updated."""
    def set_role_rating(self, role: Role, rating: int):
        for r in self.roles:
            if r["role"] == role:
                r["rating"] = rating
                return
        self.add_role(role, rating)

    def __hash__(self) -> int:
        return hash(self.name + self.email + self.phone_number)

    def add_off_time(self, start_date: datetime, end_date: datetime):
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")
        self.off_times.append((start_date, end_date))

    def remove_off_time(self, start_date: datetime, end_date: datetime):
        self.off_times = [ot for ot in self.off_times if ot != (start_date, end_date)]

    def get_off_times(self):
        return self.off_times

    def is_free(self, start_date: datetime, end_date: datetime):
        for ot in self.off_times:
            if not (end_date <= ot[0] or start_date >= ot[1]):
                return False
        return True