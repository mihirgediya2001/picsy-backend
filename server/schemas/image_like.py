import uuid
from typing import Optional

from pydantic import BaseModel


class ImageLikeBase(BaseModel):
    id: Optional[str] = None
    image_id: Optional[str] = None
    created_at: Optional[str] = None
    user_id: Optional[uuid.UUID] = None


class ImageLikeCreate(ImageLikeBase):
    pass


class ImageLikeUpdate(ImageLikeBase):
    pass


class ImageLikeUpdate(ImageLikeBase):
    pass


class ImageID(BaseModel):
    image_id: str
