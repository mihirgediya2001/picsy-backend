import uuid
from typing import Optional

from pydantic import BaseModel


class AdminConfigBase(BaseModel):
    id: Optional[str] = None
    data: Optional[dict] = None
