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
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[Optional[str]] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(60))
    photo_url: Mapped[str] = mapped_column(String(200))
    auth_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relations
    _user_profile = relationship("Profile", back_populates="_profile_user", cascade="all, delete-orphan")
    _user_participant = relationship("Participant", back_populates="_participant_user", cascade="all, delete-orphan")
