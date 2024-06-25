from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.models.base import Base
from src.storage.sql.__mixin__ import IdMixin


class User(Base, IdMixin):
    __tablename__ = "users"

    Profile_ID: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
        nullable=True,
    )
    Participant_ID: Mapped[int] = mapped_column(
        ForeignKey("participants.id"),
        nullable=True,
    )
    Tg_id = mapped_column(BigInteger)
    User_name: Mapped[str] = mapped_column(String(30))

    user_profile = relationship(
        "Profile",
        back_populates="profile_user",
    )
    user_participant = relationship(
        "Participant",
        back_populates="participant_user",
    )
