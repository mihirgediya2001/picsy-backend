from typing import Optional

from pydantic import BaseModel


class JoinBetaSchema(BaseModel):
    email: Optional[str] = None
