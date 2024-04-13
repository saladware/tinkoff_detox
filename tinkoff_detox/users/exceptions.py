from ..exceptions import (
    ItemException,
    ItemNotFoundException,
    ItemAlreadyExistsException,
)


class AuthenticationException(Exception):
    def __init__(self, message: str = "wrong email or password"):
        self.message = message


class UserException(ItemException):
    item = "user"


class UserNotFoundException(UserException, ItemNotFoundException):
    pass


class UserAlreadyExistsException(UserException, ItemAlreadyExistsException):
    pass