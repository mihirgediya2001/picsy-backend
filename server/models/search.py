from datetime import datetime

from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from server.utils.database import Base


class Search(Base):
    __tablename__ = "search_prompt"
    id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    response = Column(JSON)
    client_country = Column(String)
    client_ip = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )

    user = relationship("User")
