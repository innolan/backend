from datetime import datetime
from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.models import Base
from src.storage.sql.__mixin__ import IdMixin


class Profile(Base, IdMixin):
    __tablename__ = "profiles"

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(30))
    photo_url: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    sex: Mapped[int] = mapped_column(nullable=True)
    religion: Mapped[str] = mapped_column(String(40), nullable=True)
    about: Mapped[str] = mapped_column(String(2000), nullable=True)

    profile_user = relationship("User", back_populates="user_profile")
    # profile_metric = relationship("Metric", back_populates="metric_profile")
