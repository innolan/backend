from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models import Base


@dataclass
class Participant(Base, IdMixin):
    __tablename__ = "participants"

    # Attributes
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=True)

    # Relations
    _participant_user = relationship("User", back_populates="_user_participant")
    _participant_room = relationship("Room", back_populates="_room_participant")
