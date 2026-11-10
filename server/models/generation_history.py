import uuid

from datetime import datetime

from sqlalchemy import JSON, TIMESTAMP, Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from server.utils.database import Base


class GenerationHistory(Base):
    __tablename__ = "generation_history"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    prompt = Column(String, nullable=False)
    inputs = Column(JSON)
    output = Column(JSON)
    is_deleted = Column(Boolean, server_default="False")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )

    user = relationship("User")
