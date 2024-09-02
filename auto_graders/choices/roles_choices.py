from enum import Enum


class RoleEnum(Enum):
    ADMIN = "Admin"
    STUDENT = "Student"
    MODERATOR = "Moderator"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
