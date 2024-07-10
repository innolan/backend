from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models.base import Base


@dataclass
class User(Base, IdMixin):
    __tablename__ = "users"

    # Attributes
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    username: Mapped[str] = mapped_column(String(60), nullable=True)
    photo_url: Mapped[str] = mapped_column(String(200), nullable=True)
    auth_date_hash: Mapped[str] = mapped_column(String(200))

    # Relations
    profile = relationship("Profile", back_populates="user")
    _user_participant = relationship(
        "Participant", back_populates="_participant_user", cascade="all, delete-orphan"
    )
