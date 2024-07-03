from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models import Base


@dataclass
class Profile(Base, IdMixin):
    __tablename__ = "profiles"

    # Attributes
    date_of_birth: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    sex: Mapped[int] = mapped_column(nullable=True)
    religion: Mapped[str] = mapped_column(String(40), nullable=True)
    about: Mapped[str] = mapped_column(String(2000), nullable=True)
    hobby: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    soc_media: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

    # Relations
    _profile_user = relationship("User", back_populates="_user_profile")
    _profile_metric = relationship("Metric", back_populates="_metric_profile")
