from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import UtcDateTime


class Lab(Base):
    __tablename__ = "labs"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(String(200))
    # The deadline is stored in UTC (aware). The instructor enters it in department time.
    deadline: Mapped[datetime] = mapped_column(UtcDateTime())
    max_score: Mapped[int] = mapped_column(default=100)
