from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime

from app.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        String,
        primary_key=True,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )