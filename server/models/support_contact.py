from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String

from server.utils.database import Base


class SupportContact(Base):
    __tablename__ = "support_contact"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    message = Column(String, nullable=False)
    client_host = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now)
