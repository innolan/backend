from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models.base import Base


@dataclass
class Match(Base, IdMixin):
    __tablename__ = "matches"

    # Attributes
    profileid_1: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=True)
    profileid_2: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=True)

    # Relations
    _match1_profile = relationship(
        "Profile", backref="user1", foreign_keys=[profileid_1]
    )
    _match2_profile = relationship(
        "Profile", backref="user2", foreign_keys=[profileid_2]
    )
