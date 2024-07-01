from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models.base import Base


class Match(Base, IdMixin):
    __tablename__ = "matches"

    profileid_1: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
        nullable=True,
    )

    profileid_2: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
        nullable=True,
    )

    match1_profile = relationship("Profile", back_populates='profile_match1', foreign_keys=[profileid_1])
    match2_profile = relationship("Profile", back_populates='profile_match2', foreign_keys=[profileid_2])
