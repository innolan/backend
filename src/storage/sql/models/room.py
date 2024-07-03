from dataclasses import dataclass
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models.base import Base


@dataclass
class Room(Base, IdMixin):
    __tablename__ = "rooms"

    # Attributes
    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(400))
    capacity: Mapped[int] = mapped_column()
    occupacy: Mapped[int] = mapped_column()

    # Relations
    _room_participant = relationship("Participant", back_populates="_participant_room")
