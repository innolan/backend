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


class NoMetricException(HTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No metric found",
        )
