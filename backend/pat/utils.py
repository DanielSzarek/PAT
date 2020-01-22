from enum import IntEnum


class UserType(IntEnum):
    CLIENT = 1
    COURIER = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PackStatus(IntEnum):
    OPEN = 1
    IN_PROGRESS = 2
    CLOSED = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]