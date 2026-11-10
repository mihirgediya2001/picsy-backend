from typing import Optional
from pydantic import BaseModel


class ImageOfDayBase(BaseModel):
    id: Optional[str] = None
    date: Optional[str] = None
    image_id: Optional[str] = None

    class Config:
        orm_mode = True


class ImageOfDayCreate(ImageOfDayBase):
    pass


class ImageOfDayUpdate(ImageOfDayBase):
    pass
