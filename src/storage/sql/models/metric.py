from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models.base import Base


class Metric(Base, IdMixin):
    __tablename__ = "metrics"

    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(String(40))
    value: Mapped[float] = mapped_column()

    metric_profile = relationship("Profile", back_populates="profile_metric")
