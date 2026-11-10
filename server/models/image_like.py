import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from server.utils.database import Base


class ImageLike(Base):
    __tablename__ = "image_likes"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    image_id = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )

    user = relationship("User")
