__all__ = ["Message", "NoUserException", "NoProfileException"]

from fastapi import HTTPException, status
from pydantic import BaseModel


class Message(BaseModel):
    message: str


class UserHaveAlreadySignedInMessage(Message):
    message: str = "User have already signed in"


class NoUserException(HTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found",
        )


class UserNotFoundMessage(Message):
    message: str = "User not found"


class NoProfileException(HTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile found (really bad)",
        )


class ProfileNotFoundMessage(Message):
    message: str = "Profile not found"


class EntityExistsException(HTTPException):
    """
    HTTP_409_CONFLICT
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Entity exists",
        )


class NoMetricException(HTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No metric found",
        )


class UnauthorizedException(HTTPException):
    """
    HTTP_401_UNAUTHORIZED
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


### PRUNE ABOVE


class EntityExistsException(HTTPException):
    """
    HTTP_409_CONFLICT
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Entity exists",
        )


class EntityNotFoundException(HTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No entity found: {detail}",
        )

class NotImplementedException(HTTPException):
    """
    HTTP_501_NOT_IMPLEMENTED
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Not implemented",
        )