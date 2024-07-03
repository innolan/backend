from dataclasses import dataclass
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models.base import Base


@dataclass
class Metric(Base, IdMixin):
    __tablename__ = "metrics"

    # Attributes
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(40))
    value: Mapped[float] = mapped_column()

    # Relations
    _metric_profile = relationship("Profile", back_populates="_profile_metric")
