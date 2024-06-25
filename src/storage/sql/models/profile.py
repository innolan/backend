from datetime import datetime
from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.models import Base
from src.storage.sql.__mixin__ import IdMixin


class Profile(Base, IdMixin):
    __tablename__ = "profiles"

    Name: Mapped[str] = mapped_column(String(100))
    Age: Mapped[int] = mapped_column()
    Photo: Mapped[str] = mapped_column(String(40))
    Date_birth: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    Sex: Mapped[int] = mapped_column()
    Religion: Mapped[str] = mapped_column(String(40))
    About: Mapped[str] = mapped_column(String(1000))

    profile_user = relationship("User", back_populates="user_profile")
    # profile_metric = relationship("Metric", back_populates="metric_profile")
