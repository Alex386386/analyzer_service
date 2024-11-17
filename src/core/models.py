from typing import Optional

from sqlalchemy import (
    String,
    Text,
    DateTime,
    Integer,
    Float,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.core.db import Base


class SalesData(Base):
    __tablename__ = "sales_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    product_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String)
    create_date: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), server_default=func.now()
    )
    update_date: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=func.now(),
        default=func.now(),
        server_default=func.now(),
    )


class AnalysisReport(Base):
    __tablename__ = "analysis_report"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    date: Mapped[DateTime] = mapped_column(TIMESTAMP(timezone=True))
    start_prompt: Mapped[str] = mapped_column(Text)
    report: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    create_date: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), server_default=func.now()
    )
    update_date: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=func.now(),
        default=func.now(),
        server_default=func.now(),
    )
