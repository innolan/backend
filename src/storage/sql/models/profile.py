from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models import Base


@dataclass
class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    
    # Attributes
    date_of_birth: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    sex: Mapped[int] = mapped_column(nullable=True)
    religion: Mapped[str] = mapped_column(String(40), nullable=True)
    about: Mapped[str] = mapped_column(String(2000), nullable=True)
    hobby: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    soc_media: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    
    # Relations
    _profile_user = relationship("User", back_populates="_user_profile")
    _profile_metric = relationship("Metric", back_populates="_metric_profile", cascade="all, delete-orphan")
