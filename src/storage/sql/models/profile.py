from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models import Base


class Profile(Base, IdMixin):
    __tablename__ = "profiles"

    # Attributes
    date_of_birth: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    sex: Mapped[int] = mapped_column(nullable=True)
    religion: Mapped[str] = mapped_column(String(40), nullable=True)
    about: Mapped[str] = mapped_column(String(2000), nullable=True)

    # Relations
    profile_user = relationship("User", back_populates="user_profile")
    profile_metric = relationship("Metric", back_populates="metric_profile")
