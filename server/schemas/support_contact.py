from pydantic import BaseModel


class SupportContactSchema(BaseModel):
    email: str = None
    name: str = None
    message: str = None
