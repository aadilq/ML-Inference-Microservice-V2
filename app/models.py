from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime
from sqlalchemy import Text, Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime, func
from sqlalchemy import String
from app.database import Base


class Request(Base):
    __tablename__ = "inference_requests"

    request_id: Mapped[int] = mapped_column(primary_key=True)
    video_url : Mapped[str] = mapped_column(String(500), nullable=False)
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    segment_count: Mapped[int] = mapped_column(nullable=False)
    created_at : Mapped[datetime.datetime] = mapped_column(
          DateTime(timezone=True),
          server_default=func.now()
     )

class Result(Base):
    __tablename__ = "inference_results"

    result_id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("inference_requests.request_id"))
    segment_index: Mapped[int]
    raw_text : Mapped[str] = mapped_column(String(500), nullable=False)
    score : Mapped[float] = mapped_column(Float, nullable=False)
    topic : Mapped[str] = mapped_column(Text, nullable=False)
    energy_level : Mapped[str] = mapped_column(String(10), nullable=False)
    created_at : Mapped[datetime.datetime] = mapped_column(
          DateTime(timezone=True),
          server_default=func.now()
     )