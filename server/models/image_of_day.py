from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from server.utils.database import Base


class ImageOfDay(Base):
    __tablename__ = "image_of_day"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    image_id = Column(String)

