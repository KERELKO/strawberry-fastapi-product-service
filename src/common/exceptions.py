from dataclasses import dataclass


class ApplicationException(Exception):
    ...


@dataclass(eq=False, frozen=True)
class ObjectDoesNotExistException(ApplicationException):
    object: str
    object_id: int = None

    def __str__(self) -> str:
        return f'{self.object} not found' + f', id: {self.object_id}' if self.object_id else ''


class IDIsNotProvided(ApplicationException):
    def __str__(self) -> str:
        return 'ID for the object is not provided'
