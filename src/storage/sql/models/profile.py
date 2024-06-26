from datetime import datetime
from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.models import Base
from src.storage.sql.__mixin__ import IdMixin


class Profile(Base, IdMixin):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column()
    photo: Mapped[str] = mapped_column(String(40))
    date_birth: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    sex: Mapped[int] = mapped_column()
    religion: Mapped[str] = mapped_column(String(40))
    about: Mapped[str] = mapped_column(String(1000))

    profile_user = relationship("User", back_populates="user_profile")
    # profile_metric = relationship("Metric", back_populates="metric_profile")
