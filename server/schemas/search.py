from typing import Optional
from pydantic import BaseModel, constr


class SearchBase(BaseModel):
    prompt: Optional[str] = None
    client_country: Optional[str] = None
    client_ip: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class SearchCreate(SearchBase):
    pass


class SearchUpdate(SearchBase):
    pass


class FreeSearchLogin(BaseModel):
    browser_token: constr(min_length=8)


class SearchPrompt(BaseModel):
    query: Optional[str] = ""
    search_after: Optional[str] = None
    location: Optional[str] = None
    ip: Optional[str] = None


class SearchSuggestions(BaseModel):
    query: Optional[str]


class SearchById(BaseModel):
    id: Optional[str]
