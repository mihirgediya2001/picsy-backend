import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from server.utils.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    fb_uid = Column(String, unique=True)
    avatar = Column(String)
    browser_token = Column(String)
    age = Column(Integer, nullable=True)
    email = Column(String, unique=True)
    name = Column(String, index=True)
    password = Column(
        String,
    )
    is_verified = Column(Boolean, default=False)
    providers = Column(String)
    client_country = Column(String)
    client_ip = Column(String)
    client_browser = Column(String)
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
