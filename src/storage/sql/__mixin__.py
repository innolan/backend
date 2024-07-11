from sqlalchemy import BigInteger, Column, Integer
from sqlalchemy.orm import Mapped


class IdMixin:
    id: Mapped[int] = Column(BigInteger, primary_key=True)
