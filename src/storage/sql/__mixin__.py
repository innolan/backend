from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
