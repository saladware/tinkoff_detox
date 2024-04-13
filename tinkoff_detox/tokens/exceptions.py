from ..exceptions import ItemException, ItemNotFoundException, ItemAlreadyExistsException


class TokenException(ItemException):
    item = "token"


class TokenNotFoundException(TokenException, ItemNotFoundException):
    pass


class TokenAlreadyExistsException(TokenException, ItemAlreadyExistsException):
    pass
