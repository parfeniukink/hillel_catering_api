from enum import StrEnum, auto
from functools import lru_cache


class Role(StrEnum):
    ADMIN = auto()
    MANAGER = auto()
    DRIVER = auto()
    CLIENT = auto()

    @classmethod
    @lru_cache(maxsize=1)
    def users(cls) -> list[str]:
        return [cls.DRIVER, cls.CLIENT]

    @classmethod
    @lru_cache(maxsize=1)
    def choices(cls) -> list[tuple[str, str]]:
        # ('admin', "Aenior")
        # ('manager', "Manager")
        # ('driver', "Driver")
        # ('client', "Client")

        results = []

        for element in cls:
            # >>> Role.ADMIN [name: ADMIN, value: ADMIN]
            _element = (element.value, element.name.lower().capitalize())
            results.append(_element)

        return results
