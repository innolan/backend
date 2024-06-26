from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.models import Base
from src.storage.sql.__mixin__ import IdMixin


class Participant(Base, IdMixin):
    __tablename__ = "participants"

    participant_user = relationship(
        "User",
        back_populates="user_participant",
    )
