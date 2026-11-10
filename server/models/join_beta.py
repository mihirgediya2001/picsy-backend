from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String

from server.utils.database import Base


class JoinBeta(Base):
    __tablename__ = "join_beta"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    client_host = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now)
