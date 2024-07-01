from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models import Base


class Participant(Base, IdMixin):
    __tablename__ = "participants"

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
        nullable=True,
    )

    participant_user = relationship(
        "User",
        back_populates="user_participant",
    )

    participant_room = relationship(
        "Room",
        back_populates="room_participant"
    )
