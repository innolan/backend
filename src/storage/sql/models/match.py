from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models.base import Base


@dataclass
class Match(Base):
    __tablename__ = "matches"

    # Attributes
    primary_id: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
        primary_key=True,
        nullable=True,
    )
    secondary_id: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
        primary_key=True,
        nullable=True,
    )

